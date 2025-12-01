"""
REST API untuk Aplikasi Kasir Digital - Version 2.0
Menggunakan Flask Framework dengan JWT Authentication
"""

from flask import Flask, request, jsonify
from flasgger import Swagger
from datetime import datetime
from config import DAFTAR_PRODUK, DATE_FORMAT
from database import db
from auth import AuthManager, token_required

# Inisialisasi Flask app
app = Flask(__name__)

# Inisialisasi Swagger untuk dokumentasi API
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Kasir Digital API",
        "version": "2.0.0",
        "description": "REST API untuk mengelola transaksi top-up digital dengan JWT authentication"
    },
    "basePath": "/",
    "schemes": ["http", "https"]
})

# ============ ROUTES ============

@app.route('/', methods=['GET'])
def home():
    """Endpoint home - untuk cek apakah API berjalan"""
    return jsonify({
        "status": "success",
        "version": "2.0.0",
        "message": "Selamat datang di Kasir Digital API v2.0",
        "features": ["Authentication", "JWT Token", "Protected Endpoints"],
        "info": "Gunakan /auth/register dan /auth/login untuk memulai"
    }), 200


# ============ AUTHENTICATION ROUTES ============

@app.route('/auth/register', methods=['POST'])
def register():
    """
    Register user baru
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: yusuf
            password:
              type: string
              example: password123
    responses:
      201:
        description: User berhasil terdaftar
        schema:
          properties:
            status:
              type: string
              example: success
            message:
              type: string
      400:
        description: Username sudah ada atau input tidak valid
    """
    try:
        data = request.get_json(force=True, silent=False)
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                "status": "error",
                "message": "Username dan password harus disediakan"
            }), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                "status": "error",
                "message": "Username dan password tidak boleh kosong"
            }), 400
        
        response, status_code = AuthManager.register(username, password)
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Username dan password harus disediakan"
        }), 400


@app.route('/auth/login', methods=['POST'])
def login():
    """
    Login dan dapatkan JWT token
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login berhasil, return JWT token
        schema:
          properties:
            status:
              type: string
            message:
              type: string
            token:
              type: string
      401:
        description: Username atau password salah
    """
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                "status": "error",
                "message": "Username dan password harus disediakan"
            }), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        response, status_code = AuthManager.login(username, password)
        return jsonify(response), status_code
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500


# ============ PROTECTED ROUTES (Butuh Token) ============

@app.route('/api/produk', methods=['GET'])
@token_required
def get_produk():
    """Endpoint untuk mendapatkan daftar produk"""
    produk_list = []
    for kode, info in DAFTAR_PRODUK.items():
        produk_list.append({
            "kode": kode,
            "nama": info['nama'],
            "harga": info['harga'],
            "kategori": info['kategori']
        })
    
    return jsonify({
        "status": "success",
        "data": produk_list,
        "total": len(produk_list)
    }), 200


@app.route('/api/transaksi', methods=['POST'])
@token_required
def buat_transaksi():
    """Endpoint untuk membuat transaksi baru"""
    try:
        data = request.get_json()
        
        if not data or 'nama' not in data or 'kode_produk' not in data:
            return jsonify({
                "status": "error",
                "message": "Nama dan kode_produk harus disediakan"
            }), 400
        
        nama = data.get('nama', '').strip()
        kode_produk = data.get('kode_produk', '').upper().strip()
        
        if not nama:
            return jsonify({
                "status": "error",
                "message": "Nama pembeli tidak boleh kosong"
            }), 400
        
        if kode_produk not in DAFTAR_PRODUK:
            return jsonify({
                "status": "error",
                "message": f"Kode produk '{kode_produk}' tidak ditemukan"
            }), 404
        
        produk = DAFTAR_PRODUK[kode_produk]
        tanggal = datetime.now().strftime(DATE_FORMAT)
        
        transaksi = {
            "tanggal": tanggal,
            "nama": nama,
            "produk": produk['nama'],
            "kategori": produk['kategori'],
            "harga": produk['harga'],
            "operator": request.username
        }
        
        db.tambah_transaksi(transaksi)
        
        return jsonify({
            "status": "success",
            "message": "Transaksi berhasil dibuat",
            "data": transaksi
        }), 201
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500


@app.route('/api/riwayat', methods=['GET'])
@token_required
def get_riwayat():
    """Endpoint untuk mendapatkan riwayat transaksi"""
    try:
        nama = request.args.get('nama')
        
        if nama:
            transaksi_list = db.get_transaksi_by_nama(nama)
        else:
            transaksi_list = db.get_semua_transaksi()
        
        return jsonify({
            "status": "success",
            "data": transaksi_list,
            "total": len(transaksi_list)
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500


@app.route('/api/laporan', methods=['GET'])
@token_required
def get_laporan():
    """Endpoint untuk mendapatkan laporan penjualan"""
    try:
        total_transaksi = db.hitung_total_transaksi()
        total_penjualan = db.hitung_total_penjualan()
        rata_rata = total_penjualan / total_transaksi if total_transaksi > 0 else 0
        
        return jsonify({
            "status": "success",
            "data": {
                "total_transaksi": total_transaksi,
                "total_penjualan": total_penjualan,
                "rata_rata_per_transaksi": int(rata_rata)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan: {str(e)}"
        }), 500


# ============ ERROR HANDLING ============

@app.errorhandler(404)
def not_found(error):
    """Handler untuk endpoint yang tidak ditemukan"""
    return jsonify({
        "status": "error",
        "message": "Endpoint tidak ditemukan"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handler untuk error internal server"""
    return jsonify({
        "status": "error",
        "message": "Terjadi kesalahan di server"
    }), 500


# ============ MAIN ============

if __name__ == "__main__":
    # For production (Railway), use host='0.0.0.0' and port from env
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
