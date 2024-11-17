"Test cases to verify CRUD functionality of github REST API repositiory endpoint"

import pytest
import httpx
import random
import json

import git_rest.helpers as helpers

class TestGetRepositories:

    url = f"https://api.github.com/repos/{helpers.USER_NAME}"
    headers = {"Accept": "application/vnd.github+json"}
    test_repo_name = "test_repo_1"
    repo_url = url + f"/{test_repo_name}"

    @pytest.mark.parametrize("token", ["with_permission", "without_permission"])
    def test_get_user_repository(self, token_grained_all, token_grained_none, token):
        auth_token = (
            token_grained_all
            if token == "with_permission"
            else token_grained_none
        )
        auth_header = {"Authorization": f"Bearer {auth_token}"}
        auth_header.update(self.headers)
        response = httpx.get(self.repo_url, headers=auth_header)
        repo = response.json()
        if token == "without_permission":
            assert response.status_code == 404, "Unexpected status code"
        else:
            assert response.status_code == 200, "Unexpected status code"
            assert (
                repo.get("name") == self.test_repo_name
            ), "Unexpected repository returned"


class TestUpdateRepositories:

    url = f"https://api.github.com/repos/{helpers.USER_NAME}"
    headers = {"Accept": "application/vnd.github+json"}
    test_repo_name = "test_repo_2"

    def test_update_non_existant(self, token_grained_all):
        random_description = helpers.random_string(100)
        auth_header = {"Authorization": f"Bearer {token_grained_all}"}
        auth_header.update(self.headers)
        update_data = json.dumps({"description": random_description})
        response = httpx.patch(
            self.url + f"/{helpers.INVALID_NAME}",
            headers=auth_header,
            content=update_data,
        )
        assert response.status_code == 404, "Unexpected status code"

    def test_update_existant(self, token_grained_all):
        random_description = helpers.random_string(100)
        auth_header = {"Authorization": f"Bearer {token_grained_all}"}
        auth_header.update(self.headers)
        update_data = json.dumps({"description": random_description})
        response = httpx.patch(
            self.url + f"/{self.test_repo_name}",
            headers=auth_header,
            content=update_data,
        )
        assert response.status_code == 200, "Unexpected status code"


class TestDeleteRepositories:

    url = f"https://api.github.com/repos/{helpers.USER_NAME}"
    headers = {"Accept": "application/vnd.github+json"}

    def test_delete_non_existant(self, token_grained_all):
        auth_header = {"Authorization": f"Bearer {token_grained_all}"}
        auth_header.update(self.headers)
        response = httpx.delete(
            self.url + f"/{helpers.INVALID_NAME}", headers=auth_header
        )
        assert response.status_code == 404, "Unexpected status code"
