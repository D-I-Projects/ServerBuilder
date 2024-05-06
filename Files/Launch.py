import configparser
import psutil
import platform

class config:
    def __init__(self):

        self.configparser = configparser
        self.platform = platform

        self.my_system = platform.uname()

        self.RAM = str(round(psutil.virtual_memory().total / (1024.**3)))

    def write_data(self):

        config = self.configparser.ConfigParser()
        config['Hardware'] = {'RAM': self.RAM}

        config['System'] = {'System': self.my_system.system, 'Release': self.my_system.release, 'Version': self.my_system.version, 'Machine': self.my_system.machine, 'Processor': self.my_system.processor, 'Python-Version': self.platform.python_version()}

        config['Advanced'] = {'Full-RAM': False, 'Developer': False}

        with open("config.ini", 'w') as configfile:
            config.write(configfile)

    def get_data(self, section, key):
        return config[section][key]