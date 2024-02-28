from setuptools import setup

# Setting up
setup(
    name="warsaw-bus-api",
    version="0.1.0",
    author="Jakub Szmurło",
    author_email="js438747@students.mimuw.edu.pl",
    description="Python wrap for warsaw public api",
    packages=["warsaw_bus_api"],
    install_requires=["requests"],
    setup_requires=["requests"],
    classifiers=[
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": [
            "warsaw-data-api=warsaw_data_api:main",
        ]
    },
)
