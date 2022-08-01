import modules
from modules import check_value
from modules import GitMate
from modules import get_path
import rest_client
import argparse
import namegenerator
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gitmate")

    parser.add_argument("-n", "--name",
                        help="Name of the project.")
    parser.add_argument("-d", "--description",
                        help="About your project")
    parser.add_argument("-p", "--path",
                        help="Local path to create a directory")

    parser.add_argument("-username")
    parser.add_argument("-token")

    args = parser.parse_args()

    if args.username or args.token:
        if args.username:
            modules.set_data("username", args.username)
            print("-- GitMate --")
            print(f"[+] Username {args.username} added !")
            exit()

        if args.token:
            modules.set_data("authtoken", args.token)
            print("-- GitMate --")
            print(f"[+] Token added !")
            exit()

    # check: if "token" is available
    global TOKEN
    with open("user_data.json", "r+") as file:
        user_data = json.load(file)
        token = user_data["authtoken"]

        if not token:
            print("-- GitMate --")
            print("[!] Add Personal Assess token to use gitmate.")
            print("$ gitmate -token \"your_personal_access_token\" ")
            exit()
        else:
            TOKEN = token

    global project_name, project_description, project_path

    project_name = args.name if check_value(
        args.name) else namegenerator.gen(repeatParts=False)
    project_description = args.description if check_value(
        args.description) else "New Project !"
    project_path = args.path if check_value(args.path) else get_path()

    git_commands = ["git add .", "git commit -m \"Initial commit 🗳️\""]

    gitmate = GitMate(project_path, project_name)
    gitmate.create_local_repo()
    gitmate.git_init()
    gitmate.add_readme(project_name, project_description)
    gitmate.stage_git(git_commands)

    data_header = {"name": f"{project_name}",
                   "description": f"{project_description}"}
    url = "https://api.github.com/user/repos"
    github = rest_client.RestClient(TOKEN, data_header, url)
    github.create_post_request()
    errors = github.error_check()

    if errors != 0:
        print("[*] Error Occoured while creating remote repository")
        print(errors)
        exit()

    remote_url = github.pretty_response()
    gitmate.adding_remote_repository(remote_url)
    gitmate.git_push()
