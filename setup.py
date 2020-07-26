from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('pdf_gui.py', base=base, targetName = 'splitPDF')
]

setup(name='splitPDF',
      version = '1.0',
      description = 'Divisor de PDFs',
      options = {'build_exe': build_options},
      executables = executables)
