from setuptools import setup

# Setting up
setup(
    name="bus_data_analisys",
    version="0.1.0",
    author="Jakub Szmurło",
    author_email="js438747@students.mimuw.edu.pl",
    description="Analisys for data collected from warsaw public api",
    packages=["bus_data_analisys"],
    install_requires=["requests"],
    setup_requires=["requests"],
    classifiers=[
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
