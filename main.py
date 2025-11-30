"""
Aplikasi Kasir Digital - Main Entry Point
Aplikasi untuk mengelola transaksi top-up digital
"""

from menu import Menu
from transaksi import Transaksi


def main():
    """Main program loop"""
    while True:
        Menu.tampilkan_menu_utama()
        
        pilihan = input("🎯 Pilih menu (1-4): ").strip()
        
        if pilihan == "1":
            Transaksi.proses_transaksi()
        elif pilihan == "2":
            Menu.tampilkan_riwayat()
        elif pilihan == "3":
            Menu.tampilkan_laporan()
        elif pilihan == "4":
            print("\n👋 Terima Kasih telah menggunakan Aplikasi Kasir Digital!")
            print("Sampai Jumpa Lagi! 😊\n")
            break
        else:
            input("❌ Pilihan tidak valid! Tekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    main()
   
