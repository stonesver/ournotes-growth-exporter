"""Entry point shared by the source distribution and portable Windows build."""
import sys
from pathlib import Path


def main():
    if '--self-test' in sys.argv:
        from tools.growth_package_check import main as check
        return check()
    from tools.growth_login_local import main as start
    args = sys.argv[1:]
    root = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
    sdk = root / 'sdk.xml'
    if sdk.is_file() and '--sdk-resources' not in args:
        args = ['--sdk-resources', str(sdk), *args]
    if '--open-browser' not in args:
        args.append('--open-browser')
    return start(args)


if __name__ == '__main__':
    raise SystemExit(main())
