import sys;
import os;
import sgmllib;

AppSettings = {};

configFile = 'Config\\' + sys.argv[0].split('.')[0]+'.config';

def getSetting(name, defVal):
    try:
        ret = AppSettings[name];
        return ret;
    except:
        return defVal;
        
#####    Get objects #####
class configParser(sgmllib.SGMLParser):
    def parse(self, s):
        self.feed(s);
        self.close();

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose);
        self.insideAppSettings = False;
        
    def unknown_starttag(self, tag, attributes):
        pass;
    def start_appsettings(self, attributes):
        self.insideAppSettings = True;
    
    def start_key(self, attributes):
        id = '';
        value = '';
        if (self.insideAppSettings):
            for att in attributes:
                if att[0] == 'id':
                    id = att[1];
                elif att[0] == 'value':
                    value = att[1];
            if(id != '' and value != ''):
                AppSettings[id] = value; 

if(os.path.exists(configFile)):
    p = configParser();
    if(os.path.exists('Config\\Global.config')):
        f = open('Config\\Global.config');
        p.parse(f.read());
        f.close();  
    f = open(configFile);
    p.parse(f.read());
    f.close();
