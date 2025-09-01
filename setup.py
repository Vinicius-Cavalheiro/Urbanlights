from cx_Freeze import setup, Executable
import os

path = "./assets"
asset_list = os.listdir(path)
asset_list_completa = [os.path.join(path, asset) for asset in asset_list]

executables = [Executable("main.py")]

build_options = {
    "packages": ["pygame"],
    "include_files": asset_list_completa
}

setup(
    name="Urbanlights",
    version="0.2",
    description="Urban lights app",
    options={"build_exe": build_options},
    executables=executables
)
