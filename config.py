# -*- coding: utf-8 -*-


class Config(object):
    def __init__(self, **configs):
        super(Config, self).__setattr__("data", configs)

    def __getattr__(self, name):
        return self.data.get(name, None)

    def __setattr__(self, name, value):
        self.data[name] = value


if __name__ == '__main__':
    config = Config(bind="0.0.0.0", port=9999, listen=1024)
