import requests
# import namegenerator


# sample code for rest api
"""
auth_token = 'your_personal_access_token'

hed = {'Authorization': 'token ' + auth_token}
data = {'name': 'test-repo1', 'description': 'New Repository'}

url = "https://api.github.com/user/repos"

response = requests.post(url, json=data, headers=hed)
print(response.json())

"""


class RestClient:
    """
    REST client for github request 
    """

    def __init__(self, auth_token, data, url) -> None:
        self.auth_token = auth_token
        self.data = data
        self.url = url
        self.head = {"Authorization": f"token {self.auth_token}"}
        self.response = None

    def create_post_request(self) -> requests.Response:
        """
        Calls GitHub Api and create a response object.
        """
        self.response = requests.post(
            url=self.url, headers=self.head, json=self.data)
        return self.response

    def error_check(self):
        """
        Checking if same repository already exists or any other error
        """
        if "errors" in self.response:
            error_message = self.response["errors"][0]["message"]
            return error_message
        return 0

    def pretty_response(self):
        """
        Decorating Response for output
        """
        data = self.response.json()
        name = data["name"]
        url_path = data["full_name"]
        url = "https://www.github.com/"+url_path
        self.git_url = url + ".git"
        print(
            f"STATUS => {self.response}\nREPOSITORY NAME => {name}\nGITHUB URL => {url}")
        return self.git_url


# Testing RestClient() class
"""
# Test Data

newname = namegenerator.gen()
token = "your_personal_access_token"
data = {"name": f"{newname}", "description": "This is a repository."}
url = "https://api.github.com/user/repos"


github = RestClient(token, data, url)
response = github.create_post_request()
github.pretty_response()
print(github.git_url)

test passed
"""
