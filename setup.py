import os
from setuptools import setup, find_packages

setup(
    name="pylash",
    version="2.0.0",

    description="A lightweight and relaxed game engine for Python.",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    
    url="https://github.com/yuehaowang/pylash_engine",

    packages=find_packages(),
    install_requires=[
        "PySide2>=5.11"
    ],
    python_requires='>= 3.5'
)