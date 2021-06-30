# -*- mode: python ; coding: utf-8 -*-
import sys
import os
import importlib
sys.setrecursionlimit(5000)

block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\mypy'],
             binaries=[],
             datas=[(os.path.join(os.path.dirname(importlib.import_module('tensorflow').__file__),"lite/experimental/microfrontend/python/ops/_audio_microfrontend_op.so"),"tensorflow/lite/experimental/microfrontend/python/ops/")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
