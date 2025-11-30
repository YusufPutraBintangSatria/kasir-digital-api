"""
Utils module untuk fungsi-fungsi helper
"""

import os


def clear_screen():
    """Clear layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def format_rupiah(nilai):
    """Format nilai ke format Rupiah"""
    return f"Rp{nilai:,}".replace(',', '.')


def tampilkan_separator(panjang=50):
    """Tampilkan separator"""
    print("=" * panjang)


def input_dengan_validasi(prompt, validasi_func=None):
    """Input dengan validasi custom"""
    while True:
        user_input = input(prompt).strip()
        if validasi_func is None or validasi_func(user_input):
            return user_input
        print("❌ Input tidak valid! Silakan coba lagi.\n")
