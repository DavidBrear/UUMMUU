import myLogger;
import Configuration;
import datetime;
from databaseConn import databaseConn;
#### GLOBAL DATA######

myDBConn = databaseConn();

#### MAIN METHOD ####
if __name__ == '__main__':
    
    _oLog = myLogger.myLogger(moduleName="url_assign_log");
    _oLog.info("Started parsing out new URLs");
    
    now = datetime.datetime.now();
    date = now.strftime('%Y%m%d');
    if(Configuration.getSetting('override_date',  '') != ''):
        date = Configuration.getSetting('override_date',  date);
    try:
        datetime.strptime(date, "%Y%m%d");
    except:
        _oLog.error("Parsing date is not a valid date. Must be in format: yyyyMMdd");
    _oLog.info("Running URL Assign on date: " + str(date));
    file = Configuration.getSetting("url_handoff", "C:\\UUMMUU_Code\\Logs\\"+str(date)[0:6]+"\\LINKED_URLS_LOG\\linked_urls_log_"+str(date)+'.log');
    
    try:
        opened_file = open(file);
    except:
        _oLog.info("File is not ready to be parsed. Exiting...");
        exit();
    
    for line in opened_file.readlines():
        try:
            _oLog.info("adding url to crawl list");
            parts = line.split('\t');
            sql_statement = "INSERT INTO sites_sitequeue(url, domain, crawled, status, date_submitted, last_crawl) values('"+parts[1]+"', '"+parts[2]+"', 0, 200, '"+str(now)+"', '"+str(now)+"');";
            print "sql statement is: " + sql_statement;
            myDBConn.cursor.execute(sql_statement);
        except Exception, exp:
            _oLog.error("Error adding record to database. " + str(exp));
