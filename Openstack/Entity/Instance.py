# -*- utf-8 : -*-
class Instance(object):
    def __init__(self, uuid, name):
        self.uuid = uuid
        self.name = name

    def get_uuid(self):
        return self.id

    def get_name(self):
        return self.name


if __name__ == "__main__":
    instance = Instance()
