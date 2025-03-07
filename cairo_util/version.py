"""Return a version number extracted from the git history, in a form suitable
for PEP 440."""

import subprocess

def version_from_git():
    """Query git and return a version string.  This is mostly just `git
    describe`, but without the hash junk it sometimes includes."""
    try:
        version = subprocess.check_output(['git', 'describe', '--tags', '--match', 'v[0-9]*'],
                                          stderr=subprocess.STDOUT)
        version = version.strip().decode('utf-8')
    except subprocess.CalledProcessError as cpe:
        output = cpe.output.decode('utf-8')
        if 'fatal: No names found, cannot describe anything.' in output:
            print('No tags found.  Defaulting to v0.0.')
            version = 'v0.0'
        else:
            raise

    if '-' in version:
        parts = version.split('-')
        version = f"{parts[0][1:]}.dev{parts[1]}"
    else:
        version = version[1:]
    return version

if __name__ == '__main__':
    print(version_from_git())

