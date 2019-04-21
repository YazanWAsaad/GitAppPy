import configparser


class ConfigCls:

    def __init__(self, file_name:str):
        self.config = configparser.ConfigParser()
        self.config.read(file_name)

    def DbHost(self)->str:
        host:str="";
        if(None != self.config):host = self.config['DbConnection']['Host']
        return(host);

    def DbUser(self)->str:
        user:str="";
        if(None != self.config):user = self.config['DbConnection']['user']
        return(user);

    def DbPassword(self)->str:
        password:str="";
        if(None != self.config):password = self.config['DbConnection']['Password']
        return(password);




    def GitUser(self)->str:
        user:str="";
        if(None != self.config):user = self.config['GitConnection']['user']
        return(user);

    def GitPassword(self)->str:
        password:str="";
        if(None != self.config):password = self.config['GitConnection']['Password']
        return(password);