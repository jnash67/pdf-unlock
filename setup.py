from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'gui'

executables = [
    Executable('.\PDF-Password-Remover\__main__.py', base=base, target_name = 'prog.exe')
]

setup(name='PDF-Password-Remover',
      version = '1.0',
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
