from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='dosuby',
    use_scm_version=True,  # Simplified configuration - details in pyproject.toml
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'dosuby=dosuby.cli:main',  # CLI entry point
        ],
    },
    author='deidax',
    author_email='deidaxtech@gmail.com',
    description='A tool for enumerating subdomains of a parent domain',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/deidax/dosuby',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    python_requires='>=3.10',
    keywords='subdomain enumeration security network',
    license='MIT',
)