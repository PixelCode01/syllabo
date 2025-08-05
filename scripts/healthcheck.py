#!/usr/bin/env python3
"""
Health check script for Docker container
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from src.database import SyllaboDatabase
    from src.logger import SyllaboLogger
    
    # Test database connection
    db = SyllaboDatabase()
    
    # Test logger
    logger = SyllaboLogger("healthcheck")
    logger.info("Health check passed")
    
    print("Health check: OK")
    sys.exit(0)
    
except Exception as e:
    print(f"Health check failed: {e}")
    sys.exit(1)