"""
Import products from an Excel price list and write `products.json`.

Expected Excel columns (case-insensitive):
- code (product code, e.g. ML_86)
- nama (product name)
- harga (price, numeric)
- kategori (category string)

Usage:
    pip install pandas openpyxl
    python scripts/import_products_from_xls.py path/to/Daftar_Harga_01_Dec_2025.xls

The script will create `products.json` in the project root. Restart the app to load the new catalog.
"""

import sys
import os
import json
from pathlib import Path

try:
    import pandas as pd
except Exception as e:
    print("Missing dependency: pandas. Install with: pip install pandas openpyxl")
    raise


def normalize_column_name(name):
    return str(name).strip().lower()


def read_excel_to_products(excel_path: Path):
    """Read Excel file and convert to products dict. Supports both .xls and .xlsx formats."""
    file_ext = str(excel_path).lower()
    
    # For .xls files (legacy format), use xlrd engine
    if file_ext.endswith('.xls'):
        engine = 'xlrd'
    # For .xlsx files, use openpyxl engine
    elif file_ext.endswith('.xlsx'):
        engine = 'openpyxl'
    else:
        engine = None
    
    df = pd.read_excel(excel_path, engine=engine)
    # Normalize column names
    df.columns = [normalize_column_name(c) for c in df.columns]

    # Try to detect columns
    possible_code_cols = ['code', 'kode', 'kode_produk', 'product_code']
    possible_name_cols = ['nama', 'name', 'product_name']
    possible_price_cols = ['harga', 'price', 'harga_rp']
    possible_cat_cols = ['kategori', 'category']

    def find_col(possibles):
        for p in possibles:
            if p in df.columns:
                return p
        return None

    code_col = find_col(possible_code_cols)
    name_col = find_col(possible_name_cols)
    price_col = find_col(possible_price_cols)
    cat_col = find_col(possible_cat_cols)

    if not code_col or not name_col or not price_col:
        raise ValueError(f"Required columns not found. Found columns: {list(df.columns)}")

    products = {}
    for _, row in df.iterrows():
        code = str(row[code_col]).strip()
        if not code or code.lower() == 'nan':
            continue
        name = str(row[name_col]).strip()
        # price normalization
        try:
            harga = int(float(row[price_col]))
        except Exception:
            # try removing non-digits
            harga_str = str(row[price_col])
            digits = ''.join(ch for ch in harga_str if ch.isdigit())
            harga = int(digits) if digits else 0

        kategori = str(row[cat_col]).strip() if cat_col and row[cat_col] and str(row[cat_col]).strip().lower() != 'nan' else 'Lainnya'

        products[code] = {
            'nama': name,
            'harga': harga,
            'kategori': kategori
        }

    return products


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_products_from_xls.py path/to/Daftar_Harga.xls")
        sys.exit(1)

    excel_path = Path(sys.argv[1])
    if not excel_path.exists():
        print(f"File not found: {excel_path}")
        sys.exit(2)

    try:
        products = read_excel_to_products(excel_path)
    except Exception as e:
        print("Failed to parse Excel:", e)
        sys.exit(3)

    out_path = Path(os.getcwd()) / 'products.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(products)} products to {out_path}")
