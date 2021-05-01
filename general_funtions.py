import yaml, os  
def get_configurations():
    directory_path = r'%s' % os.getcwd().replace('\\','//')
    
    configuration_file=directory_path + "//configuration.yaml"
    with open(configuration_file) as file:
        config_yaml = yaml.load(file, Loader=yaml.FullLoader)
    
    return config_yaml