# libvirtconnect.py
from .config import LIBVIRT_CREDENTIALS
import libvirt

class Connection:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            username = LIBVIRT_CREDENTIALS.get('username', '')
            host = LIBVIRT_CREDENTIALS.get('host', '')

            if not username or not host:
                raise Exception('Invalid libvirt credentials')

            self.conn = libvirt.open(f"qemu+ssh://{username}@{host}/system")
            
            if self.conn is None:
                raise Exception('Failed to open connection to libvirt')

        except Exception as e:
            raise e

    # Rest of your Connection class implementation...
