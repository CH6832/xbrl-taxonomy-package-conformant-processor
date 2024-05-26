from setuptools import setup, find_packages

setup(
    name='xbrl_tool',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'xbrl_tool=app:main',
        ],
    },
    author='Christoph Hartleb',
    author_email='krystovhar@gmail.com',
    description='A tool for processing XBRL taxonomy packages.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CH6832/xbrl-taxonomy-package-conformant-processor.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL v3 License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
