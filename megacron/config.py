import ConfigParser

CONFIG_FILE = "/etc/megacron.conf"


def get_option(section, option):
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)

    return config.get(section, option)
