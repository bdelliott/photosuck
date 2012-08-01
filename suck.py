from optparse import OptionParser
import os

from prettytable import PrettyTable
import requests

from api import GraphAPI


def download_photos(album_id, photos):

    d = os.path.join("photos", album_id)
    if not os.path.exists(d):
        os.makedirs(d)

    for p in photos:
        print "Downloading photo %s (album %s)" % (p['id'], album_id)
        url = p['picture']
        print "  " + url

        x = url.rfind(".") 
        ext = url[x:]
        fname = p['id'] + ext
        path = os.path.join(d, fname)
        f = open(path, "wb")
        
        r = requests.get(url)

        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
        f.close()


def print_albums(albums):
    field_names = ('Album Name', 'Owner', 'Size', 'Id')
    table = PrettyTable(field_names=field_names)
    for a in albums:
        #print a
        l = (a['name'], a['from']['name'], a['count'], a['id'])
        table.add_row(l)
    print table.get_string()


def print_photos(photos):
    field_names = ('Photo Name', 'Owner', 'Size', 'Id')
    table = PrettyTable(field_names=field_names)

    for p in photos:
        #print p
        #raise
        sz = "%dx%d" % (p['width'], p['height'])
        l = (p['name'][:50], p['from']['name'], sz, p['id'])
        table.add_row(l)
    print table.get_string()


if __name__=='__main__':
    parser = OptionParser(usage="%prog -u <Facebook user id>")
    parser.add_option("-s", "--stub", dest="stub", help="Stub API for testing",
            action="store_true", default=False)
    parser.add_option("-u", "--user-id", dest="user_id",
            help="Facebook user id", metavar="12345")
    parser.add_option("-a", "--album-user-id", dest="album_user_id",
            help="Facebook user id of album owner", metavar="23456")
    parser.add_option("-d", "--download-album-ids", dest="download_album_ids",
            help="Comma-separated list of album ids to suck down", metavar="123,456,789",
            default=None)

    (opts, args) = parser.parse_args()

    if not opts.user_id:
        parser.error("Please specify a facebook user id")

    if opts.album_user_id:
        album_user_id = opts.album_user_id
    else:
        # default to the same user id
        album_user_id = opts.user_id

    api = GraphAPI.create(opts.user_id, opts.stub)

    # if requested, download any specified albums:
    if opts.download_album_ids:
        album_ids = opts.download_album_ids.split(",")
        for album_id in album_ids:
            photos = api.list_album_photos(album_id)
            download_photos(album_id, photos)
            print_photos(photos)
    else:
        # just print available album info :
        albums = api.list_albums(album_user_id)
        print_albums(albums)


