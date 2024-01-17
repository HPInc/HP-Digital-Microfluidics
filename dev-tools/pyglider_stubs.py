from __future__ import annotations

from argparse import ArgumentParser, Namespace
import os
import subprocess
from subprocess import CompletedProcess
import sys
import logging
import shutil

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    default_module = "pyglider"
    this_dir = os.path.dirname(os.path.abspath(__file__))
    default_stubdir = os.path.join(this_dir, "..", "stubs")
    default_stubdir = os.path.abspath(default_stubdir)
    default_prog = "pybind11-stubgen"
    default_logging = "INFO"
    
    parser = ArgumentParser()
    parser.add_argument('--module', default=default_module,
                        help=f"Module to create stubs for. Default is '{default_module}'.")
    parser.add_argument('--stub-dir', default=default_stubdir,
                        help = f"Stub directory.  Default is '{default_stubdir}")
    parser.add_argument('--prog', default=default_prog,
                        help = f"Stub generator.  Default is {default_prog}")
    parser.add_argument('--search', action='append',
                        help="Directories added to the search for the .pyd file")
    parser.add_argument('--logging', default=default_logging,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help=f"The logging level.  Default is {default_logging}")
    
    args: Namespace = parser.parse_args()
    module: str = args.module
    stubdir: str = args.stub_dir
    prog: str = args.prog
    dirs: list[str] = args.search or []
    log_level: str = args.logging
    
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    logger.addHandler(handler)
    
    var = "PYTHONPATH"
    env = os.environ.copy()
    dirs.append(env.get(var,""))
    env[var] = os.pathsep.join(dirs)
    
    subprocess_args = ['-o', stubdir,
                       '--log-level', log_level,
                       module
                       ]
    process: CompletedProcess = subprocess.run([prog, *subprocess_args], env=env,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               text=True)
    
    sys.stderr.write(process.stderr)
    print(process.stdout, flush=True)
    if process.returncode < 0:
        logger.error(f"{prog} returned with error code {process.returncode}")
        sys.exit(process.returncode)
        
    emitted_dir = os.path.join(stubdir, f"{module}-stubs")
    emitted_pyi = os.path.join(emitted_dir, "__init__.pyi")
    emitted_setup = os.path.join(emitted_dir, "setup.py")
    desired_pyi = os.path.join(stubdir, f"{module}.pyi")
    
    def check_emitted(path: str) -> None:
        if not os.path.exists(path):
            logger.error(f"Directory {path} not emitted")
            sys.exit(-1)
    
    check_emitted(emitted_dir)
    check_emitted(emitted_pyi)        
    if os.path.exists(desired_pyi):
        os.remove(desired_pyi)
    os.rename(emitted_pyi, desired_pyi)
    shutil.rmtree(emitted_dir)
    logger.info(f"Stubs for {module} emitted to {desired_pyi}")

    


