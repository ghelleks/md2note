from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="md2note",
    version="0.1.0",
    author="Gunnar Hellekson",
    author_email="gunnar@hellekson.com",
    description="A Python application that converts Markdown files to Apple Notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghelleks/md2note",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: Markup",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pyyaml>=6.0",
        "markdown>=3.4",
    ],
    entry_points={
        "console_scripts": [
            "md2note=main:main",
        ],
    },
) 