from setuptools import setup, find_packages

setup(
    name='dosuby',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'inquirer',  # Add other dependencies as needed
        'art',
    ],
    entry_points={
        'console_scripts': [
            'dosuby=dosuby.cli:main',  # CLI entry point
        ],
    },
    author='Your Name',
    author_email='deidaxtech@gmail.com',
    description='A tool for enumerating subdomains of a parent domain',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/deidax/dosuby',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)