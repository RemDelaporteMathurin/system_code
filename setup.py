import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flf_systems_code",
    version="develop",
    author="Rémi Delaporte-Mathurin",
    author_email="",
    description="A systems code for tritium inventory predictions in fusion reactors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RemDelaporteMathurin/system_code",
    packages=setuptools.find_packages(),
    classifiers=[
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # f strings are used which require 3.6 and above
    install_requires=[
        "numpy",
        "matplotlib", # required in examples
        "scipy",
    ],
)
