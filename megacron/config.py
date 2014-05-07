try:
    import ConfigParser as cp
except ImportError:
    import configparser as cp

CONFIG_FILE = "/etc/megacron.conf"


def get_option(section, option):
    config = cp.RawConfigParser()
    config.read(CONFIG_FILE)

    return config.get(section, option)
