import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "delete-migration",
    version = "1.0.2",
    
    author = "Abandy Roosevelt",
    author_email = "rooseveltabandy@gmail.com",
    description = "This is a commandline app that deletes a single folder migrations or all directory migrations folder",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://www.github.com/RooseveltTech",
    project_urls = {
        "Bug Tracker": "https://www.github.com/RooseveltTech",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)