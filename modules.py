import os
import json


class GitMate:
    """
    Creating and Linking Git Repository
    """

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.project_path = os.path.join(self.path, self.name)

    def create_local_repo(self):
        """
        Creates local repository and returns project path
        """
        if os.path.isdir(self.path):
            # project_path = os.path.join(self.path, name)
            os.chdir(self.path)
            os.mkdir(self.project_path)

    def git_init(self):
        """
        Initializes github repository, returns system response.
        """
        if os.path.isdir(self.project_path):
            os.chdir(self.project_path)
            system_response = os.system("git init")
        return system_response

    def add_readme(self, title, description):
        """
            Create a README.md file in project dir root.
        """
        if os.path.isdir(self.project_path):
            os.chdir(self.project_path)
            file_content = f""" # {title}
            {description}
            """
            file_path = os.path.join(self.project_path, "README.md")
            with open("README.md", 'w+') as file:
                file.write(file_content)

        if os.path.isfile(file_path):
            return 0

    def stage_git(self, commands: list):
        """
        Stating changes to git and then commiting
        returns system response, check while debugging
        """
        if os.path.isdir(self.project_path):
            os.chdir(self.project_path)
            sys_response = []
            for cmd in commands:
                try:
                    response = os.system(cmd)
                    sys_response.append(response)
                except Exception as e:
                    return (e, sys_response)
            return 0

    def adding_remote_repository(self, remote_link):
        """
        Adding Remote link to local repository
        """
        if os.path.isdir(self.project_path):
            os.chdir(self.project_path)
            sys_log = []
            try:
                add_remote = os.system(f"git remote add origin {remote_link}")
                branch = os.system("git branch -M main")
                sys_log.append(add_remote)
                sys_log.append(branch)
            except Exception as e:
                return (e, sys_log)

            return 0

    def git_push(self):
        if os.path.isdir(self.project_path):
            os.chdir(self.project_path)
            sys_log = []
            try:
                push = os.system("git push -u origin main")
                sys_log.append(push)
            except Exception as e:
                return (e, sys_log)


# Utility Methods

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
