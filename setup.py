from setuptools import setup, find_packages

setup(
    name="VirtualTerminalAtmosphere",
    version="1.0.1",
    author="Joey Soprano 420",
    description="A Virtual Terminal Atmosphere (VTA) for integrating and running various scripts and languages with advanced web crawling and modular plugin architecture.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/YourUsername/YourRepository",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "scrapy>=2.5.0",  # Optional, if using Scrapy for advanced crawling
        "torch>=1.9.0",
        "transformers>=4.9.0",
        "tkinter"  # tkinter is included with standard Python installations
    ],
    entry_points={
        'console_scripts': [
            'vta=vtapp:main',  # This assumes you have a `main` function in `vtapp.py` for running the CLI
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Modified QSRLC License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md'],  # Include additional files in the package
    },
    scripts=[
        'scripts/run_wcpl.py',  # Add any scripts you want to install as executable
        'scripts/run_spinstar.py',
    ],
)
