"Test cases to verify CRUD functionality of github REST API users endpoint"

import pytest
import httpx
import random

import git_rest.helpers as helpers


class TestGetUsers:

    url = "https://api.github.com/users"
    user_url = "https://api.github.com/user"
    headers = {"Accept": "application/vnd.github+json"}

    @pytest.mark.parametrize("since", [random.randint(100, 10000), helpers.MAX_ID])
    def test_get_all_users(self, since):
        query_params = {"per_page": helpers.MAX_PAGINATION, "since": since}
        response = httpx.get(self.url, headers=self.headers, params=query_params)
        users = response.json()
        assert response.status_code == 200, "Unexpected status code"
        if since == helpers.MAX_ID:
            assert len(users) == 0, "Unexpected users were returned"
        else:
            first_user_id = users[0].get("id")
            assert (
                len(users) == helpers.MAX_PAGINATION
            ), "Incorrect number of users was returned"
            assert first_user_id > since, "Incorrect id of first returned user"

    @pytest.mark.parametrize("authorization", ["with_auth", "without_auth"])
    def test_get_authenticated_user(self, token_grained_none, authorization):
        if authorization == "without_auth":
            response = httpx.get(self.user_url, headers=self.headers)
            assert response.status_code == 401, "Unexpected status code"
        else:
            auth_header = {"Authorization": f"Bearer {token_grained_none}"}
            auth_header.update(self.headers)
            response = httpx.get(self.user_url, headers=auth_header)
            user_info = response.json()
            assert response.status_code == 200, "Unexpected status code"
            assert (
                user_info.get("login") == helpers.USER_NAME
            ), "Unexpected user name returned"

    @pytest.mark.parametrize("exists", ["existing", "non-existing"])
    @pytest.mark.parametrize("method", ["username", "account_id"])
    def test_get_user(self, method, exists):
        if exists == "existing":
            user_name = helpers.USER_NAME
            account_id = helpers.ACCOUNT_ID
        else:
            user_name = helpers.INVALID_NAME
            account_id = helpers.MAX_ID
        url = (
            self.url + f"/{user_name}"
            if method == "username"
            else self.user_url + f"/{account_id}"
        )
        response = httpx.get(url, headers=self.headers)
        user = response.json()

        if exists == "existing":
            assert response.status_code == 200, "Unexpected status code"
            assert (user.get("username") == user_name and method == "username") or (
                user.get("account_id") == account_id and method == "account_id"
            ), f"Unexepected {method} returned"
        else:
            assert response.status_code == 404, "Unexpected status code"
            assert user.get("message") == "Not Found", "Unexpected users returned"
