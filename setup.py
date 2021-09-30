import setuptools

setuptools.setup(
    name="PiBot",
    version="0.0.1",
    author="Hattyot",
    description="A robot simulator",
    url="https://github.com/Hattyot/PiBot",
    project_urls={
        "Bug Tracker": "https://github.com/Hattyot/PiBot/issues"
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)