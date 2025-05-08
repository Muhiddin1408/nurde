import sys
from google.auth.transport import requests
from google.oauth2 import id_token

from core.settings import GOOGLE_ID_TOKEN_ISS


class Google:
    @staticmethod
    def verify_auth_token(auth_token):
        try:
            id_info = id_token.verify_token(auth_token, requests.Request())

            if GOOGLE_ID_TOKEN_ISS in id_info['iss']:
                return True, id_info

        except Exception as e:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            msg = str(e) + ' --- line -' + str(line)
            return False, msg
