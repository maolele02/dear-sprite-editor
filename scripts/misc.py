import sys
import config
import pathlib

def get_exe_path() -> pathlib.Path:
    return pathlib.Path(sys.argv[0])

def get_root_dir() -> pathlib.Path:
    return get_exe_path().parent

def get_export_output_dir() -> pathlib.Path:
    output_dir = config.get_output_dir()
    if output_dir:
        return output_dir
    return get_root_dir() / 'output'
