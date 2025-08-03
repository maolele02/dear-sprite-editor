import logging
import pathlib
import tomllib
from typing import Optional

conf = {}

def load(path):
    global conf
    with open(path, 'rb') as f:
        conf = tomllib.load(f)
        logging.info(f'loaded config: {conf}')

def is_auto_export_clear() -> bool:
    return conf['export']['auto_clear']

def get_output_dir() -> Optional[pathlib.Path]:
    output_dir = conf['export']['output_dir']
    if output_dir:
        return pathlib.Path(output_dir)
    return None