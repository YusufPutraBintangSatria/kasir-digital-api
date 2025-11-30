"""
Configuration file untuk Aplikasi Kasir Digital
"""

# Database Produk
DAFTAR_PRODUK = {
    "ML_86": {
        "nama": "Mobile Legends 86 Diamond",
        "harga": 20000,
        "kategori": "Game"
    },
    "FF_140": {
        "nama": "Free Fire 140 Diamond",
        "harga": 19000,
        "kategori": "Game"
    },
    "PULSA_20": {
        "nama": "Pulsa All Operator 20rb",
        "harga": 22000,
        "kategori": "Pulsa"
    }
}

# File Configuration
FILE_TRANSAKSI = "transaksi.json"
LOG_FILE = "app.log"

# Format
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
