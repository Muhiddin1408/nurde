import jwt
import requests
import os
from datetime import timedelta
from django.utils import timezone
from social_core.utils import handle_http_errors


class AppleOAuth2:
    """apple authentication backend"""

    name = 'apple'
    ACCESS_TOKEN_URL = 'https://appleid.apple.com/auth/token'
    SCOPE_SEPARATOR = 'name email'
    ID_KEY = 'uid'

    @handle_http_errors
    def do_auth(self, access_token, *args, **kwargs):
        """
        Finish the auth process once the access_token was retrieved
        Get the email from ID token received from apple
        """
        try:

            client_id, client_secret = self.get_key_and_secret()
            print(client_id, client_secret)

            headers = {'content-type': "application/x-www-form-urlencoded"}

            data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'code': access_token,
                'grant_type': 'authorization_code',
                'scope': 'name email'
            }

            res = requests.post('https://appleid.apple.com/auth/token', data=data, headers=headers)

            response_dict = res.json()
            print(response_dict)

            # infoUrl = 'https://appleid.apple.com/auth/authorize?client_id=' + client_id + '&nonce=' + access_token + '&response_type=code&state=state&scope=name%20email&response_mode=form_post&redirect_uri=https://travel.gazon-tashkent.uz/api/v1/auth/apple-account/'
            # resOp = requests.get(infoUrl)
            id_token = response_dict.get('id_token', None)
            print(id_token)
            if id_token:
                print('kkkk')
                response_data = {}
                decoded = jwt.decode(id_token, '', options={"verify_signature": False})
                response_data.update({'email': decoded['email']}) if 'email' in decoded else None
                response_data.update({'uid': decoded['sub']}) if 'sub' in decoded else None
                response_data.update({'name': decoded['fullName']}) if 'fullName' in decoded else None
                # response_data.update({'decoded': {'data': resOp.status_code, 'infoUrl': infoUrl}})
                print(response_data)
                return True, response_data['email']
            else:
                return "The access token is invalid or expired."
        except:
            return "The access token is invalid or expired."

    def get_key_and_secret(self):
        kid = os.environ.get('USER_SOCIAL_AUTH_APPLE_KEY_ID')

        team_id = os.environ.get('USER_SOCIAL_AUTH_APPLE_TEAM_ID')

        client_id = os.environ.get('USER_SOCIAL_AUTH_APPLE_CLIENT_ID')

        private_key = open(os.environ.get('SOCIAL_AUTH_APPLE_PRIVATE_KEY_USER'), 'rb').read()
        print(kid)
        print(team_id)
        print(client_id)
        print(private_key)



        headers = {
            'kid': kid
        }
        print(headers)

        payload = {
            'iss': team_id,
            'iat': timezone.now(),
            'exp': timezone.now() + timedelta(days=180),
            'aud': 'https://appleid.apple.com',
            'sub': client_id,
        }

        client_secret = jwt.encode(
            payload,
            private_key,
            algorithm='ES256',
            headers=headers
        )  # .decode("utf-8")

        return client_id, client_secret
