import json
import pytest
from conftest import client


class TestAuth:

    emails_reg = ['test1@example.ru', '+79876543210']
    emails_login = ['test1@example.ru', '+79876543210', '9876543210']
    emails_fail = ['test1example.ru', 'test1@exampleru', '+79876543210', '+9876543210', '98765432100']

    @classmethod
    async def setup_class(cls):
        """setup any state specific to the execution of the given class (which usually contains tests)."""

    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a call to setup_class."""

    # @pytest.mark.skip
    def test_register_fail_email(self):
        for email in self.emails_fail:
            new_user_dict = {
                'email': email,
                'password': 'password',
            }
        response = client.post('/auth/register', json=new_user_dict)
        assert response.status_code == 422
        assert response.text == '{"detail":[{"loc":["body","email"],"msg":"value is not a valid email address",' \
                                '"type":"value_error.email"},{"loc":["body","email"],"msg":"value is not a valid ' \
                                'phone","type":"value_error"}]}'

    # @pytest.mark.skip
    def test_register_new(self):
        for email in self.emails_reg:
            new_user_dict = {
                'email': email,
                'password': 'password',
            }
            response = client.post('/auth/register', json=new_user_dict)
            assert response.status_code == 201
            json_response = json.loads(response.content)
            assert json_response['email'] == new_user_dict['email']

    # @pytest.mark.skip
    def test_register_exists(self):
        for email in self.emails_login:
            new_user_dict = {
                'email': email,
                'password': 'password',
            }

            response = client.post('/auth/register', json=new_user_dict)
            assert response.status_code == 400
            assert response.text == '{"detail":"REGISTER_USER_ALREADY_EXISTS"}'

    # @pytest.mark.skip
    def test_login_ok(self):
        for email in self.emails_login:
            new_user_dict = {
                'username': email,
                'password': 'password',
            }

            response = client.post('auth/jwt/login', data=new_user_dict,
                                   headers={'content-type': 'application/x-www-form-urlencoded'})
            assert response.status_code == 200
            token_response = json.loads(response.content)
            assert 'token_type' in token_response
            assert 'access_token' in token_response

    # @pytest.mark.skip
    def test_login_fail_email(self):
        response = client.post('auth/jwt/login', data={
            'username': 'test2@example.ru',
            'password': 'password',
        }, headers={'content-type': 'application/x-www-form-urlencoded'})
        assert response.status_code == 400
        assert response.text == '{"detail":"LOGIN_BAD_CREDENTIALS"}'

    # @pytest.mark.skip
    def test_login_fail_pass(self):
        response = client.post('auth/jwt/login', data={
            'username': 'test1@example.ru',
            'password': 'test1@example.ru',
        }, headers={'content-type': 'application/x-www-form-urlencoded'})
        assert response.status_code == 400
        assert response.text == '{"detail":"LOGIN_BAD_CREDENTIALS"}'
