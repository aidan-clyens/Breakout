import cx_Freeze

executables = [cx_Freeze.Executable("src/breakout.py", shortcutName="Breakout", shortcutDir="DesktopFolder")]

build_exe_options = {"packages": ["pygame"], "include_files": ["fonts/AtariClassic-Regular.ttf"]}

cx_Freeze.setup(
    name = "Breakout",
    version = "1.0.0",
    options = {"build_exe": build_exe_options},
    description = "Breakout Game",
    executables = executables
)
