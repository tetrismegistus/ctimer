# -*- mode: python -*-

block_cipher = None


a = Analysis(['ctimer.py'],
             pathex=['C:\\Users\\amaddux\\AppData\\Local\\Programs\\Python\\Python35-32\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\Users\\amaddux\\Dropbox\\programming\\python\\my utils\\ctimer'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
image_file = [('icon.png', 'C:\\Users\\amaddux\\Dropbox\\programming\\python\\my utils\\ctimer\\icon.png', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ctimer',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas + image_file,
               strip=False,
               upx=True,
               name='ctimer')
