# -*- mode: python -*-

block_cipher = None


a = Analysis(['Index.py'],
             pathex=['..\\venv\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'X:\\Projects\\Python\\FaceIDFinal\\src'],
             binaries=[],
             datas=[('models', 'models'),
                    ('styles\\*.png', 'styles'),
                    ('services\\*.json', 'services'),
                    ('mask\\*.png', 'src\\mask')],
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
          name='launcher',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='styles\\spbstu.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Index')
