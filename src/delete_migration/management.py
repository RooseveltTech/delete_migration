import argparse
import datetime
from pathlib import Path
import os
import shutil

# get the root directory of the project
ROOT_DIR = os.path.abspath(os.curdir)

# get all system folders that
system_file = ("bin", "include", "lib", "lib64", "Scripts", "Lib", "Include", "venv" ,"env", ".env", ".venv")

# delete all migration folders excluding system folders
def delete_migration(delete):
    app_path=ROOT_DIR
    folder_name = 'migrations'
    count = {"number": 0}
    for root, dirs, file in os.walk(app_path):
        # check if system folder exists
        is_system_file = root.endswith(system_file)
        if is_system_file == True:
            # dont delete system folders
            continue
        else:
            if folder_name in dirs:
                count["number"] += 1
                # delete migration folder(s) and print the directory
                shutil.rmtree(os.path.abspath(os.path.join(root, folder_name)))
                print("dir >>>>", os.path.abspath(os.path.join(root, folder_name)), "deleted\n")
    if count["number"] == 0:
        msg = False
    elif count["number"] > 0:
        msg = True
    else:
        msg = False
    return msg

# delete single directory migration folder
def delete_single_migration(delete):
    app_path=os.path.abspath(os.path.join(ROOT_DIR, delete))
    print(app_path)
    folder_name = 'migrations'
    count = {"number": 0}
    for root, dirs, file in os.walk(app_path):
        # check if system folder exists
        if root.endswith(system_file):
            continue
        else:
            if folder_name in dirs:
                count["number"] += 1
                # delete migration folder(s) and print the directory
                shutil.rmtree(os.path.abspath(os.path.join(root, folder_name)))
                print("dir >>>>", os.path.abspath(os.path.join(root, folder_name)), "deleted")
            else:
                pass
    
    if count["number"] == 0:
        msg = False
    elif count["number"] > 0:
        msg = True
    else:
        msg = False
    return msg
    
def delete_all(delete):
    if delete == "all":
        del_all = delete_migration(delete)
        if del_all is True:
            message = "all migration folders deleted"
            output_msg = global_parser.exit(1, message=message)
        else:
            message = "no migration folder found" 
            output_msg = global_parser.error(message=message)
    else:
        del_all = delete_single_migration(delete)
        if del_all is True:
            message = "single migration folder deleted"
            output_msg = global_parser.exit(1, message=message)
        else:
            message = "no migration folder found" 
            output_msg = global_parser.error(message=message)
    return output_msg


global_parser = argparse.ArgumentParser(
    prog="delete_migration",
    description="delete migrations folder",
    epilog="Thanks for using %(prog)s! :)"
)


global_parser.add_argument(
    "-d",
    "--delete",
    type=str,
    nargs=1,
    default="all",
    help="delete migrations folder in target directory"
)
global_parser.set_defaults(func=delete_all)



global_parser.add_argument(
    "-v",
    "--version",
    action="version",
    version="%(prog)s 1.0.0"
)
args = global_parser.parse_args()

try:
    print(args.func(*args.delete))
except TypeError:
    global_parser.print_help()