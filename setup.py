from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="pelote",
    version="0.1.2",
    description="Collection of network-related utilities for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/medialab/pelote",
    license="MIT",
    author="Guillaume Plique",
    author_email="guillaume.plique@sciencespo.fr",
    keywords="network",
    python_requires=">=3.6",
    packages=find_packages(exclude=["test"]),
    package_data={"docs": ["README.md"], "pelote": ["*.pyi"]},
    install_requires=["networkx>=2,<3", "typing_extensions"],
    zip_safe=True,
)
