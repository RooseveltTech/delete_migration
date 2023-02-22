# `migrations_delete`

The `migrations_delete` is a commandline app that deletes a single folder migrations or all directory migrations folder.

# Installation
## Using Pip
```bash
  $ pip install delete_migration
```
## Accessing the package on command line
- [x] create a file "find.py" on the root directory of your project
- [x] import the commandline app in the "find.py" file
    ```bash
    $ from delete_migration_roosevelt import management
    ```
- [x] save the "find.py"

# Usage
```bash
$ python find.py
```
## get help
`using the help command`
```bash
$ python find.py --help
```
`using the help command abbreviated`
```bash
$ python find.py -h
```
## all migrations folders
`search and delete folders migrations`
```bash
$ python find.py --delete all
```
`search and delete folders migrations abbreviated`
```bash
$ python find.py -D all
```
## all single folder
`search and delete single folder migrations`
```bash
$ python find.py --delete <name-of-folder>
```
`search and delete single folder migrations abbreviated`
```bash
$ python find.py -D <name-of-folder>
```
## all single folder
`get the current version of the commandline library`
```bash
$ python find.py --version
```
`get the current version of the commandline library abbreviated`
```bash
$ python find.py -V
```