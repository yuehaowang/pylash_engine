import os
from setuptools import setup, find_packages

setup(
    name="pylash_engine",
    version="2.0.0a1",

    author="Yuehao Wang",
    author_email="wangyuehao1999@gmail.com",
    license="MIT",
    description="A lightweight and relaxed game engine for Python.",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    
    url="https://github.com/yuehaowang/pylash_engine",

    packages=find_packages(),
    install_requires=[
        "PySide2>=5.11"
    ],
    python_requires='>= 3.5, <3.9',

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",

        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",

        "License :: OSI Approved :: MIT License",

        "Intended Audience :: Developers",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video"
    ]
)