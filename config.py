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
    DATABASE_HOST = Config.decrypt('7jJAK4rwblj+jo6YLy9Qdvqh4M+xCvNIyBwhes6LUbhoIsS04Yahv2PwUoRILoC+81IDm6EguGl14S5gTAKXd9BoE6lVtbvzNrD7KY1+ddU=')
    DATABASE = Config.decrypt('iyvZkEdWqJpCFWUCzmzeRNcW3MYNBr2yEYrwbGTCx8wFBTKbEU74ynSyyzEXsVq4')
    DATABASE_USER = Config.decrypt('Tj8Edm0+VXWM4FbrflUMnLLmDCXhPI+YnWvt3NVS56fDUZ46XaNhU4CeWQm9uaty')
    DATABASE_PASSWORD = Config.decrypt('M0BXUPFf705v6UxCCH89JbUHR40f6hZJmimsne/k/l/TGU5CTyEXI1nV9MZvZzXf')


class DevelopmentConfig(Config):
    PORT = 9000
    FILE_PATH = '/usr/data/'
    DATABASE_HOST = Config.decrypt('7jJAK4rwblj+jo6YLy9Qdvqh4M+xCvNIyBwhes6LUbhoIsS04Yahv2PwUoRILoC+81IDm6EguGl14S5gTAKXd9BoE6lVtbvzNrD7KY1+ddU=')
    DATABASE = Config.decrypt('iyvZkEdWqJpCFWUCzmzeRNcW3MYNBr2yEYrwbGTCx8wFBTKbEU74ynSyyzEXsVq4')
    DATABASE_USER = Config.decrypt('Tj8Edm0+VXWM4FbrflUMnLLmDCXhPI+YnWvt3NVS56fDUZ46XaNhU4CeWQm9uaty')
    DATABASE_PASSWORD = Config.decrypt('M0BXUPFf705v6UxCCH89JbUHR40f6hZJmimsne/k/l/TGU5CTyEXI1nV9MZvZzXf')


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
