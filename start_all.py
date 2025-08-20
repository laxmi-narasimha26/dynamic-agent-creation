import subprocess
import sys
import time
import threading
import os
import shutil
import argparse
import urllib.request
import urllib.error

def command_exists(command: str) -> bool:
    return shutil.which(command) is not None

def free_ports():
    """Run kill_ports.ps1 to free commonly used ports."""
    script = os.path.join(os.path.dirname(__file__), 'kill_ports.ps1')
    if not os.path.exists(script):
        return
    try:
        subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-File', script, '-KillDevProcesses'],
            check=False,
        )
    except Exception:
        pass

def remove_frontend_build():
    path = os.path.join('frontend', '.next')
    try:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
    except Exception:
        pass

def backend_python_exe() -> str:
    """Prefer backend/.venv if present, else current python."""
    venv_py = os.path.join('backend', '.venv', 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join('backend', '.venv', 'bin', 'python')
    if os.path.exists(venv_py):
        return venv_py
    # Fallback to 'venv' if exists
    venv2_py = os.path.join('backend', 'venv', 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join('backend', 'venv', 'bin', 'python')
    if os.path.exists(venv2_py):
        return venv2_py
    return sys.executable

def ensure_backend_env_and_deps(no_install: bool = False) -> None:
    """Create venv if missing and install requirements."""
    if no_install:
        return
    py = backend_python_exe()
    # Create venv if not present
    if py == sys.executable:
        # Check if any venv exists; if not, create backend/.venv
        target = os.path.join('backend', '.venv')
        if not os.path.exists(target):
            try:
                subprocess.run([sys.executable, '-m', 'venv', target], cwd='backend', check=True)
            except subprocess.CalledProcessError:
                # Fall back to system python
                pass
        # Refresh chosen interpreter
        py2 = backend_python_exe()
        if os.path.exists(py2):
            py = py2
    # Install deps if requirements.txt exists
    req = os.path.join('backend', 'requirements.txt')
    if os.path.exists(req):
        try:
            subprocess.run([py, '-m', 'pip', 'install', '-r', 'requirements.txt'], cwd='backend', check=False)
        except Exception:
            pass

# Function to start backend server
def start_backend() -> subprocess.Popen | None:
    try:
        py = backend_python_exe()
        env = os.environ.copy()
        # Ensure dotenv will be found; FastAPI app already loads it
        proc = subprocess.Popen(
            [py, '-m', 'uvicorn', 'main:app', '--reload', '--host', '127.0.0.1', '--port', '8000'],
            cwd='backend',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
            shell=False,
        )
        return proc
    except Exception as e:
        print(f"Error starting backend: {e}")
        return None

# Function to start frontend server
def ensure_frontend_deps(no_install: bool = False) -> None:
    if no_install:
        return
    if not command_exists('npm'):
        print('Error: npm is not installed or not in PATH. Please install Node.js and npm.')
        return
    try:
        lockfile = os.path.join('frontend', 'package-lock.json')
        cmd = 'npm ci' if os.path.exists(lockfile) else 'npm install'
        subprocess.run(cmd, cwd='frontend', shell=True, check=False)
    except Exception:
        pass

def start_frontend() -> subprocess.Popen | None:
    if not command_exists('npm'):
        print('Error: npm is not installed or not in PATH. Please install Node.js and npm.')
        return None
    try:
        proc = subprocess.Popen(
            'npm run dev',
            cwd='frontend',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True,
        )
        return proc
    except Exception as e:
        print(f"Error starting frontend: {e}")
        return None

def wait_for_url(url: str, timeout: int = 60) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                if r.status == 200:
                    return True
        except urllib.error.URLError:
            pass
        except Exception:
            pass
        time.sleep(1)
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start backend and frontend together (fresh).')
    parser.add_argument('--clean', action='store_true', help='Clean frontend .next build before starting')
    parser.add_argument('--no-install', action='store_true', help='Skip dependency installation (npm/pip)')
    parser.add_argument('--skip-ports', action='store_true', help='Skip freeing dev ports')
    parser.add_argument('--backend-only', action='store_true', help='Start backend only')
    parser.add_argument('--frontend-only', action='store_true', help='Start frontend only')
    args = parser.parse_args()

    if not os.path.exists('backend'):
        print('Error: Backend directory not found.')
        sys.exit(1)
    if not os.path.exists('frontend'):
        print('Error: Frontend directory not found.')
        sys.exit(1)

    if not args.skip_ports:
        free_ports()
        time.sleep(1)

    if args.clean:
        remove_frontend_build()

    # Ensure deps
    if not args.no_install:
        print('Installing backend requirements...')
    ensure_backend_env_and_deps(no_install=args.no_install)
    if not args.no_install:
        print('Installing frontend dependencies...')
    ensure_frontend_deps(no_install=args.no_install)

    backend_proc = None
    frontend_proc = None

    if not args.frontend_only:
        print('Starting backend...')
        backend_proc = start_backend()

    if not args.backend_only:
        print('Starting frontend...')
        frontend_proc = start_frontend()

    if (args.backend_only and backend_proc) or (args.frontend_only and frontend_proc) or (backend_proc and frontend_proc):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            try:
                if backend_proc: backend_proc.terminate()
            except Exception:
                pass
            try:
                if frontend_proc: frontend_proc.terminate()
            except Exception:
                pass
    else:
        print('Failed to start required services.')
