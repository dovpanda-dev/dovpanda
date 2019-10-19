import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dovpanda",
    version="0.0.1",
    author="Dean Langsam",
    author_email="deanla@gmail.com",
    description="DOn't reinVent PANDAs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeanLa/dovpanda",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)