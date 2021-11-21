import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kyuutils",
    version="0.0.1",
    author="kyuunin",
    author_email="cneumann@students.uni-mainz.de",
    description="Some Utils for my projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyuunin/kyuutils",
    project_urls={
        "Bug Tracker": "https://github.com/kyuunin/kyuutils/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    test_suite='tests',
    install_requires=[
          'mysql-connector-python',
    ],
)
