import logging;
import AppConfig;
from datetime import datetime;
import os;

class myLogger:
    
    def __init__(self, moduleName="", name='UUMMUU Crawler', format='logging', folder='RUN_DATA'):
        
        month_folder = (AppConfig.logging_template %(datetime.today().strftime('%Y%m')));
        self.ensure_dir(month_folder);
        fileName = "";
        if(format == 'data'):
            folder = moduleName.upper();
        self.ensure_dir(month_folder + '\\' + folder);
        if(moduleName != ""):
            fileName = month_folder + '\\' + folder + "\\" + moduleName + "_" + datetime.today().strftime('%Y%m%d') + '.log';
        else:
            fileName = month_folder + '\\' + folder + "\\" + datetime.today().strftime('%Y%m%d')+ '.log';
        self.log_name = (fileName);
        self.logger = logging.getLogger(name)
        hdlr = logging.FileHandler(self.log_name)
        if(format == 'data'):
            formatter = logging.Formatter("%(message)s");
        else:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s");
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def ensure_dir(self, f):
        if not os.path.exists(f):
            os.makedirs(f);
    
    def debug(self, str):
        self.logger.debug(str);
    
    def warning(self, str):
        self.logger.warning(str);
    
    def info(self, str):
        self.logger.info(str);
        
    def critical(self, str):
        self.logger.critical(str);
    
    def error(self, str):
        self.logger.error(str);
