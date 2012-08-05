import client
import fbtoken


BASE_URL = "https://graph.facebook.com"

class GraphAPI(object):

    def __init__(self, user_id, token_fetcher=None, net_client=None):
        self.user_id = user_id

        if not token_fetcher:
            token_fetcher = fbtoken.TokenFetcher()

        self.token = token_fetcher(user_id)
        if not self.token:
            raise Exception("Failed to acquire a token for user %s" % user_id)

        if not net_client:
            net_client = client.Client()

        self.client = net_client

    def list_album_photos(self, album_id):
        """list photos in album"""

        url = self._url(obj=album_id, connection="photos")

        photos = self.client.get(url)
        return photos

    def list_albums(self, album_user_id):
        """list photo albums"""

        url = self._url(obj=album_user_id, connection="albums")

        # acquire all 'pages' of results:
        albums = self.client.get(url)

        return albums

    def list_friends(self):

        url = self._url(obj=self.user_id, connection="friends")
        friends = self.client.get(url)
        return friends

    def _url(self, obj=None, connection=None):
        if not obj:
            obj = self.user_id 

        url = BASE_URL + "/%s" % obj
        if connection:
            url += "/%s" % connection

        url += "?access_token=%s" % self.token

        return url

    @classmethod
    def create(cls, user_id, stub=False):

        kwargs = {}
        if stub:
            kwargs['token_fetcher'] = fbtoken.StubTokenFetcher()
            kwargs['client'] = client.StubClient()

        return GraphAPI(user_id, **kwargs)

