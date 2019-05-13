
import json
import os
import subprocess
from typing import Dict, List, Union, AnyStr
from urllib import parse, request
from urllib.error import HTTPError

API_URL = 'https://git.soton.ac.uk/api/v4/'


def get_all_projects_owned_by_current_user() -> List[Dict]:
    cmd = 'projects?owned=true&per_page=100'
    projects = api_call(cmd)
    return projects


def api_call(cmd: AnyStr, token: Union[AnyStr, None] = None, data: Dict = None, username: AnyStr = None):
    if token is None:
        token = get_token(username)
    headers = {'Private-Token': token}

    parsed_data = parse.urlencode(data).encode() if data else None

    full_url = API_URL + cmd
    request_object = request.Request(full_url, headers=headers, data=parsed_data)

    response = request.urlopen(request_object)
    json_data = response.read()
    data = json.loads(json_data)
    return data


def add_user_to_project(project: Dict, user: Dict, access_level: int):
    data = {'user_id': user['id'], 'access_level': access_level}
    cmd = f'/projects/{project["id"]}/members'
    user_response = api_call(cmd, data=data)
    print(user_response)


def add_user_to_gitlab_projects(projects: List[Dict]):
    username_to_add = 'etfrogers'
    access_level = 40
    user = get_user_details(username_to_add)
    print(user)
    for project in projects:
        try:
            add_user_to_project(project, user, access_level)
        except HTTPError:
            pass


def get_user_details(username: AnyStr) -> Dict:
    cmd = f"user/"
    user = api_call(cmd, username=username)
    return user


def get_token(username: str = None):
    if not username:
        username = 'etfr'
    token_file = f'{username}_api_token.txt'
    with open(token_file) as f:
        token = f.readline()
    return token


def clone_all_projects(projects: List[Dict], into_dir: AnyStr):
    os.chdir(into_dir)
    for project in projects:
        # Needs to be run from a bash prompt.
        completed_process = subprocess.run(['git', 'clone', project["ssh_url_to_repo"]], shell=True)


def main():
    projects = get_all_projects_owned_by_current_user()
    print(projects)
    # add_user_to_gitlab_projects(projects)
    clone_directory = r'C:\Users\Ed\Documents\git.soton.ac.uk backup'
    clone_all_projects(projects, clone_directory)


if __name__ == '__main__':
    main()
