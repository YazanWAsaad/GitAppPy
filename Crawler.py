from Base import Files
from Base import Config

from Source import research


#text = Files.TextRead(Files.WorkingDir()+'Config.ini');

config:list = Files.IniRed(Files.WorkingDir()+'Config.ini');
#print(config['host']);


research.crawl(5)