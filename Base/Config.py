import configparser


class Config:

    def __init__(self, file_name:str):
        self.config = configparser.ConfigParser()
        self.config.read(file_name)

    def Host(self)->str:
        host:str="";
        if(None != self.config):host = self.config['Connection']['user']
        return(host);

    def User(self)->str:
        user:str="";
        if(None != self.config):user = self.config['Connection']['user']
        return(user);