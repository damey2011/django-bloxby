from django.contrib.sites.models import Site
from pyftpdlib.servers import FTPServer

from bloxby.ftp.authorizers import APIAuth
from bloxby.ftp.filesystems import CustomFileSystem
from bloxby.ftp.handlers import Handler


def get_ftp_server(host, port=21):
    authorizer = APIAuth()
    handler = Handler
    handler.authorizer = authorizer
    handler.abstracted_fs = CustomFileSystem
    handler.masquerade_address = Site.objects.get_current().domain
    handler.passive_ports = range(60000, 65535)
    address = (host, port)
    server = FTPServer(address, handler)
    return server
