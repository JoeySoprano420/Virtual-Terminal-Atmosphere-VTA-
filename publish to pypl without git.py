import os
import subprocess

def build_and_upload():
    os.system('python setup.py sdist bdist_wheel')
    subprocess.run([
        'twine', 'upload', 'dist/*',
        '--username', '__token__',
        '--password', os.getenv('PYPI_TOKEN')
    ])

if __name__ == '__main__':
    build_and_upload()
