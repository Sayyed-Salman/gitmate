import os
import argparse
import json
import namegenerator
from rest_client import RestClient


def check_value(argument):
    if argument:
        return True


def set_data(key, value):
    with open("user_data.json", "+r") as file:
        user_data = json.load(file)
        user_data[key] = value
        file.seek(0)
        json.dump(user_data, file, indent=4)
        file.truncate()


def create_local_repo(name, path):
    """
    Creates local repository and returns project path
    """
    if os.path.isdir(path):
        project_path = os.path.join(path, name)
        os.chdir(path)
        os.mkdir(project_path)
    return project_path


def git_init(path):
    """
    Initializes github repository, returns system response.
    """
    if os.path.isdir(path):
        os.chdir(path)
        system_response = os.system("git init")
    return system_response


def add_readme(path, title, description):
    """
        Create a README.md file in project dir root.
    """
    if os.path.isdir(path):
        os.chdir(path)
        file_content = f""" # {title}
        {description}
        """
        file_path = os.path.join(path, "README.md")
        with open("README.md", 'w+') as file:
            file.write(file_content)

    if os.path.isfile(file_path):
        return 0


# testing add_readme() func
"""
result = add_readme('A:\\Test\\monkey', "Monkey-Code",
                    "Writing Monkey Code to analyze how monkey brain works")
print(result)
test passed 
"""


def stage_git(path, commands: list):
    """
    Stating changes to git and then commiting
    returns system response, check while debugging
    """
    if os.path.isdir(path):
        os.chdir(path)
        sys_response = []
        for cmd in commands:
            try:
                response = os.system(cmd)
                sys_response.append(response)
            except Exception as e:
                return (e, sys_response)
        return 0


# testing stage_git()
"""
result = stage_git('A:\\Test\\monkey', [
                   "git add .", "git commit -m \"first commit\""])
print(result)
test passed
"""


def adding_remote_repository(path, remote_link):
    if os.path.isdir(path):
        os.chdir(path)
        sys_log = []
        try:
            add_remote = os.system(f"git remote add origin {remote_link}")
            branch = os.system("git branch -M main")
            sys_log.append(add_remote)
            sys_log.append(branch)
        except Exception as e:
            return (e, sys_log)

        return 0


def git_push(path):
    if os.path.isdir(path):
        os.chdir(path)
        sys_log = []
        try:
            push = os.system("git push -u origin main")
            sys_log.append(push)
        except Exception as e:
            return (e, sys_log)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # general arguments
    parser.add_argument("-n", "--name", help="Repository name")
    parser.add_argument("-d", "--description",
                        help="Description about the repository")
    parser.add_argument("-p", "--path", help="Local path")

    # User Data arguments
    parser.add_argument("--set-username", help="sets github username")
    parser.add_argument("--set-auth-token",
                        help="set your github personal access token")
    parser.add_argument("--set-projects-folder",
                        help="set a default project folder")
    args = parser.parse_args()

    PROJECT_NAME = args.name if check_value(
        args.name) else namegenerator.gen()
    PROJECT_DESCRIPTION = args.description if check_value(
        args.description) else "This is a new repository"
    USER_DATA = None
    URL = "https://api.github.com/user/repos"
    AUTH_TOKEN = None
    PATH = args.path if check_value(args.path) else "../"

    if args.set_auth_token:
        token = args.set_auth_token
        set_data("auth_token", token)
        exit

    elif check_value(args.set_projects_folder):
        folder_loc = args.set_projects_folder
        set_folder = False
        while not set_folder:
            if os.path.isdir:
                set_data("projectsFolder", folder_loc)
                set_folder = True
            else:
                print("[!] Invalid Folder Location ")
                folder_loc = input(
                    "Enter Project Folder Location again (absolute path): ")
        exit

    else:
        with open("user_data.json", "r") as file:
            USER_DATA = json.load(file)
            AUTH_TOKEN = USER_DATA["auth_token"]
            PROJECT_FOLDER = USER_DATA["projectsFolder"]

        if USER_DATA['auth_token'] == "":
            print("* Git Mate *")
            print("set your personal-access-token")
            print("gitmate --set-auth-token \"your_personal_access_token\"")
            exit
        elif USER_DATA["projectsFolder"] == "":
            print("[!] Set your default projects folder ")
            print("[cmd] gitmate --set-projects-folder")

    # if not USER_DATA["projectsFolder"] == "":
    #     PATH = USER_DATA["projectsFolder"]


#  Execution starts here
    create_local_repo(PROJECT_NAME, PATH)
    git_init(PATH)
    add_readme(PATH, PROJECT_NAME, PROJECT_DESCRIPTION)

    git_commands = ["git add .", "git commit -m \"Initial commit 🗳️\""]
    stage_git(PATH, git_commands)

    data = {"name": f"{PROJECT_NAME}", "description": f"{PROJECT_DESCRIPTION}"}
    github = RestClient(AUTH_TOKEN, data, URL)
    github.create_post_request()
    error_check = github.error_check()

    if error_check != 0:
        print("[*] Error Occoured while creating remote repository")
        print(error_check)
        exit

    REMOTE_URL = github.pretty_response()
    adding_remote_repository(PATH, REMOTE_URL)
    git_push(PATH)
