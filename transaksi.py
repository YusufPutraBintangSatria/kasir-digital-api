"""
Transaction module untuk mengelola transaksi
"""

from datetime import datetime
from config import DAFTAR_PRODUK, DATE_FORMAT
from database import db
from utils import input_dengan_validasi


class Transaksi:
    """Mengelola proses transaksi"""
    
    @staticmethod
    def proses_transaksi():
        """Proses transaksi baru dengan validasi"""
        print("\n" + "="*50)
        print("💳 FORM TRANSAKSI BARU")
        print("="*50)
        
        # Input nama pembeli dengan validasi
        def validasi_nama(nama):
            return len(nama) > 0
        
        nama = input_dengan_validasi(
            "👤 Nama Pembeli: ",
            validasi_nama
        )
        
        # Loop untuk input kode produk
        while True:
            kode = input("\n📦 Kode Produk (Contoh: ML_86): ").upper().strip()
            
            if kode == "":
                print("❌ Kode produk tidak boleh kosong!")
                continue
            
            if kode in DAFTAR_PRODUK:
                produk = DAFTAR_PRODUK[kode]
                tanggal = datetime.now().strftime(DATE_FORMAT)
                
                # Buat data transaksi
                data_transaksi = {
                    "tanggal": tanggal,
                    "nama": nama,
                    "produk": produk['nama'],
                    "kategori": produk['kategori'],
                    "harga": produk['harga']
                }
                
                # Simpan ke database
                db.tambah_transaksi(data_transaksi)
                
                # Tampilkan struk
                Transaksi._tampilkan_struk(data_transaksi)
                break
            else:
                print(f"❌ Kode produk '{kode}' tidak ditemukan!")
                print("💡 Silakan coba lagi atau ketik 'BATAL' untuk membatalkan\n")
                
                if kode == "BATAL":
                    print("❌ Transaksi dibatalkan.")
                    break
    
    @staticmethod
    def _tampilkan_struk(data_transaksi):
        """Tampilkan struk transaksi"""
        print("\n" + "="*50)
        print("✅ TRANSAKSI BERHASIL".center(50))
        print("="*50)
        print(f"📅 Tanggal     : {data_transaksi['tanggal']}")
        print(f"👤 Pembeli     : {data_transaksi['nama']}")
        print(f"📦 Produk      : {data_transaksi['produk']}")
        print(f"💵 Harga       : Rp{data_transaksi['harga']:,}")
        print("="*50)
        input("\n⏎ Tekan Enter untuk melanjutkan...")
