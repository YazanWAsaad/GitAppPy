from Base import Files
from Source import research


text = Files.TextRead(Files.WorkingDir()+'Config.ini');
print(text);

config:list = Files.IniRed(Files.WorkingDir()+'Config.ini');
print(config['host']);


research.crawl(5)