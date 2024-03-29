from setuptools import find_namespace_packages, setup

with open("README.md") as f:
    readme = f.read()

with open("requirements/production.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="opulence.collectors",
    version="1.0.0",
    description="Collectors service",
    long_description=readme,
    author="Opulence",
    author_email="contact@opulence.fr",
    url="https://github.com/opullence/collectors",
    license=license,
    packages=find_namespace_packages(include=["opulence.*"]),
    entry_points={
        "console_scripts": [
            "opulence-collectors=opulence.collectors.__main__:main",
            "opulence-try_collector=opulence.collectors.scripts.test_collector:main",
        ]
    },
    install_requires=requirements,
    python_requires=">=3.6.*, <4",
)
