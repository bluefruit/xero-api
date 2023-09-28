import base64
import datetime


class Token:
    def __init__(self):
        self.access_token = ""
        self.expires_in = 0
        self.token_type = ""
        self.scope = []
        self.expires_at = None

    def set(self, JWT):
        try:
            self.access_token = JWT["access_token"]
        except KeyError as e:
            raise Exception(JWT)
        self.expires_in = int(JWT["expires_in"])
        self.token_type = JWT["token_type"]
        self.scope = []
        for scope in JWT["scope"].split(" "):
            self.scope.append(scope)
        self.expires_at = datetime.datetime.today() + datetime.timedelta(
            seconds=self.expires_in - 120
        )

    def __repr__(self):
        ret = (
            "access_token: "
            + self.access_token[0:5]
            + "..."
            + self.access_token[-5:]
            + "\n"
        )
        ret += "expires_in: " + str(self.expires_in) + "\n"
        ret += "token_type: " + self.token_type + "\n"
        ret += "scope: " + self.scope.__repr__() + "\n"
        ret += "expires_at: " + self.expires_at
        return ret


def _create_space_seperated_scopes(scopes: list[str]):
    response = ""
    for scope in scopes:
        response += scope + " "
    response = response[:-1]
    return response


def _create_auth_header(id, secret):
    to_encode = id + ":" + secret
    to_encode = bytes(to_encode, encoding="utf-8")
    auth = b"Basic " + base64.b64encode(to_encode)
    return auth


async def _get_access_token(client, id, secret, scopes):
    scopes = _create_space_seperated_scopes(scopes)
    auth = _create_auth_header(id, secret)
    headers = {
        "authorization": auth,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    request_body = {"grant_type": "client_credentials", "scope": scopes}
    response = await client.post(
        "https://identity.xero.com/connect/token", headers=headers, data=request_body
    )
    return response.json()


async def get_access_token(client, id, secret, scopes):
    JWT = await _get_access_token(client, id, secret, scopes)
    token = Token()
    token.set(JWT)
    return token


