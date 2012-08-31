#created by David Brear
#March 12 2009
#this is the main portion of code.
import re;
import sys;
import datetime;
from uummuuObjects import *;
from HTMLObject import HTMLObject;
import uummuuWord;
from uummuuWord import Document;
from time import sleep;
import AppConfig;

import myLogger;
from parsingThread import parseThread;
from databaseConn import databaseConn;

'''
* This Program is the main web crawler which will reside on each of the data servers
* In its initial implementation, it operates on the database associated with it and will fetch the information
* just for this server's sites.
* @author: David Brear
* @date: March 18 2008
* @version: 6.0.1 May 24 2009
'''
    
def create_stop_words():
    stop_list = [];
    stop_file = open('new_stop_words',  'r');
    for line in stop_file.readlines():
        line = line.replace('\n',  '');
        uummuuWord.append_word(stop_list,  line);
    return stop_list;

###           MAIN                   #############################
if __name__ == '__main__':
    
    pageCounter = 0;
    doc_id = -1;
    limit = AppConfig.site_limit;
    ##am_i_blocked_counter is a counter to see if we have triggered some sort of block##
    am_i_blocked_counter = 0;
    
    #The Thread List
    myArr = [];
    
    #create stop_words
    stop_words = create_stop_words();
    
    '''
        NOTE: custom status code: 501 for UUMMUU index is an unsupported file type.
    '''
    myDBConn = databaseConn();
    result = myDBConn.getDomainCount(sys.argv);
    try:
        crawl_domain = result[0][0];
        counter = int(result[0][1]);
    except:
        logger.error('there was an error getting any site domains to crawl');
    
    #get a list of the links we are to ignore for this domain
    dont_follow_links = find_RobotsTxt(crawl_domain);
    
    #start a logger to keep track of what breaks.
    logger = myLogger.myLogger(moduleName="url_reader_log");
    
    #make sure we do not crawl too many pages for a single domain.
    while pageCounter < limit:
        #an index of all the words.
        index = {};
        total_unique_words = [];
        repository = {};
        ## a list of the links on this page ##
        link_list = [];
        ###set up the variables that will be put in the database. USE THESE IN THE SQL STATEMENT
        site = Site();
        
        try:
            if(crawl_domain != ''):
                sql = "SELECT url, id, domain FROM sites_sitequeue WHERE crawled != 1 AND status = 200 AND domain = '%s' ORDER BY id LIMIT 1;" %(crawl_domain);
                
                myDBConn.cursor.execute(sql);
            else:
                myDBConn.cursor.execute("SELECT url, id, domain FROM sites_sitequeue WHERE crawled != 1 AND status = 200 ORDER BY id LIMIT 1;");
        except Exception,  e:
            logger.error("line 105: There was an error selecting the information: "+str(e));
            ###connect to the database###
            myDBConn = databaseConn();
            if(crawl_domain != ''):
                am_i_blocked_counter += 1;
            if(am_i_blocked_counter >= 20):
                logger.critical('Looks like we got blocked from the site we were crawling.');
                break;
            continue;
        result = myDBConn.cursor.fetchall();
        try:
            site.url = result[0][0];
            dont_follow = False;
            for link in dont_follow_links:
                if(re.search(r'^'+link, site.url)):
                    print 'not going to:', site.url;
                    myDBConn.cursor.execute("UPDATE sites_sitequeue set crawled = 1, status=401 WHERE id = %d;" %result[0][1]);
                    dont_follow = True;
                    continue;
            if(dont_follow):
                continue;
        except Exception,  e:
            logger.info('sleeping for 10 seconds to find if there are more sites coming.');
            sleep(10);
            myDBConn.commit();
            myDBConn.close();
            myDBConn = databaseConn();
            continue;
            #break;
        myHTML = HTMLObject();
        links = [];
        
        doc_id = result[0][1];
        site.domain = result[0][2];
        try:
            if(not myHTML.getHTML(site.url)):
                myDBConn.cursor.execute('UPDATE sites_sitequeue set status=400 WHERE id = %d;' %doc_id);
                continue;
                
        except Exception,  e:
            myDBConn.cursor.execute('UPDATE sites_sitequeue set status=400 WHERE id = %d;' %doc_id);
            continue;
        
        ##if we get here we are not blocked....yet.....reset the blocked counter if applicable##
        am_i_blocked_counter = 0;
        
        if(myHTML.content_type.split('/')[0].lower() != 'text'):
            logger.info('found something other than text. Found:', myHTML.content_type.split('/')[0].lower());
            myDBConn.cursor.execute("UPDATE sites_sitequeue set status=501 WHERE id = %d;" %doc_id);
            continue;
            
        try:
            if(myHTML.redirected_url != ''):
                logger.info('got a redirected url:', myHTML.redirected_url, 'from:', url);
                
                redirected_domain = getDomain(myHTML.redirected_url);
                
                myDBConn.cursor.execute("INSERT INTO sites_new_urls(url) VALUES('%s');" %(myHTML.redirected_url));
                continue
            if(getDomain(site.url) != site.domain):
                site.domain = getDomain(site.url);
                myDBConn.cursor.execute("UPDATE sites_sitequeue SET domain = '%s' where id = %d;" %(site.domain,  doc_id));
        except Exception,  e:
            logger.error('urlReader: line 176:', e);
            
            myDBConn.cursor.execute("UPDATE sites_sitequeue set status=300, crawled=1 where id = %d;" %(doc_id));
            continue;
        
        #crawler has gotten this far, it must be a valid url. Say it is already used.
        try:
            myDBConn.cursor.execute("UPDATE sites_sitequeue set status=200, crawled=1 where id = %d;" %(doc_id));
            myDBConn.commit();
            pageCounter += 1;
        except Exception, e:
            logger.critical("There was an error setting the url to read"+str(e));
        
        ##initialize the parser threads ##

        counter = AppConfig.ThreadLimit;
        while counter >= AppConfig.ThreadLimit:
            counter = 0;
            for x in (0, AppConfig.ThreadLimit):
                try:
                    if myArr[x].isAlive():
                        counter += 1;
                except Exception, e:
                    pass;
            if counter >= AppConfig.ThreadLimit:
                logger.info("sleeping for 10 seconds because all the threads are filled");
                sleep(10);
        for x in xrange(0, AppConfig.ThreadLimit):
            try:
                if myArr[x].isAlive():
                    print 'thread', x, 'is still alive';
                    continue;
                else:
                    logger.info('thread ' + str(x)+ ' is ready to be given a new job');
                    myArr[x] = parseThread(doc_id, site.url, site.domain);
                    #myHTML.getHTML(site.url);
                    myArr[x].setHTML(myHTML.getPage());
                    myArr[x].passStopWords(stop_words);
                    myArr[x].start();
                    break;
            except Exception, e:
                print e;
                logger.info("Starting new thread number: " + str(len(myArr)));
                myArr.append(parseThread(doc_id, site.url, site.domain));
                #myHTML.getHTML(site.url);
                myArr[len(myArr)-1].setHTML(myHTML.getPage());
                myArr[len(myArr)-1].passStopWords(stop_words);
                myArr[len(myArr)-1].start();
                break;
