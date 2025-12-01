"""
Configuration file untuk Aplikasi Kasir Digital
"""

# Database Produk (expanded catalog)
DAFTAR_PRODUK = {
    # Game Top-up
    "ML_86": {"nama": "Mobile Legends 86 Diamond", "harga": 20000, "kategori": "Game"},
    "ML_150": {"nama": "Mobile Legends 150 Diamond", "harga": 35000, "kategori": "Game"},
    "FF_140": {"nama": "Free Fire 140 Diamond", "harga": 19000, "kategori": "Game"},
    "FF_355": {"nama": "Free Fire 355 Diamond", "harga": 45000, "kategori": "Game"},
    "PUBG_70": {"nama": "PUBG UC 70", "harga": 25000, "kategori": "Game"},
    "COD_300": {"nama": "Call of Duty CP 300", "harga": 30000, "kategori": "Game"},

    # Pulsa (All Operator)
    "PULSA_5": {"nama": "Pulsa All Operator 5.000", "harga": 5500, "kategori": "Pulsa"},
    "PULSA_10": {"nama": "Pulsa All Operator 10.000", "harga": 11500, "kategori": "Pulsa"},
    "PULSA_20": {"nama": "Pulsa All Operator 20.000", "harga": 22000, "kategori": "Pulsa"},
    "PULSA_50": {"nama": "Pulsa All Operator 50.000", "harga": 52500, "kategori": "Pulsa"},

    # Paket Data (by quota)
    "DATA_1GB": {"nama": "Kuota 1GB (24 jam)", "harga": 8000, "kategori": "Data"},
    "DATA_3GB": {"nama": "Kuota 3GB (7 hari)", "harga": 15000, "kategori": "Data"},
    "DATA_5GB": {"nama": "Kuota 5GB (30 hari)", "harga": 30000, "kategori": "Data"},
    "DATA_10GB": {"nama": "Kuota 10GB (30 hari)", "harga": 55000, "kategori": "Data"},

    # E-Money Top-up
    "OVO_100": {"nama": "OVO Balance 100.000", "harga": 102000, "kategori": "E-Money"},
    "GOPAY_50": {"nama": "GoPay Balance 50.000", "harga": 51500, "kategori": "E-Money"},
    "DANA_25": {"nama": "Dana Balance 25.000", "harga": 26000, "kategori": "E-Money"},

    # PLN Prepaid (Token)
    "PLN_20": {"nama": "Token PLN 20.000", "harga": 21500, "kategori": "PLN"},
    "PLN_50": {"nama": "Token PLN 50.000", "harga": 52000, "kategori": "PLN"},
    "PLN_100": {"nama": "Token PLN 100.000", "harga": 102000, "kategori": "PLN"},

    # Voucher & Subscription
    "STEAM_20": {"nama": "Steam Wallet 20 USD", "harga": 300000, "kategori": "Voucher"},
    "GP_100": {"nama": "Google Play 100.000", "harga": 102000, "kategori": "Voucher"},
    "SPOTIFY_1M": {"nama": "Spotify Premium 1 Month", "harga": 49000, "kategori": "Subscription"},
    "NETFLIX_1M": {"nama": "Netflix 1 Month (Basic)", "harga": 55000, "kategori": "Subscription"},

    # Digital Services (Top-ups kecil dan promo)
    "TELKOM_10": {"nama": "Telkom Voucher 10.000", "harga": 11000, "kategori": "Voucher"},
    "GAMEPLAY_30": {"nama": "In-Game Currency Small Pack", "harga": 12000, "kategori": "Game"},

    # Misc small denominations
    "PULSA_2": {"nama": "Pulsa All Operator 2.500", "harga": 3000, "kategori": "Pulsa"},
    "DATA_0_5GB": {"nama": "Kuota 500MB (1 hari)", "harga": 5000, "kategori": "Data"},
    "EMONEY_10": {"nama": "E-Money 10.000", "harga": 10500, "kategori": "E-Money"}
}

# If there's a products.json file in project root (created from Excel import),
# load it and override the hard-coded `DAFTAR_PRODUK` so the app uses the latest catalog.
try:
    import json
    from pathlib import Path
    p = Path(__file__).resolve().parent / 'products.json'
    if p.exists():
        with p.open('r', encoding='utf-8') as fh:
            data = json.load(fh)
            # validate simple structure: code -> {nama,harga,kategori}
            if isinstance(data, dict) and data:
                DAFTAR_PRODUK = data
except Exception:
    # If any error occurs while loading external catalog, keep built-in catalog.
    pass

# File Configuration
FILE_TRANSAKSI = "transaksi.json"
LOG_FILE = "app.log"

# Format
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
