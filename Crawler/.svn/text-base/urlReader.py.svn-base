#created by David Brear
#March 12 2009
#this is the main portion of code.
import re;
import sys;
import MySQLdb;
import datetime;
from uummuuObjects import *;
from HTMLObject import HTMLObject;
import uummuuWord;
from uummuuWord import Document;
from time import sleep;
from userInfo import userInfo;
import AppConfig;
'''
* This Program is the main web crawler which will reside on each of the data servers
* In its initial implementation, it operates on the database associated with it and will fetch the information
* just for this server's sites.
* @author: David Brear
* @date: March 18 2008
* @version: 5.1.1 Nov 30th 2008
'''
def add_full_text(cursor, doc_id, site, full_text):
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
    
def create_stop_words():
    stop_list = [];
    stop_file = open('new_stop_words',  'r');
    for line in stop_file.readlines():
        line = line.replace('\n',  '');
        uummuuWord.append_word(stop_list,  line);
    return stop_list;

###           MAIN                   #############################
if __name__ == '__main__':
    
    counter = 0;
    doc_id = -1;
    limit = AppConfig.site_limit;
    userinfo = userInfo();
    
    ##am_i_blocked_counter is a counter to see if we have triggered some sort of block##
    am_i_blocked_counter = 0;
    
    '''
        NOTE: custom status code: 501 for UUMMUU index is an unsupported file type.
    '''
    
    crawl_domain = '';
    
    ###connect to the database###
    conn = MySQLdb.connect(host=userinfo.server, user=userinfo.username, passwd=userinfo.password, db=userinfo.database+AppConfig.development_status);
    cursor = conn.cursor();
    
    if len(sys.argv) > 1:
        crawl_domain = sys.argv[1];
        print 'crawling only:', crawl_domain;
        cursor.execute("SELECT pages_crawled from sites_domains where url = '%s';" %(crawl_domain));
        result = cursor.fetchall();
        counter = result[0][0];
    else:
        cursor.execute("SELECT url, pages_crawled FROM sites_domains order by pages_crawled limit 1;");
        result = cursor.fetchall();
        crawl_domain = result[0][0];
        counter = int(result[0][1]);
    
    dont_follow_links = find_RobotsTxt(crawl_domain);
    
    while counter < limit:
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
                cursor.execute(sql);
            else:
                cursor.execute("SELECT url, id, domain FROM sites_sitequeue WHERE crawled != 1 AND status = 200 ORDER BY id LIMIT 1;");
        except Exception,  e:
            print "There was an error selecting the information:", e;
            ###connect to the database###
            conn = MySQLdb.connect(host=userinfo.server, user=userinfo.username, passwd=userinfo.password, db=userinfo.database);
            cursor = conn.cursor();
            if(crawl_domain != ''):
                am_i_blocked_counter += 1;
            if(am_i_blocked_counter >= 20):
                print;
                print;
                print 'Looks like we got blocked from the site we were crawling.';
                break;
            continue;
        result = cursor.fetchall();
        try:
            site.url = result[0][0];
            dont_follow = False;
            for link in dont_follow_links:
                if(re.search(r'^'+link, site.url)):
                    print 'not going to:', site.url;
                    cursor.execute("UPDATE sites_sitequeue set crawled = 1, status=401 WHERE id = %d;" %result[0][1]);
                    dont_follow = True;
                    continue;
            if(dont_follow):
                continue;
        except Exception,  e:
            print 'error 60:', e;
            break;
        myHTML = HTMLObject();
        links = [];
        
        doc_id = result[0][1];
        site.domain = result[0][2];
        try:
            if(not myHTML.getHTML(site.url)):
                cursor.execute('UPDATE sites_sitequeue set status=400 WHERE id = %d;' %doc_id);
                conn.commit();
                conn.close();
                #cursor.excute("
                continue;
                
        except Exception,  e:
            cursor.execute('UPDATE sites_sitequeue set status=400 WHERE id = %d;' %doc_id);
            conn.commit();
            conn.close();
            continue;
        
        ##if we get here we are not blocked....yet.....reset the blocked counter if applicable##
        am_i_blocked_counter = 0;
        
        if(myHTML.content_type.split('/')[0].lower() != 'text'):
            print 'found something other than text. Found:', myHTML.content_type.split('/')[0].lower();
            cursor.execute("UPDATE sites_sitequeue set status=501 WHERE id = %d;" %doc_id);
            continue;
            
        try:
            if(myHTML.redirected_url != ''):
                print 'got a redirected url:', myHTML.redirected_url;
                
                redirected_domain = getDomain(myHTML.redirected_url);
                
                cursor.execute("INSERT INTO sites_sitequeue(url,crawled,domain,date_submitted, last_crawl, status) VALUES('%s',0,'%s',now(),now(),200);" %(myHTML.redirected_url,  redirected_domain));
                cursor.execute("SELECT id FROM sites_sitequeue WHERE url = '%s';" %myHTML.redirected_url);
                continue;
                redirected_to = cursor.fetchall();
                
                uummuuWord.append_word(link_list, redirected_to[0][0]);
                #cursor.execute("UPDATE sites_sitequeue set crawled = 1, status=300 where id = %d;" %(int(redirected_to[0][0]), doc_id));
            if(getDomain(site.url) != site.domain):
                site.domain = getDomain(site.url);
                cursor.execute("UPDATE sites_sitequeue SET domain = '%s' where id = %d;" %(site.domain,  doc_id));
        except Exception,  e:
            print 'error 85:', e;
            
            cursor.execute("UPDATE sites_sitequeue set status=300, crawled=1 where id = %d;" %(doc_id));
            conn.commit();
            continue;
        ##initialize the parser ##
        parser = myParser(myurl = site.url, domain = site.domain);
        parser.parse(myHTML.page);
        try:
            ## run the parser on the html from this page.##
            pass;
        except Exception, e:
            print 'error 126:', e;
            cursor.execute("UPDATE sites_sitequeue SET status=400, crawled=1 WHERE id = %d;" %doc_id);
            conn.commit();
            continue;
            
        try:
            total_styled_objs, total_term_count = main_style_parse(parser);
            got_word_data = True;
        except Exception, e:
            print 'error 206:', e;
            got_word_data = False;
        
        ## check to see if this page has a meta refresh ##
        if(parser.has_meta_refresh and parser.meta_refresh_url != ''):
            try:
                refreshed_url = makeURL(site.url,  parser.meta_refresh_url);
                
                refreshed_domain = getDomain(refreshed_url);
                
                cursor.execute("INSERT INTO sites_sitequeue(url,crawled,domain,date_submitted, last_crawl, status) VALUES('%s',0,'%s',now(),now(),200);" %(refreshed_url,  refreshed_domain));
                cursor.execute("SELECT id FROM sites_sitequeue WHERE url = '%s';" %refreshed_url);
                
                print 'executed the renaming of meta refresh...', ;
                conn.commit();
                
                print 'done';
                refreshed_url_id = cursor.fetchall()[0][0];
                
                uummuuWord.append_word(link_list, refreshed_url_id);
            except Exception, e:
                print 'success line 108:',  e;
        links = parser.get_hyperlinks();
        for link in links:
            try:
                link = link.replace('\s', '%20');
                link = link.replace('\'',  '');
                link = link.replace('://www.',  '://');
                #not sure why this vvv works but it does...
                link_domain = getDomain(link);
                if(len(link) < len(link_domain)+1):
                    link += "/";
                cursor.execute("INSERT INTO sites_sitequeue(url,  crawled,  date_submitted,  domain,  status,  last_crawl) VALUES('%s',  0,  now(),  '%s', 200,  now());" %(link,  link_domain));
                cursor.execute("SELECT id from sites_sitequeue where url = '%s';" %link);
                conn.commit();
                curr_link = cursor.fetchall();
                uummuuWord.append_word(link_list, curr_link[0][0]);
            except Exception,  e:
                #print 'success line 122:', e;
                cursor.execute("SELECT id from sites_sitequeue where url = '%s';" %link);
                curr_link = cursor.fetchall();
                uummuuWord.append_word(link_list, curr_link[0][0]);
        
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
                if(len(link) < len(link_domain)+1):
                    link += "/";
                cursor.execute("INSERT INTO sites_sitequeue(url,  crawled,  date_submitted,  domain,  status,  last_crawl) VALUES('%s',  0,  now(),  '%s', 200,  now());" %(link,  link_domain));
                cursor.execute("SELECT id from sites_sitequeue where url = '%s';" %link);
                conn.commit();
                curr_link = cursor.fetchall();
            except Exception,  e:
                #print 'success line 122:', e;
                cursor.execute("SELECT id from sites_sitequeue where url = '%s';" %link);
                curr_link = cursor.fetchall();
        
        ## get the links from this page and put them into the database;##
        list_str = '';
        for link in link_list:
            if(link != doc_id):
                list_str += str(link) + ',';
        list_str = list_str[0:-1];
        cursor.execute("INSERT INTO sites_lira(id, link_list) VALUES(%d,  '%s');" %(doc_id,  list_str));        
        
        #set up a string to put all these words in.
        all_words = '';
        
        ## get the parsed data ##
        meta_info = parser.get_meta();
        
        all_words = parser.full_text;
        
        try:
            if((meta_info['title'] is not None) and meta_info['title'] != ''):
                site.title = meta_info['title'];
                all_words += site.title + " ";
        except:
            site.title = site.url;
        try:
            if((meta_info['description'] is not None) and meta_info['description'] != ''):
                site.description = meta_info['description'];
        except:
            site.description = 'no description';
            
        ## escape bad characters. Naughty code be gone! ##    
        site.description = site.description.replace("'", "\'");
        
        site.title = site.title.replace("'", "\'");
        
        #did we get the word data?
        if(got_word_data):
            #create the stop list
            stop_words = create_stop_words();
            
            title_terms = {};
            for term in parser.get_title().split(' '):
                if(re.search(r'[a-z|0-9|A-Z]*', term)):
                    title_terms[term.lower()] = 1;
            for key in total_styled_objs.keys():
                try:
                    insert_into_db(cursor, doc_id, key, total_styled_objs[key], total_term_count[key.lower()], title_terms[key.lower()]);
                except Exception, e:
                    insert_into_db(cursor, doc_id, key, total_styled_objs[key], total_term_count[key.lower()], 0);
                        
            #add the description to the database
            add_full_text(cursor, doc_id, site, all_words + parser.get_full_text());
            
        #update the crawled status of this entry in the database.
        try:
            cursor.execute("UPDATE sites_htmlsite set description = '%s', information = '%s' where id = %d;" %(site.description, all_words, doc_id));
            cursor.execute("UPDATE sites_sitequeue set crawled = 1 where id = %d;" %(doc_id));
            cursor.execute("UPDATE sites_domains set pages_crawled = pages_crawled + 1 WHERE url = '%s';" %site.domain);
            counter = counter + 1;
        except Exception,  e:
            print 'error 149:', e;
            
        ##close out everything and prepare for exit ##
        conn.commit();
    #cursor.execute("DELETE FROM sites_sitequeue where status == 200;");
    conn.commit();
    conn.close();
