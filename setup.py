import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "delete-migrations",
    version = "1.0.1",
    
    author = "Abandy Roosevelt",
    author_email = "rooseveltabandy@gmail.com",
    description = "This is a command-line app that deletes a single folder migrations or all directory migrations folder",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/RooseveltTech/delete_migration",
    project_urls = {
        "Bug Tracker": "https://github.com/RooseveltTech/delete_migration/issues",
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