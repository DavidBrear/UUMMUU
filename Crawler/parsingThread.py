import threading;
from uummuuObjects import *;
from databaseConn import databaseConn;
import uummuuWord;

import myLogger;

import datetime;
import time;

class parseThread(threading.Thread):
    
    
    def __init__(self, doc_id=-1,  siteurl ='', domain=''):
        threading.Thread.__init__(self);
        self.site = Site();
        self.site.url = siteurl;
        self.site.domain = domain;
        self.doc_id = doc_id;
        self.myDBConn = databaseConn();
    
    def setHTML(self, html):
        self.html = html;
        
    def passStopWords(self, stop_words):
        self.stop_words = stop_words;
    
    def run(self):
        logger = myLogger.myLogger("parsing_thread_log");
        linkedUrls = myLogger.myLogger("linked_urls_log", format='data');
        
        parser = myParser(myurl = self.site.url, domain = self.site.domain);
        parser.parse(self.html);
        try:
            ## run the parser on the html from this page.##
            pass;
        except Exception, e:
            logger.error('urlReader line 188:'+str(e));
            self.myDBConn.cursor.execute("UPDATE sites_sitequeue SET status=400, crawled=1 WHERE id = %d;" %doc_id);
            return;

        try:
            total_styled_objs, total_term_count = main_style_parse(parser);
            got_word_data = True;
        except Exception, e:
            logger.error('urlReader line 197:' + str(e));
            got_word_data = False;
        
        ## check to see if this page has a meta refresh ##
        if(parser.has_meta_refresh and parser.meta_refresh_url != ''):
            try:
                refreshed_url = makeURL(self.site.url,  parser.meta_refresh_url);
                
                refreshed_domain = getDomain(refreshed_url);
                
                self.myDBConn.cursor.execute("INSERT INTO sites_new_urls(url) VALUES('%s');" %(refreshed_url));
                linkedUrls.info(self.site.url + "\t" + refreshed_url + "\t" + refreshed_domain);
                
            except Exception, e:
                logger.error(str(e));
                pass;
        links = parser.get_hyperlinks();
        for link in links:
            try:
                link = link.replace('\s', '%20');
                link = link.replace('\'',  '');
                link = link.replace('://www.',  '://');
                #not sure why this vvv works but it does...
                link_domain = getDomain(link);
                if(len(link) == len(link_domain) and link[-1] != '/'):
                    link += "/";
                self.myDBConn.cursor.execute("INSERT INTO sites_new_urls(url) VALUES('%s');" %(link));
                linkedUrls.info(self.site.url + "\t" + link + "\t" + link_domain);
            except Exception,  e:
                logger.error(str(e));
                pass;
        
        ##add the links for pages which this page has no follow links
        links = parser.get_no_follow_links();
        ##go through all the links.
        
        for link in links:
            try:
                link = link.replace('\s', '%20');
                link = link.replace('\'',  '');
                link = link.replace('://www.',  '://');
                #not sure why this vvv works but it does...
                link_domain = getDomain(link);
                if(len(link) == len(link_domain) and link[-1] != '/'):
                    link += "/";
                self.myDBConn.cursor.execute("INSERT INTO sites_new_urls(url) VALUES('%s');" %(link));
            except Exception,  e:
                logger.error(str(e));
                print e;
        
        ## get the links from this page and put them into the database;##
        '''
        ***************THIS PART SHOULD BE READDED WHEN IT CAN BE IMPLEMENTED*************************
        
        list_str = '';
        for link in link_list:
            if(link != self.doc_id):
                list_str += str(link) + ',';
        list_str = list_str[0:-1];
        self.myDBConn.cursor.execute("INSERT INTO sites_lira(id, link_list) VALUES(%d,  '%s');" %(self.doc_id,  list_str));        
        '''
        #set up a string to put all these words in.
        all_words = '';
        
        ## get the parsed data ##
        meta_info = parser.get_meta();
        
        all_words = parser.full_text;
        try:
            if((meta_info['title'] is not None) and meta_info['title'] != ''):
                self.site.title = meta_info['title'];
                all_words += self.site.title + " ";
        except:
            self.site.title = self.site.url;
        try:
            if((meta_info['description'] is not None) and meta_info['description'] != ''):
                self.site.description = meta_info['description'];
        except:
            self.site.description = 'no description';
            
        ## escape bad characters. Naughty code be gone! ##
        self.site.description = self.site.description.replace("'", "\'");
        
        self.site.title = self.site.title.replace("'", "\'");
        #did we get the word data?
        if(got_word_data):
            #create the stop list
            
            title_terms = {};
            for term in parser.get_title().split(' '):
                if(re.search(r'[a-z|0-9|A-Z]*', term)):
                    title_terms[term.lower()] = 1;
            for key in total_styled_objs.keys():
                try:
                    insert_into_db(self.myDBConn.cursor, self.doc_id, key, total_styled_objs[key], total_term_count[key.lower()], title_terms[key.lower()]);
                except Exception, e:
                    insert_into_db(self.myDBConn.cursor, self.doc_id, key, total_styled_objs[key], total_term_count[key.lower()], 0);
                self.myDBConn.commit();
            #add the description to the database
            self.add_full_text(self.myDBConn.cursor, self.doc_id, self.site, all_words + parser.get_full_text());
        #update the crawled status of this entry in the database.
        try:
            self.myDBConn.cursor.execute("UPDATE sites_htmlsite set description = '%s', information = '%s' where id = %d;" %(self.site.description, all_words, self.doc_id));
            self.myDBConn.cursor.execute("UPDATE sites_sitequeue set crawled = 1 where id = %d;" %(self.doc_id));
            self.myDBConn.cursor.execute("UPDATE sites_domains set pages_crawled = pages_crawled + 1 WHERE url = '%s';" %self.site.domain);
        except Exception,  e:
            logger.error('error 149:' + str(e));
        self.myDBConn.commit();
        self.myDBConn.close();
    
    def add_full_text(self, cursor, doc_id, site, full_text):
        data = full_text;
        all_words = "";
        for sentence in data.split(' '):
            if(len(all_words) < 4000):
                try:
                    all_words = unicode(sentence, 'ascii');
                    #all_words = all_words + ' ' + sentence.encode('utf8');
                except Exception,  e:
                    new_sentence = '';
                    for word in sentence.split(' '):
                        try:
                            new_sentence += unicode(word, 'ascii');
                        except Exception, e:
                            pass;
                    all_words += " " + new_sentence;
                    '''
                    try:
                        sentence = unicode(sentence, 'latin1');
                        all_words = all_words + ' ' + sentence.encode('latin1');
                    except Exception, e:
                        print "error adding sentence:", e;
                        print sentence;
                    '''
        try:
            all_words = all_words.replace("'", "");
            all_words = re.sub('\s[\s]*', ' ',  all_words);
            cursor.execute("INSERT INTO sites_htmlsite(id, name, description, information, updated, last_indexed, indexed, sitequeue_id) VALUES (%d, '%s', '%s', '%s', '%s', '%s', 0, %d);" %(doc_id,  site.title, site.description, all_words, str(datetime.datetime.now()),str(datetime.datetime.now()),  doc_id));
        except Exception, e:
            print 'error line 250:', e;
