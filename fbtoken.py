import json


class TokenFetcher(object):
    def __call__(self, user_id):
        """Fetch user access token from fbtoken service"""
        print "call dawg"
        pass

    def _parse(self, user_id, j):
        d = json.loads(j)
        if d['user_id'] != user_id:
            raise Exception("Wrong user id.  Got %s, expected %s" % (d['user_id'],
                user_id))

        return d['token']


class StubTokenFetcher(TokenFetcher):
    def __call__(self, user_id):
        """Grab user access token from a test file"""

        f = open("data/sample_token_response.json")
        json = f.read()
        f.close()

        return self._parse(user_id, json)


