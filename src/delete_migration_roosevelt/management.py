import argparse
import datetime
from pathlib import Path
import os
import shutil
from datetime import datetime

# get the root directory of the project
ROOT_DIR = os.path.abspath(os.curdir)

# get all system folders that
system_file = ["bin", "include", "site-packages","lib", "lib64", "Scripts", "Lib", "Include", "venv" ,"env", ".env", ".venv"]

def get_directories(path):
    folders = []

    while True:
        path, folder = os.path.split(path)
        if folder != '':
            folders.append(folder)
        else:
            if path != '':
                folders.append(path)
            break

    folders.reverse()
    return folders

# delete all migration folders excluding system folders
def delete_migration(delete):
    start_time = datetime.now()
    app_path=ROOT_DIR
    folder_name = 'migrations'
    count = {"number": 0}
    for root, dirs, file in os.walk(app_path):
        # check if migration folder exists
        if folder_name in dirs:
            my_path = os.path.abspath(os.path.join(root, folder_name))
            get_all_dir = get_directories(my_path)
            this_count = 0
            # check if path belongs to system folder 
            for system in system_file:
                if system in get_all_dir:
                    this_count += 1
                else:
                    pass
            if this_count < 1:
                count["number"] += 1
                # delete migration folder(s) and print the directory
                shutil.rmtree(os.path.abspath(os.path.join(root, folder_name)))
                print("dir >>>>", os.path.abspath(os.path.join(root, folder_name)), "deleted\n")
            else:
                pass
        else:
            pass
    if count["number"] == 0:
        msg = False
    elif count["number"] > 0:
        msg = True
    else:
        msg = False
    stop_time = datetime.now()
    task_time = stop_time - start_time
    print("done: ",task_time)
    return msg

# delete single directory migration folder
def delete_single_migration(delete):
    start_time = datetime.now()
    app_path=os.path.abspath(os.path.join(ROOT_DIR, delete))
    folder_name = 'migrations'
    count = {"number": 0}
    for root, dirs, file in os.walk(app_path):
        # check if migration folder exists
        if folder_name in dirs:
            my_path = os.path.abspath(os.path.join(root, folder_name))
            get_all_dir = get_directories(my_path)
            this_count = 0
            # check if path belongs to system folder 
            for system in system_file:
                if system in get_all_dir:
                    this_count += 1
                else:
                    pass
            if this_count < 1:
                count["number"] += 1
                # delete migration folder(s) and print the directory
                shutil.rmtree(os.path.abspath(os.path.join(root, folder_name)))
                print("dir >>>>", os.path.abspath(os.path.join(root, folder_name)), "deleted\n")
            else:
                pass
        else:
            pass    
    if count["number"] == 0:
        msg = False
    elif count["number"] > 0:
        msg = True
    else:
        msg = False
    stop_time = datetime.now()
    task_time = stop_time - start_time
    print("done: ",task_time)
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
    prog="delete-migrations",
    description="delete migrations folder",
    epilog="Thanks for using %(prog)s! :)",
    usage='%(prog)s [-h help] [-v version] [-d [arg] delete]',
)

# global_parser.add_argument('arg', help='required when using [-d] or [--delete]')
subparsers = global_parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='required when using [-d] or [--delete]')
subparsers.add_parser("all", help="delete migrations folder(s) from all directories", usage="[-d all]") 
subparsers.add_parser("dir_name", help="delete migrations folder(s) from the single <dir_name>", usage="[-d <dir_name>]")
global_parser.add_argument(
    "-d",
    "--delete",
    type=str,
    nargs=1,
    default="all",
    help="argument can be [all] or [dir_name]",
)
global_parser.set_defaults(func=delete_all)



global_parser.add_argument(
    "-v",
    "--version",
    action="version",
    version="%(prog)s 1.0.2"
)
args = global_parser.parse_args()

try:
    print(args.func(*args.delete))
except TypeError:
    global_parser.print_help()