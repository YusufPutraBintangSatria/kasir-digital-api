"""
Authentication module untuk Kasir Digital API
Menggunakan JWT (JSON Web Token) untuk secure access
"""

import jwt
import json
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

# Secret key untuk encode/decode JWT (GANTI INI DI PRODUCTION!)
SECRET_KEY = "your-secret-key-kasir-digital-2025"

# File untuk menyimpan user
USERS_FILE = "users.json"


class AuthManager:
    """Mengelola authentication dan authorization"""
    
    @staticmethod
    def _load_users():
        """Baca file users.json"""
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def _save_users(users):
        """Simpan users ke file"""
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    
    @staticmethod
    def register(username, password):
        """Register user baru"""
        users = AuthManager._load_users()
        
        # Validasi
        if username in users:
            return {
                "status": "error",
                "message": "Username sudah terdaftar"
            }, 400
        
        if len(password) < 6:
            return {
                "status": "error",
                "message": "Password minimal 6 karakter"
            }, 400
        
        # Simpan user (hash password untuk production!)
        users[username] = {
            "password": password,  # HANYA UNTUK DEMO! Use bcrypt di production
            "created_at": datetime.now().isoformat()
        }
        
        AuthManager._save_users(users)
        
        return {
            "status": "success",
            "message": "User berhasil terdaftar"
        }, 201
    
    @staticmethod
    def login(username, password):
        """Login dan return JWT token"""
        users = AuthManager._load_users()
        
        # Validasi credentials
        if username not in users:
            return {
                "status": "error",
                "message": "Username tidak ditemukan"
            }, 401
        
        if users[username]["password"] != password:
            return {
                "status": "error",
                "message": "Password salah"
            }, 401
        
        # Generate JWT token (valid 24 jam)
        payload = {
            "username": username,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        return {
            "status": "success",
            "message": "Login berhasil",
            "token": token
        }, 200
    
    @staticmethod
    def verify_token(token):
        """Verifikasi JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload, True
        except jwt.ExpiredSignatureError:
            return None, False
        except jwt.InvalidTokenError:
            return None, False


def token_required(f):
    """Decorator untuk protect endpoints yang butuh authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Ambil token dari header
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Format: "Bearer <token>"
            except IndexError:
                return jsonify({
                    "status": "error",
                    "message": "Format token tidak valid. Gunakan: Bearer <token>"
                }), 401
        
        if not token:
            return jsonify({
                "status": "error",
                "message": "Token tidak ditemukan di header Authorization"
            }), 401
        
        # Verify token
        payload, is_valid = AuthManager.verify_token(token)
        
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": "Token tidak valid atau sudah expired"
            }), 401
        
        # Simpan username di request untuk diakses di function
        request.username = payload['username']
        
        return f(*args, **kwargs)
    
    return decorated
