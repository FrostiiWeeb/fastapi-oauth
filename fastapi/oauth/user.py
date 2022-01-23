from typing import *

class User(object):
    def __init__(self, data : dict) -> None:
        self.name = data['username']
        self.id = int(data['id'])
        self.discriminator = data['discriminator']
        self.avatar = data['avatar']
        self.banner = data.get('banner', None)
        self.accent_colour = data.get('accent_color', None)
        self.public_flags = data.get('public_flags', 0)
        self.bot = data.get('bot', False)
        self.system = data.get('system', False)