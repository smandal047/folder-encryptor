from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["cx-Freeze", "unittest"],
    "zip_include_packages": ["PyQt5.QtWidgets","PyQt5.QtGui","PyQt5.QtCore","cryptography.fernet"],
    "bin_path_includes": ["bin"]
}


setup(
    name="Encryptor",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": build_exe_options},
    executables=[Executable("gui.py", base="Win32GUI")],
)