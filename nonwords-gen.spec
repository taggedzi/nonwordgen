# PyInstaller spec file for building the nonwordgen GUI as a
# standalone Windows executable named "nonwords-gen.exe".
#
# Usage (from the project root, on Windows):
#   py -m PyInstaller nonwords-gen.spec
#
# This assumes:
#   - PyInstaller is installed in your environment
#   - PyQt6 is installed (the "gui" extra)
#   - You have created an ICO file at assets/nonword-gen.ico

block_cipher = None


from PyInstaller.utils.hooks import collect_submodules


hidden_imports = collect_submodules("nonwordgen.languages")


a = Analysis(
    ["run_gui.py"],
    pathex=[],
    binaries=[],
    datas=[
        # Ensure the GUI icon image is available at runtime for importlib.resources
        ("nonwordgen/assets/nonword-gen.png", "nonwordgen/assets"),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="nonwords-gen",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/nonword-gen.ico",
)

