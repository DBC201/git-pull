import os
import shutil

from sys import exit

def write_location(location):
    user = os.path.expanduser("~")
    install_folder = os.path.join(user, "Documents", "git-pull")
    with open(os.path.join(install_folder, "location_log"), 'a') as file:
        file.write(location + '\n')


def return_locations():
    user = os.path.expanduser("~")
    install_folder = os.path.join(user, "Documents", "git-pull")
    locations = []
    with open(os.path.join(install_folder, "location_log"), 'r') as file:
        while True:
            line = file.readline().strip()
            if not line:
                break
            locations.append(line)
    return locations


def remove_location(location):
    locations = return_locations()
    if location in locations:
        locations.remove(location)
        user = os.path.expanduser("~")
        install_folder = os.path.join(user, "Documents", "git-pull")
        with open(os.path.join(install_folder, 'location_log'), 'w') as file:
            for location in locations:
                file.write(location + '\n')


def confirm_selection():
    while True:
        selection = input("Type confirm to confirm, cancel to change:").lower()
        if selection == "confirm":
            return True
        elif selection == "cancel":
            return False


def yes_no_selection(prompt):
    while True:
        selection = input(f"{prompt}(y/n):").lower()
        if selection == 'y':
            return True
        elif selection == 'n':
            return False


def get_repo_folder():
    while True:
        repo_folder = input("Enter the full path where your git repos are at:")
        try:
            repos = os.listdir(repo_folder)
        except Exception as e:
            print(e)
            print("Failed to find or access the given folder")
        else:
            for repo in repos:
                print(repo)
            if confirm_selection():
                return repo_folder

def uninstall():
    user = os.path.expanduser("~")
    try:
        for f in return_locations():
            try:
                os.remove(f)
            except Exception as e:
                print(e)
        shutil.rmtree(os.path.join(user, "Documents\git-pull"))
    except Exception as e:
        print(e)
        print("Error deleting files")
    else:
        print("Succesfully uninstalled!")
        exit()


def options():
    menu = """
    Type u to uninstall
    Type r to change repo dir
    Type s to add/remove from startup
    Type c to create a bat file in desired dir
    Type a to change arguments
    Type e to exit
    """
    while True:
        print(menu)
        selection = input().lower()
        user = os.path.expanduser("~")
        if selection == 'u':
            uninstall()
        elif selection == 'r':
            new_location = get_repo_folder()
            for f in return_locations():
                create_bat_file('\\'.join(f.split('\\')[:-1]), new_location)
            print("Done!")
        elif selection == 's':
            startup_folder = os.path.join(
                user,
                "AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
            )
            if check_startup():
                if yes_no_selection("Are you sure you want to remove the program from startup?"):
                    try:
                        os.remove(os.path.join(startup_folder, "run-git-pull.bat"))
                    except Exception as e:
                        print(e)
                        print("Error removing from startup, perhaps run as admin?")
                    else:
                        remove_location(os.path.join(startup_folder, "run-git-pull.bat"))
                        print("Sucessfully removed!")
            else:
                if yes_no_selection("Are you sure you want to add the program to startup?"):
                    repo_folder = get_repo_folder()
                    create_bat_file(startup_folder, repo_folder)
                    print("Done!")
        elif selection == 'c':
            repo_folder = get_repo_folder()
            folder = input("Enter the full path to desired directory:")
            try:
                create_bat_file(folder, repo_folder)
            except OSError as e:
                print(e)
                print("Perhaps this dir doesn't exit or isn't accessible?")
            else:
                print("Done!")
        elif selection == 'a':
            print("This will change the arguments for all found .bat files")
            push = yes_no_selection("Would you like to auto push after each pull?")
            reset = yes_no_selection("Would you like to hard reset master before each pull(local will be lost)")
            arguments = []
            if push:
                arguments.append('-p')
            if reset:
                arguments.append('-r')
            arguments = ' '.join(arguments)
            for f in return_locations():
                repo_folder = ''
                with open(f, "r") as file:
                    content = file.read()
                    index = content.find('-d')
                    repo_folder = content[index + 2:]
                    repo_folder = repo_folder.strip(" \"")
                remove_location(f)
                os.remove(f)
                create_bat_file('\\'.join(f.split('\\')[:-1]), repo_folder, arguments)
            print("Done!")
        elif selection == 'e':
            return


def check_startup():
    user = os.path.expanduser("~")
    return "run-git-pull.bat" in os.listdir(
        os.path.join(user, "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"))


def check_documents():
    user = os.path.expanduser("~")
    return "git-pull" in os.listdir(os.path.join(user, "Documents"))


def create_bat_file(bat_location, script_destination, arguments=''):
    script_path = os.path.join(
        os.path.expanduser("~"),
        "Documents",
        "git-pull",
        "git_pull.py"
    )
    path_argument = f"-d \"{script_destination}\""
    command = f"""@echo off
cmd /k \"python \"{script_path}\" {arguments} {path_argument} \""""
    with open(os.path.join(bat_location, "run-git-pull.bat"), "w") as file:
        file.write(command)
        write_location(os.path.join(bat_location, "run-git-pull.bat"))


def install(repo_folder, startup):
    user = os.path.expanduser("~")
    install_folder = os.path.join(user, "Documents\git-pull")
    try:
        os.mkdir(install_folder)
        shutil.copy2(
            os.path.join(os.getcwd(), "git_pull.py"),
            install_folder
        )
        shutil.copy2(
            os.path.join(os.getcwd(), "install.py"),
            install_folder
        )
        create_bat_file(install_folder, repo_folder)
        create_bat_file(os.path.join(user, "Desktop"), repo_folder)
        if startup:
            try:
                create_bat_file(
                    os.path.join(user, "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"),
                    repo_folder
                )
            except Exception as e:
                print("Unable to add it to start, perhaps run as admin?")
                print(e)
    except Exception as e:
        print("Unable to install")
        raise e
    print("Install sucessful")
    print("Run this again to view options")


if __name__ == "__main__":

    print("git-pull by dbc201")
    print("Press CTRL+C to halt")
    if check_documents():
        options()
    elif check_startup():
        print("Installation in startup found but not in documents")
        print("Perhaps you would like to check it out?")
        user = os.path.expanduser("~")
        startup_folder = os.path.join(user, "AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        os.system(f"explorer.exe \"{startup_folder}\"")
    else:
        repo_folder = get_repo_folder()
        startup = yes_no_selection("Would you like to have this program run on startup")
        install(repo_folder, startup)