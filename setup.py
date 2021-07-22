# #!/usr/bin/env python
"""The setup script."""
from setuptools import setup, find_packages

setup(
    zip_safe=False,
    setup_requires=['pytest-runner',],
    install_requires=['requests','beautifulsoup4','click',],
    python_requires='>=3',
    tests_require=['pytest>=3',],
    include_package_data=True,
    packages=find_packages(include=['deep_translator'],),
    entry_points={'console_scripts':[
        'deep-translator=deep_translator.__main__:cli',
        'dt=deep_translator.__main__:cli',
    ],},
)
