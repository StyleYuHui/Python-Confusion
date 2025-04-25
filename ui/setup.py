import PyInstaller.__main__

PyInstaller.__main__.run([
    'ui/app.py',
    '--name=Python代码混淆器',
    '--windowed',
    '--onefile',
    '--icon=ui/kunkun.ico',
    '--add-data=ui/kunkun.ico;ui',
    '--clean',
    '--noconfirm'
])