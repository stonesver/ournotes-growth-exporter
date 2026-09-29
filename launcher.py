"""Entry point shared by the source distribution and portable Windows build."""
import sys
from pathlib import Path


def main():
    root = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
    sdk = root / 'sdk.xml'
    if not sdk.is_file():
        sdk = root / 'sdk.bhk.xml'
    if '--self-test' in sys.argv:
        from tools.growth_package_check import main as check
        from tools.growth_login import Profile
        if '--require-bundled-sdk' in sys.argv and not (root / 'sdk.bhk.xml').is_file():
            raise SystemExit('Bundled SDK configuration missing')
        return check(profile=Profile.from_resources(sdk) if sdk.is_file() else None)
    from tools.growth_login_local import main as start
    args = sys.argv[1:]
    if sdk.is_file() and '--sdk-resources' not in args:
        args = ['--sdk-resources', str(sdk), *args]
    if '--open-browser' not in args:
        args.append('--open-browser')
    return start(args)


if __name__ == '__main__':
    raise SystemExit(main())
