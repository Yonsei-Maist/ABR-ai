from lib.crypto import AESCipher
import sys


class Config(object):
    VERSION = 0.1
    CIPHER = AESCipher(sys.argv[1])

    @staticmethod
    def decrypt(str_data):
        return Config.CIPHER.decrypt(str_data)


class LocalConfig(Config):
    PORT = 9000
    FILE_PATH = '/Users/gwonchan-u/'
    DATABASE_HOST = Config.decrypt('g75HCbNFvcsBbZTyE5lxxivLSWVED5EW/a3WCvTKu7QB2L+O3V0xGRnRuJ7QfMbH')
    DATABASE = Config.decrypt('iyvZkEdWqJpCFWUCzmzeRNcW3MYNBr2yEYrwbGTCx8wFBTKbEU74ynSyyzEXsVq4')
    DATABASE_USER = Config.decrypt('Sfq+bb38EuBgsLKRuP+GpqzAezwQPKXl02UsiwQuWgq5MkEGToVVFO7nqHNvusiM')
    DATABASE_PASSWORD = Config.decrypt('VLI/oi5AznaBGjyt0Rn2QsO7D7ccX+iUklAdSbE9+sFumcj8AuP8gqGV/ffWTxyT')


class DevelopmentConfig(Config):
    PORT = 9000
    FILE_PATH = '/usr/data/'
    DATABASE_HOST = Config.decrypt('g75HCbNFvcsBbZTyE5lxxivLSWVED5EW/a3WCvTKu7QB2L+O3V0xGRnRuJ7QfMbH')
    DATABASE = Config.decrypt('iyvZkEdWqJpCFWUCzmzeRNcW3MYNBr2yEYrwbGTCx8wFBTKbEU74ynSyyzEXsVq4')
    DATABASE_USER = Config.decrypt('Sfq+bb38EuBgsLKRuP+GpqzAezwQPKXl02UsiwQuWgq5MkEGToVVFO7nqHNvusiM')
    DATABASE_PASSWORD = Config.decrypt('VLI/oi5AznaBGjyt0Rn2QsO7D7ccX+iUklAdSbE9+sFumcj8AuP8gqGV/ffWTxyT')


config_by_name = dict(dev=DevelopmentConfig, local=LocalConfig)

success = {
    "version": Config.VERSION,
    "result": "success"
}

fail = {
    "version": Config.VERSION,
    "result": "fail"
}


def success_msg(data=None):
    return dict(success, **{"data": data})


def fail_msg(message):
    return dict(fail, **{"message": message})
