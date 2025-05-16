from setuptools import setup, find_packages


setup(
    name="picflow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python"
    ],
    author="<NAME>",
    desciption="Picflow Python package",
    long_description=open("README.md").read(),
    #url = ,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "picflow = picflow.main:main"
        ]
    }
)
