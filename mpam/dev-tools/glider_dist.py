from __future__ import annotations
import zipfile
from argparse import ArgumentParser, Namespace
from typing import Final
from erk.config import ConfigParam
import logging
import os
import re
import sys
from erk.basic import ValOrFn, ensure_val

logger = logging.getLogger(__name__)

dll_files = [ 
    "WallabyHAL.dll",
    "pyglider.pyd",
    "SDL2.dll",
    "SDL2_ttf.dll",
    "libfreetype-6.dll",
    "zlib1.dll"
    ]

config_files = [
    "SensorConfig_ESElog.json",
    "WallabyElectrodes.csv",
    "WallabyElectrodes15.csv",
    "WallabyHeaters.csv",
    "WallabyHeaters15.csv",
    "WallabyMagnets.csv",
    "WallabyMagnets15.csv",
    "WallabyThermalStates15.csv"
    ]

class Config:
    zip_file: Final = ConfigParam[str]("glider.zip")
    output_dir: Final = ConfigParam[str](".")
    build_root: Final = ConfigParam[str](".")
    dll_dir: Final = ConfigParam[str]("x64/Debug")
    config_dir: Final = ConfigParam[str]("WallabyHAL")
    python_root: Final = ConfigParam[str]()
    python_dll: Final = ConfigParam[str]("python310.dll")
    

def create_zip(files: list[str], archive_name: str) -> None:
    logger.info(f"Writing to {archive_name}.")
    with zipfile.ZipFile(archive_name, 'w') as zipf:
        for file in files:
            if os.path.isfile(file):
                _,f = os.path.split(file)
                logger.info(f"Adding {file}")
                zipf.write(file, arcname=f)
            else:
                logger.warning(f"{file} does not exist or is not a file, ignoring.")
            
def is_relative_to_dir(path: str) -> bool:
    # For Unix and Windows
    if os.path.isabs(path):
        return False

    # Checking if the path starts with `.` or `..` followed by directory separator or end of string.
    if re.match(r'^\.\.?(\\|/|$)', path):
        return False

    # For Windows
    if os.name == 'nt' and path.startswith('\\'):
        return False

    return True

def ensure_relative_to_dir(dir_path: ValOrFn[str], path: str) -> str:
    if is_relative_to_dir(path):
        return os.path.join(ensure_val(dir_path,str), path)
    return path            
            
if __name__ == '__main__':
    parser = ArgumentParser(description="Package Glider (HAL) files for distribution")
    Config.zip_file.add_arg_to(parser, "-o", "--output", metavar="FILE",
                               help='''
                               The ZIP file to write.  Relative to the output directory (--dir).
                               ''')
    Config.output_dir.add_arg_to(parser, "-d", "--dir", metavar="DIR",
                                 default_desc = lambda d: "the current directory" if d == "." else d,
                                 help = '''
                                 The directory in which to store the zip file.
                                 ''')
    Config.build_root.add_arg_to(parser, "--root", metavar="DIR",
                                 default_desc = lambda d: "the current directory" if d == "." else d,
                                 help = '''
                                 The root of the build directory.
                                 ''')
    Config.dll_dir.add_arg_to(parser, "--dll-dir", metavar="DIR",
                              help = '''
                              The directory in which the .dll and .pyd files are found.  Relative to the
                              root directory (--root).
                              ''')
    Config.config_dir.add_arg_to(parser, "--config-dir", metavar="DIR",
                                 help = '''
                                  The directory in which the configuration files are found.  Relative to the
                                  root directory (--root).
                                  ''')
    Config.python_root.add_arg_to(parser, "--python-root", metavar="DIR",
                                 help = '''
                                  The root directory of the Python distribution.
                                  ''')
    Config.python_dll.add_arg_to(parser, "--python-dll", metavar="FILE",
                                 help = '''
                                  The Python DLL.  Relative to --python-root.
                                  ''')
    
    ns: Namespace = parser.parse_args()
    ConfigParam.set_namespace(ns)
    
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    zipf = os.path.realpath(ensure_relative_to_dir(Config.output_dir(), 
                                                   Config.zip_file()))
    
    root = Config.build_root()
    dll_dir = os.path.realpath(ensure_relative_to_dir(root, Config.dll_dir()))
    if not os.path.isdir(dll_dir):
        logger.critical(f"DLL dir {dll_dir} doesn't exist or is not a directory.")
        sys.exit(-1)
    logger.info(f"DLL dir: {dll_dir}")

    config_dir = os.path.realpath(ensure_relative_to_dir(root, Config.config_dir()))
    if not os.path.isdir(config_dir):
        logger.critical(f"Config dir {config_dir} doesn't exist or is not a directory.")
        sys.exit(-1)
    logger.info(f"Config dir: {config_dir}")
    
    python_dll = os.path.realpath(ensure_relative_to_dir(lambda: Config.python_root(), 
                                                         Config.python_dll()))
    
    files = [*(os.path.join(dll_dir, f) for f in dll_files),
             *(os.path.join(config_dir, f) for f in config_files),
             python_dll]
    
    create_zip(files, zipf)
    