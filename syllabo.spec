# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Syllabo standalone executable
Optimized to reduce antivirus false positives
"""

import sys
import os
from pathlib import Path

# Get the current directory
current_dir = Path.cwd()

# Define hidden imports for standalone execution
hidden_imports = [
    # Syllabo modules
    'src.ai_client',
    'src.quiz_generator',
    'src.video_analyzer',
    'src.video_analyzer_fast',
    'src.youtube_client',
    'src.setup_manager',
    'src.config_manager',
    
    # Essential third-party dependencies
    'textual',
    'textual.app',
    'textual.widgets',
    'rich',
    'rich.console',
    'rich.table',
    'requests',
    'google.generativeai',
    'googleapiclient',
    'youtube_transcript_api',
    'beautifulsoup4',
    'bs4',
    'dotenv',
    
    # Standard library modules
    'sqlite3',
    'json',
    'pathlib',
    'datetime',
    'urllib.parse',
    'urllib.request',
]

# Data files to include
datas = [
    ('src', 'src'),
]

# Add .env.example if it exists
if (current_dir / '.env.example').exists():
    datas.append(('.env.example', '.'))

# Collect all packages
collect_all = [
    'textual',
    'rich',
    'requests',
    'google',
    'googleapiclient',
    'bs4',
]

# Platform-specific settings
if sys.platform.startswith('win'):
    exe_name = 'syllabo'
    console = True
    icon = None
else:
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
        # Exclude modules that trigger false positives
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
        'wheel',
        'pip',
        'test',
        'unittest',
        'doctest',
        'pdb',
        'profile',
        'pstats',
        'cProfile',
        'trace',
        'timeit',
        'py_compile',
        'compileall',
        'dis',
        'pickletools',
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
    strip=True,
    upx=False,  # Disable UPX compression to reduce false positives
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