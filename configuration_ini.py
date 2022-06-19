import configparser, os

def get_data(file_path):
    file_path = os.path.join(*file_path)

    config = configparser.ConfigParser()
    data = config.read(file_path)
    return config

def set_data(file_path, category, variable, value):
    file_path = os.path.join(*file_path)

    config = configparser.ConfigParser()
    config.read(file_path)
    config[category][variable] = value
    config.write(open(file_path,'w'))