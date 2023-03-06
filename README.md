📦 delete-migrations
=======================

The `delete-migrations` is a command-line app that deletes a single folder migrations or all directory migrations folder.

# Installation
You can install nigeria_banks from [PyPI](https://pypi.org/project/delete-migrations/):

## Create a virtual environment in root folder
`for mac, linux os`
```bash
  $ virtualenv <virtualenv_name> #create a virtual environment
  $ source <virtualenv_name>/bin/activate #activate the virtual environment
```
`for windows os`
```bash
  $ virtualenv <virtualenv_name> #create a virtual environment
  $ <virtualenv_name>\Scripts\activate #activate the virtual environment
```
## Using Pip
```bash
  $ pip install delete-migrations #install the delete-migrations package
```
## Accessing the package on command line
- [x] create a file "find.py" on the root directory of your project
- [x] import the delete-migrations command-line app in the "find.py" file from the module below
    ```bash
    from delete_migration_roosevelt import management
    ```
- [x] save the "find.py"

# Usage
`find usage commands`
```bash
$ python find.py #for mac, linux
```
```bash
$ py find.py #for windows
```
## get help
`using the help command`
```bash
$ python find.py --help #for mac, linux
```
```bash
$ py find.py --help #for windows
```
`using the help command abbreviated`
```bash
$ python find.py -h #for mac, linux
```
```bash
$ py find.py -h #for windows
```
`using the <all> directory help command`
```bash
$ python find.py all -h #for mac, linux
```
```bash
$ py find.py all -h #for windows
```
`using the "<dir_name" directory help command`
```bash
$ python find.py dir_name -h #for mac, linux
```
```bash
$ py find.py dir_name -h #for windows
```

## all migrations folders
`search and delete folders migrations`
```bash
$ python find.py --delete all #for mac, linux
```
```bash
$ py find.py --delete all #for windows
```
`search and delete folders migrations abbreviated`
```bash
$ python find.py -d all #for mac, linux
```
```bash
$ py find.py -d all #for windows
```
## all single folder
`search and delete single folder migrations`
```bash
$ python find.py --delete <name-of-folder> #for mac, linux
```
```bash
$ py find.py --delete <name-of-folder> #for windows
```
`search and delete single folder migrations abbreviated`
```bash
$ python find.py -d <name-of-folder> #for mac, linux
```
```bash
$ py find.py -d <name-of-folder> #for windows
```
## all single folder
`get the current version of the command-line library`
```bash
$ python find.py --version #for mac, linux
```
```bash
$ py find.py --version #for windows
```
`get the current version of the command-line library abbreviated`
```bash
$ python find.py -v #for mac, linux
```
```bash
$ py find.py -v #for windows
```