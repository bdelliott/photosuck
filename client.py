import json

import requests


class Client(object):
    def get(self, url):
        """paging-enabled get"""
      
        items = []

        while url:
            d = self._get(url)
            _items = d['data']
            if _items:
                url = d['paging']['next']
                items.extend(_items)
            else:
                url = None

        return items

    def _get(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception(r)
        return r.text

    def _parse(self, j):
        return json.loads(j)

class StubClient(Client):

    def _get(self, url):
        """Just get sample JSON data from local files"""
        if url.find("&after") != -1:
            # if this is page >= 2, return nothing:
            d = {"data": []}
            return d

        if url.find("/albums?") != -1:
            f = open("data/sample_albums.json")
            j = f.read()
            f.close()
            return self._parse(j)

        elif url.find("/photos?") != -1:
            f = open("data/sample_album_photos.json")
            j = f.read()
            f.close()
            return self._parse(j)

        raise Exception("Can't stub %s" % url)
