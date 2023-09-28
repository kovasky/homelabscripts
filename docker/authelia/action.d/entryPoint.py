#!/usr/bin/python3

import os
import sys

if len(sys.argv) < 3:
    print("Usage: ./entryPoint.py <ip> <add|del>")
    sys.exit(1)

venv_dir = 'env'

if not os.path.exists(venv_dir):
    os.system(f"{sys.executable} -m venv {venv_dir}")

activate_script = os.path.join(venv_dir, 'bin', 'activate')
os.system(f"chmod +x {activate_script}")
os.system(f"{os.path.join(venv_dir, 'bin', 'pip')} install --upgrade requests ipaddress")

os.system(f"{os.path.join(venv_dir, 'bin', 'python')} /data/action.d/modifyBanList.py {sys.argv[1]} {sys.argv[2]}")
