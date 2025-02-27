#!/usr/bin/env python
"""
Shelf Vision Audit Tool - Main Runner Script
"""

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002) 