# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Syllabo standalone executable
This ensures all dependencies are properly bundled
"""

import sys
import os
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define all hidden imports for standalone execution
hidden_imports = [
    # Syllabo modules
    'src.database',
    'src.logger', 
    'src.ai_client',
    'src.syllabus_parser',
    'src.quiz_generator',
    'src.progress_dashboard',
    'src.goals_manager',
    'src.platform_integrator',
    'src.bookmark_manager',
    'src.study_session_manager',
    'src.spaced_repetition',
    'src.notes_generator',
    'src.video_analyzer',
    'src.resource_finder',
    'src.youtube_client',
    
    # Third-party dependencies
    'textual',
    'textual.app',
    'textual.widgets',
    'textual.containers',
    'textual.screen',
    'textual.binding',
    'textual.reactive',
    'rich',
    'rich.console',
    'rich.table',
    'rich.panel',
    'rich.text',
    'rich.prompt',
    'rich.progress',
    'rich.rule',
    'rich.align',
    'requests',
    'requests.adapters',
    'requests.auth',
    'requests.cookies',
    'requests.exceptions',
    'requests.models',
    'requests.sessions',
    'requests.utils',
    'PyPDF2',
    'PyPDF2.pdf',
    'beautifulsoup4',
    'bs4',
    'feedparser',
    'google.generativeai',
    'google.api_core',
    'google.auth',
    'googleapiclient',
    'googleapiclient.discovery',
    'googleapiclient.errors',
    'youtube_transcript_api',
    'dotenv',
    
    # Standard library modules that might not be auto-detected
    'sqlite3',
    'json',
    'asyncio',
    'asyncio.events',
    'asyncio.futures',
    'asyncio.tasks',
    'typing',
    'pathlib',
    'datetime',
    'time',
    're',
    'urllib',
    'urllib.parse',
    'urllib.request',
    'urllib.error',
    'http',
    'http.client',
    'ssl',
    'socket',
    'threading',
    'multiprocessing',
    'logging',
    'logging.handlers',
    'csv',
    'xml',
    'xml.etree',
    'xml.etree.ElementTree',
    'html',
    'html.parser',
    'email',
    'email.mime',
    'email.utils',
    'base64',
    'hashlib',
    'hmac',
    'uuid',
    'tempfile',
    'shutil',
    'zipfile',
    'tarfile',
    'gzip',
    'platform',
    'subprocess',
    'signal',
    'atexit',
    'weakref',
    'collections',
    'collections.abc',
    'itertools',
    'functools',
    'operator',
    'copy',
    'pickle',
    'io',
    'contextlib',
    'warnings',
    'traceback',
    'inspect',
    'types',
    'enum',
    'dataclasses',
    
    # SSL and certificate handling
    'certifi',
    'charset_normalizer',
    'idna',
    'urllib3',
    'urllib3.util',
    'urllib3.exceptions',
    'urllib3.poolmanager',
    
    # Additional dependencies
    'six',
    'packaging',
    'packaging.version',
    'pyparsing',
]

# Data files to include
datas = [
    ('src', 'src'),  # Include all source files
]

# Add .env.example if it exists
if (current_dir / '.env.example').exists():
    datas.append(('.env.example', '.'))

# Add LICENSE if it exists
if (current_dir / 'LICENSE').exists():
    datas.append(('LICENSE', '.'))

# Collect all packages that need their submodules
collect_all = [
    'textual',
    'rich', 
    'requests',
    'google',
    'googleapiclient',
    'PyPDF2',
    'bs4',
    'feedparser',
    'youtube_transcript_api',
    'certifi',
    'urllib3',
]

# Platform-specific settings
if sys.platform.startswith('win'):
    exe_name = 'syllabo.exe'
    console = True
    icon = 'assets/icon.ico' if (current_dir / 'assets' / 'icon.ico').exists() else None
elif sys.platform.startswith('darwin'):
    exe_name = 'syllabo'
    console = True
    icon = 'assets/icon.icns' if (current_dir / 'assets' / 'icon.icns').exists() else None
else:  # Linux and other Unix
    exe_name = 'syllabo'
    console = True
    icon = None

# Analysis phase
a = Analysis(
    ['main.py'],
    pathex=[str(current_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'torch',
        'tensorflow',
        'jupyter',
        'IPython',
        'notebook',
        'pytest',
        'setuptools',
        'distutils',
        'wheel',
        'pip',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove duplicate entries
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip debug symbols for smaller size
    upx=False,   # Don't use UPX compression for better compatibility
    upx_exclude=[],
    runtime_tmpdir=None,
    console=console,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)