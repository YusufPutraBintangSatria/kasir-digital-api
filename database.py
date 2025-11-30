"""
Database module untuk mengelola data transaksi
Menggunakan JSON sebagai penyimpanan data
"""

import json
import os
from datetime import datetime
from config import FILE_TRANSAKSI, DATE_FORMAT


class Database:
    """Mengelola operasi database transaksi"""
    
    def __init__(self, filename=FILE_TRANSAKSI):
        self.filename = filename
        self._init_database()
    
    def _init_database(self):
        """Inisialisasi file database jika belum ada"""
        if not os.path.exists(self.filename):
            self._write([])
    
    def _read(self):
        """Baca semua transaksi dari file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write(self, data):
        """Simpan transaksi ke file"""
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def tambah_transaksi(self, transaksi):
        """Tambahkan transaksi baru"""
        data = self._read()
        data.append(transaksi)
        self._write(data)
    
    def get_semua_transaksi(self):
        """Ambil semua transaksi"""
        return self._read()
    
    def get_transaksi_by_nama(self, nama):
        """Ambil transaksi berdasarkan nama pembeli"""
        data = self._read()
        return [t for t in data if t['nama'].lower() == nama.lower()]
    
    def hitung_total_penjualan(self):
        """Hitung total penjualan"""
        data = self._read()
        return sum(t['harga'] for t in data)
    
    def hitung_total_transaksi(self):
        """Hitung jumlah transaksi"""
        return len(self._read())


# Singleton instance
db = Database()
