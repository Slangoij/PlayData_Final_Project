# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['webcam_ij.py'],
             pathex=['E:\\Users\\inje\\교육\\202012_국비지원 IT교육\\Final_Project\\Pyinstaller_toEXE'],
             binaries=[],
             datas=[('./common', './common'),
                    ('./model', './model'),
                    ('./src', './src'),
            ],
             hiddenimports=["common.draw",
                            "common.HandTrackingModule",
                            "src.test.Demo_ij",
                            "src.user_interface.AutopyClass",
                            "src.user_interface.GestureModelModule",
                            ],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='DryHand',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='orange_logo.ico')
