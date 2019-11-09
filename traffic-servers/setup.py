import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="traffic_servers",
    version="1.0.0",
    author="Vitalii Bursov",
    author_email="vitaly@bursov.com",
    description="Traffic generators for CTF tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vitalyvb/ideal-garbanzo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7, <4',
    install_requires=['scapy'],
    entry_points={
        'console_scripts': [
            'ctfsrv=traffic_servers:ctfsrv.main',
        ],
    },
    setup_requires=[
        'pytest-runner', 'pytest-flake8',
    ],
    tests_require=[
        'pytest', 'flake8',
    ],
)
