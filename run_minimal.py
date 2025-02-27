#!/usr/bin/env python
"""
Shelf Vision Audit Tool - Minimal Runner Script
"""

from app_minimal import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 