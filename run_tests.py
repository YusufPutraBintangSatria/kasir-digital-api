#!/usr/bin/env python
"""
Script untuk menjalankan tests
"""

import subprocess
import sys

if __name__ == '__main__':
    # Run pytest
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/test_api.py', '-v', '--tb=short'],
        cwd='.'
    )
    sys.exit(result.returncode)
