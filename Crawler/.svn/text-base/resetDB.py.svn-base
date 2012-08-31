import MySQLdb;
from userInfo import userInfo;
import AppConfig;

'''
*This is a file for resetting the database
* This file should only be run in extreme cases after the initial start of the application
* This program will completely truncate the database and add one url back into the sitequeue.
* This url can be updated below.
'''

if __name__ == '__main__':
    #create the user
    userinfo = userInfo();
    #connect to the database.
    conn = MySQLdb.connect(host=userinfo.server, user=userinfo.username, passwd=userinfo.password, db=userinfo.database+AppConfig.development_status);
    #get the cursor for this database
    cursor = conn.cursor();
    #make sure that this person wants to reset the database
    print 'are you sure? Y/N';
    if raw_input().lower()[0] == 'y':
        #this person is sure so we're going to reset the database.
        print 'resetting database...', ;
        try:
            #this is the site that is going to be added after we're done.
            site = AppConfig.reset_site;
            #lira_transposed is the transposition of the site links
            cursor.execute("TRUNCATE sites_lira_transposed;");
            #htmlsite is the database containing all the words for each site.
            #this is the repository
            cursor.execute("TRUNCATE sites_htmlsite;");
            #sitequeue is the table that holds all the urls to be crawled.
            cursor.execute("TRUNCATE sites_sitequeue;");
            #put back the one url to start with
            cursor.execute("INSERT INTO sites_sitequeue(url, crawled, domain, last_crawl, date_submitted, status) VALUES('"+site+ "', 0, '"+site+"', now(), now(), 200);");
            #domains is the list of domains to crawl
            cursor.execute("TRUNCATE sites_domains;");
            #put back this site's domain
            cursor.execute("INSERT INTO sites_domains(url, pages_crawled) values('"+site+"', 0);");
            #worddoc is the one-to-one word to document index
            cursor.execute("TRUNCATE sites_worddoc;");
            #lira is the site link list
            cursor.execute("TRUNCATE sites_lira;");
            #index is the inverted one to many index
            cursor.execute("TRUNCATE sites_index;");
            #put back a default site url for 400 sites.
            cursor.execute("INSERT INTO sites_sitequeue(id, url, domain, crawled, status, date_submitted, last_crawl) VALUES(-1, 'none', 'none', 1, 200, now(), now());");
            cursor.execute("INSERT INTO sites_htmlsite(id, name, description, information, updated, indexed, last_indexed, sitequeue_id) VALUES(-1, 'none', 'none', 'none', now(), 1, now(), -1);");
            
            print 'done.';
        except Exception,  e:
            print 'error:', e;
        conn.commit();
    conn.close();
