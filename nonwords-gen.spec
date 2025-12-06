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


from PyInstaller.utils.hooks import collect_submodules, collect_data_files


hidden_imports = collect_submodules("nonwordgen.languages")

# Collect data files for wordfreq (if installed) so its frequency tables
# are available inside the frozen binary for strict dictionary modes.
try:
    wordfreq_datas = collect_data_files("wordfreq")
except Exception:
    wordfreq_datas = []


a = Analysis(
    ["src/nonwordgen/gui.py"],
    pathex=[],
    binaries=[],
    datas=[
        # Ensure the GUI icon image is available at runtime for importlib.resources
        ("src/nonwordgen/assets/nonword-gen.png", "nonwordgen/assets"),
        # Bundle license and third-party notice files alongside the binary
        ("LICENSE", "."),
        ("THIRD_PARTY.md", "."),
        ("README.md", "."),
        ("licenses/wordfreq-LICENSE.txt", "licenses"),
        ("licenses/wordfreq-NOTICE.txt", "licenses"),
    ]
    + wordfreq_datas,
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

