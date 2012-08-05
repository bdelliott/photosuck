from optparse import OptionParser
import os
import sys

from prettytable import PrettyTable
import requests

from api import GraphAPI


def download_photos(album, photos):

    # use album name for the folder, or default to id if unnamed:
    album_name = album.get('name', album['id'])
    album_name = album_name.replace(" ", "_")
    # also get rid of directory separators:
    album_name = album_name.replace("/", "_")
    album_name = album_name[:80]

    d = os.path.join("photos", album_name)
    if not os.path.exists(d):
        os.makedirs(d)

    for p in photos:
        print "Downloading photo %s (album %s)" % (p['id'], album['id'])
        url = p['source']
        print "  " + url

        x = url.rfind(".") 
        ext = url[x:]

        # either user the photo's name as the filename, or fall back to an id:
        name = p.get('name', p['id'])
        name = name.replace(" ", "_")
        name = name.replace("/", "_")
        name = name[:50]

        fname = name + ext
        path = os.path.join(d, fname)
        f = open(path, "wb")
        
        r = requests.get(url)

        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
        f.close()


def print_albums(albums):
    field_names = ('Album Name', 'Owner', 'Id')
    table = PrettyTable(field_names=field_names)
    for a in albums:
        #print a
        l = (a['name'], a['from']['name'], a['id'])
        table.add_row(l)
    print table.get_string()


def print_photos(photos):
    field_names = ('Photo Name', 'Owner', 'Size', 'Id')
    table = PrettyTable(field_names=field_names)

    for p in photos:
        #print p
        #raise
        sz = "%dx%d" % (p['width'], p['height'])
        name = p.get('name', 'unnamed')
        l = (name[:50], p['from']['name'], sz, p['id'])
        table.add_row(l)
    print table.get_string()


if __name__=='__main__':
    parser = OptionParser(usage="%prog -u <Facebook user id>")
    parser.add_option("--stub", dest="stub", help="Stub API for testing",
            action="store_true", default=False)
    parser.add_option("-u", "--user-id", dest="user_id",
            help="Facebook user id", metavar="12345")
    parser.add_option("-f", "--friends", dest="friends", help="List friends", action="store_true")
    parser.add_option("-a", "--album-user-id", dest="album_user_id",
            help="Facebook user id of album owner", metavar="23456")
    parser.add_option("-s", "--sync", dest="sync", help="Sync *all* albums",
            action="store_true", default=False)

    (opts, args) = parser.parse_args()

    if not opts.user_id:
        parser.error("Please specify a facebook user id")

    api = GraphAPI.create(opts.user_id, opts.stub)

    if opts.friends:
        print api.list_friends()
        sys.exit(0)

    if opts.album_user_id:
        album_user_id = opts.album_user_id
    else:
        # default to the same user id
        album_user_id = opts.user_id


    if opts.sync:
        # sync all available albums:
        albums = api.list_albums(album_user_id)
        for album in albums:
            photos = api.list_album_photos(album['id'])
            download_photos(album, photos)
            print_photos(photos)

    else:
        # just print available album info :
        albums = api.list_albums(album_user_id)
        print_albums(albums)


