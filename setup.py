import setuptools

setuptools.setup(
    name="FollowerBot",
    version="0.0.2",
    author="Hattyot",
    description="A robot simulator",
    url="https://github.com/Hattyot/FollowerBot",
    project_urls={
        "Bug Tracker": "https://github.com/Hattyot/FollowerBot/issues"
    },
    package_dir={"": "src"},
    install_requires=[
         'Pillow==9.3.0'
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
