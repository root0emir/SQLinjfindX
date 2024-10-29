from setuptools import setup, find_packages

setup(
    name="SQLinjFindX",
    version="2.0",
    author="root0emir",
    description="SQL Injection tool with various testing techniques.",
    long_description=open('README.md').read(), 
    long_description_content_type="text/markdown",
    url="http://github.com/root0emir/SQLinjfindX",  
    packages=find_packages(),
    install_requires=[
        'requests',
        'curses',  
    ],
    entry_points={
        'console_scripts': [
            'sqlinjfindx=sqlinjfindx.py:main',  
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
