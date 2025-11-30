"""
Menu module untuk UI aplikasi
"""

from datetime import datetime
from config import DAFTAR_PRODUK, DATE_FORMAT
from database import db
from utils import clear_screen, format_rupiah, tampilkan_separator, input_dengan_validasi


class Menu:
    """Mengelola tampilan menu aplikasi"""
    
    @staticmethod
    def tampilkan_header():
        """Tampilkan header aplikasi"""
        clear_screen()
        tampilkan_separator(60)
        print("📱 APLIKASI KASIR DIGITAL TOP-UP 📱".center(60))
        tampilkan_separator(60)
    
    @staticmethod
    def tampilkan_produk():
        """Tampilkan daftar produk"""
        print("\n📦 DAFTAR PRODUK TERSEDIA:")
        tampilkan_separator()
        for kode, info in DAFTAR_PRODUK.items():
            print(f"  {kode:12} | {info['nama']:30} | {format_rupiah(info['harga'])}")
        tampilkan_separator()
    
    @staticmethod
    def tampilkan_menu_utama():
        """Tampilkan menu utama"""
        Menu.tampilkan_header()
        Menu.tampilkan_produk()
        print("\n🎯 PILIH MENU:")
        print("  1. 💳 Transaksi Baru")
        print("  2. 📊 Lihat Riwayat Transaksi")
        print("  3. 📈 Laporan Penjualan")
        print("  4. 🚪 Keluar")
        tampilkan_separator()
    
    @staticmethod
    def tampilkan_laporan():
        """Tampilkan laporan penjualan"""
        Menu.tampilkan_header()
        print("\n📊 LAPORAN PENJUALAN")
        tampilkan_separator()
        
        total_transaksi = db.hitung_total_transaksi()
        total_penjualan = db.hitung_total_penjualan()
        
        print(f"  Total Transaksi  : {total_transaksi} transaksi")
        print(f"  Total Penjualan  : {format_rupiah(total_penjualan)}")
        
        if total_transaksi > 0:
            rata_rata = total_penjualan / total_transaksi
            print(f"  Rata-rata/Item  : {format_rupiah(int(rata_rata))}")
        
        tampilkan_separator()
        input("\n⏎ Tekan Enter untuk kembali ke menu...")
    
    @staticmethod
    def tampilkan_riwayat():
        """Tampilkan riwayat transaksi"""
        Menu.tampilkan_header()
        print("\n📋 RIWAYAT TRANSAKSI")
        tampilkan_separator()
        
        transaksi_list = db.get_semua_transaksi()
        
        if not transaksi_list:
            print("  ℹ️  Belum ada data transaksi")
        else:
            print(f"  {'No':<4} | {'Tanggal':<19} | {'Nama':<15} | {'Produk':<30} | {'Harga':<12}")
            tampilkan_separator()
            
            for i, transaksi in enumerate(transaksi_list, 1):
                print(f"  {i:<4} | {transaksi['tanggal']:<19} | {transaksi['nama']:<15} | {transaksi['produk']:<30} | {format_rupiah(transaksi['harga']):<12}")
        
        tampilkan_separator()
        input("\n⏎ Tekan Enter untuk kembali ke menu...")
