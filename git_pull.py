import os
import argparse, sys


def pull(path):
    print(f"Pulling \"{path}\"")
    if os.system(f"git -C \"{path}\" pull origin master") == 0:
        return True
    else:
        return False


def initialize_repo(path):
    print("Initializing git")
    if os.system(f"git -C \"{path}\" init") == 0:
        return True
    else:
        return False


def reset_origin(path):
    print("Reverting to latest master branch")
    if os.system(f"git -C {path} reset origin/master --hard") == 0:
        print("Revert succesfull")
        return True
    else:
        print("Error reverting")
        return False


def remote_origin_add(path):
    repo_name = path.split('\\')[-1].replace(' ', '-')
    username = os.popen("git config user.name", "r").read().strip()
    remote = f"https://github.com/{username}/{repo_name}"
    print(f"Adding remote origin {remote}")
    if os.system(f"git -C \"{path}\" remote add origin {remote}") == 0:
        return True
    else:
        return False


def remote_origin_remove(path):
    print("Attempting to remote remove origin")
    if os.system(f"git -C \"{path}\" remote remove origin") == 0:
        print("Removed")
        return True
    else:
        print("Removal error")
        return False


def push(path):
    print("Attempting to push")
    command = f"""cd \"{path}\"
    git add .
    git commit -m \"automated push\"
    git push origin master"""
    if os.system(command.replace('\n', '&')) == 0:
        print("Push successful!")
        return True
    else:
        print("Push failed")
        return False


def input_parse():
    parser = argparse.ArgumentParser(description="Easy update for local and remote repos in a given directory")
    parser.add_argument("-p", "--push", action="store_true", dest="push",
                        help="Also attempts to push repos after attempting to pull")
    parser.add_argument("-d", "--destination", nargs=1, dest="path",
                        help="Full path to the directory program will run at")
    parser.add_argument("-r", "--reset", action="store_true", dest="reset",
                        help="Reverts to origin branch before pulling to avoid merge issues(changes will be lost)")
    return parser


def main(argv):
    parser = input_parse()
    args = parser.parse_args(argv)
    path = os.getcwd()

    if args.path:
        path = ''.join(args.path)

    try:
        files = os.listdir(path)
        files = [os.path.join(path, f) for f in files]
    except Exception as e:
        print(e)
        sys.exit(-1)

    for f in files:
        if os.path.isdir(f):
            initialize_repo(f)
            if args.reset:
                reset_origin(f)
            if not pull(f):
                remote_origin_add(f)
                if not pull(f):
                    remote_origin_remove(f)
            # attempts to pull again after initializing and adding remote origin, removes the remote origin if failed
            if args.push:
                push(f)


if __name__ == "__main__":
    main(sys.argv[1:])
