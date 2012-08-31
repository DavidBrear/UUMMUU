import MySQLdb;
from userInfo import userInfo;
import AppConfig;

import Configuration;

class databaseConn:
    
    def __init__(self):
        userinfo = userInfo();
        ###connect to the database###
        database_str = userinfo.database+Configuration.getSetting('developmentDatabase', 'test');
        print database_str;
        self.conn = MySQLdb.connect(host=userinfo.server, user=userinfo.username, passwd=userinfo.password, db=database_str);
        self.cursor = self.conn.cursor();
    
    def exec_SP(self, str=''):
        if(len(AppConfig.sql_commands[str]) == ''):
            return '';
        else:
            self.cursor.execute(AppConfig.sql_commands[str]);
            return self.cursor.fetchall();
    
    def getDomainCount(self, args=''):
        #if this is a specific domain to crawl
        if len(args) > 1:
            return self.exec_SP('getDomainCountByUrl'%(sys.argv[1]));
        else:
            return self.exec_SP('getDomainCount');

    def commit(self):
        self.conn.commit();
        
    def close(self):
        self.conn.close();
