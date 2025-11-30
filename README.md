# 🐍 Aplikasi Kasir Digital Top-Up

Aplikasi desktop untuk mengelola transaksi top-up digital (Game, Pulsa, dll) dengan antarmuka yang user-friendly.

## ✨ Fitur Utama

- ✅ **Transaksi Baru** - Proses transaksi dengan validasi input
- ✅ **Riwayat Transaksi** - Lihat semua histori transaksi dalam format tabel
- ✅ **Laporan Penjualan** - Statistik total penjualan dan rata-rata
- ✅ **Penyimpanan Data** - Database JSON untuk persistensi data
- ✅ **UI Modern** - Antarmuka yang clean dan user-friendly

## 🏗️ Struktur Proyek

```
Proyek_Kasir_Digital/
├── main.py              # Entry point aplikasi
├── config.py            # Konfigurasi dan konstanta
├── database.py          # Manajemen database JSON
├── menu.py              # Tampilan menu UI
├── transaksi.py         # Logika transaksi
├── utils.py             # Fungsi helper
├── transaksi.json       # Database transaksi (auto-generate)
└── README.md            # Dokumentasi
```

## 🚀 Cara Menggunakan

### Prerequisites
- Python 3.7+

### Instalasi
1. Clone atau download project ini
2. Buka terminal di folder project
3. Jalankan program:
   ```bash
   python main.py
   ```

### Menu Aplikasi

1. **💳 Transaksi Baru** - Tambah transaksi baru
2. **📊 Lihat Riwayat** - Lihat semua transaksi
3. **📈 Laporan Penjualan** - Lihat statistik penjualan
4. **🚪 Keluar** - Keluar dari aplikasi

## 💾 Format Data

Data disimpan dalam `transaksi.json`:
```json
[
  {
    "tanggal": "2025-11-30 16:56:50",
    "nama": "Yusuf",
    "produk": "Mobile Legends 86 Diamond",
    "kategori": "Game",
    "harga": 20000
  }
]
```

## 🛠️ Teknologi yang Digunakan

- **Language**: Python 3.7+
- **Storage**: JSON File
- **OOP**: Class-based architecture
- **Architecture**: Modular design dengan separation of concerns

## 📊 Fitur Advanced

- ✅ Input validation dengan feedback yang baik
- ✅ Database management dengan JSON
- ✅ Statistik penjualan real-time
- ✅ Error handling yang robust
- ✅ Clean code dengan dokumentasi lengkap

## 👨‍💻 Author
Yusuf Putra Bintang Satria

## 📝 License
MIT License
