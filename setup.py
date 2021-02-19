#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


# with open('./re') as reqs:
#     requirements = reqs.read()
# print(requirements)
# exit()
setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Nidhal Baccouri",
    author_email='nidhalbacc@gmail.com',
    maintainer="Nidhal Baccouri",
    maintainer_email='nidhalbacc@gmail.com',
    python_requires='>=3.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: Communications',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A flexible python tool to translate between different languages in a simple way.",
    entry_points={
        'console_scripts': [
            'deep_translator=deep_translator.cli:main',
        ],
    },
    install_requires=['requests', 'beautifulsoup4'],
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['deep_translator',
              'deepL', 'DeepL',
              'translator',
              'translation',
              'automation',
              'web scraping',
              'google translator', 'google translation', 'google trans',
              'PONS', 'YANDEX', 'MyMemory translator', 'Linguee', 'QCRI',
              'Language', 'Language detection', 'detect language',
              'free translation', 'unlimited translation', 'translate for free'],
    name='deep_translator',
    packages=find_packages(include=['deep_translator']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nidhaloff/deep_translator',
    version='1.3.5',
    zip_safe=False,
)
