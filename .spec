# socem25.spec

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

project_dir = Path(__file__).parent.resolve()
main_script = str(project_dir / "src" / "socem25" / "main.py")

# Gather all hidden imports from your package
hidden_imports = collect_submodules("socem25")

a = Analysis(
    [main_script],
    pathex=[str(project_dir / "src")],
    hiddenimports=hidden_imports,
    binaries=[],
    datas=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="socem25",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # set to False if you want to hide the terminal window (for GUI)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="socem25",
)
