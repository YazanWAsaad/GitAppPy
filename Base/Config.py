import configparser
from GitAppPy.Base import Files





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



    def WordsDomain(self)->str:
        domain_words:str="";
        if(None != self.config):
            file_name = self.config['WordFiles']['WordsDomain']
            words = Files.TextReadLines(file_name);
            return(words);

    def WordsAspects(self)->str:
        aspects_words:str="";
        if(None != self.config):
            file_name = self.config['WordFiles']['WordsAspects'];
            words = Files.TextReadLines(file_name);
            return(words);