import json
import pytest
from conftest import client


class TestAuth:
    @classmethod
    async def setup_class(cls):
        """setup any state specific to the execution of the given class (which usually contains tests)."""

    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a call to setup_class."""

    # @pytest.mark.skip
    def test_register_fail_email(self):
        response = client.post("/auth/register", json={
            "email": "test1example.ru",
            "password": "password",
        })
        assert response.status_code == 422
        assert response.text == '{"detail":[{"loc":["body","email"],"msg":"value is not a valid email address",' \
                                '"type":"value_error.email"},{"loc":["body","username"],"msg":"field required",' \
                                '"type":"value_error.missing"}]}'

    # @pytest.mark.skip
    def test_register_fail_username(self):
        response = client.post("/auth/register", json={
            "email": "test1@example.ru",
            "password": "password",
        })
        assert response.status_code == 422
        assert response.text == '{"detail":[{"loc":["body","username"],"msg":"field required",' \
                                '"type":"value_error.missing"}]}'

    # @pytest.mark.skip
    def test_register_new(self):
        new_user_dict = {
            "email": "test1@example.ru",
            "password": "password",
            "username": "test1user",
        }

        response = client.post("/auth/register", json=new_user_dict)
        assert response.status_code == 201
        new_user_response = json.loads(response.content)
        assert new_user_response['email'] == new_user_dict['email']
        assert new_user_response['username'] == new_user_dict['username']

    # @pytest.mark.skip
    def test_register_exists(self):
        new_user_dict = {
            "email": "test1@example.ru",
            "password": "password",
            "username": "test1user",
        }

        response = client.post("/auth/register", json=new_user_dict)
        assert response.status_code == 400
        assert response.text == '{"detail":"REGISTER_USER_ALREADY_EXISTS"}'

    # @pytest.mark.skip
    def test_login_ok(self):
        response = client.post("auth/jwt/login", data={
            "username": "test1@example.ru",
            "password": "password",
        }, headers={"content-type": "application/x-www-form-urlencoded"})
        assert response.status_code == 200
        token_response = json.loads(response.content)
        assert 'token_type' in token_response
        assert 'access_token' in token_response

    # @pytest.mark.skip
    def test_login_fail_email(self):
        response = client.post("auth/jwt/login", data={
            "username": "test2@example.ru",
            "password": "password",
        }, headers={"content-type": "application/x-www-form-urlencoded"})
        assert response.status_code == 400
        assert response.text == '{"detail":"LOGIN_BAD_CREDENTIALS"}'

    # @pytest.mark.skip
    def test_login_fail_pass(self):
        response = client.post("auth/jwt/login", data={
            "username": "test1@example.ru",
            "password": "test1@example.ru",
        }, headers={"content-type": "application/x-www-form-urlencoded"})
        assert response.status_code == 400
        assert response.text == '{"detail":"LOGIN_BAD_CREDENTIALS"}'
