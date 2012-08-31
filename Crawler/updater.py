import re;
import sys;
import MySQLdb;
import datetime;
from uummuuObjects import *;
import uummuuWord;
from uummuuWord import Document, add_document;
from time import sleep;
from userInfo import userInfo;

def modify_indexes(id, repos, desc, title):
    #get the words that are in the title
    in_title = {};
    
    #is there a space in the title?
    if(re.search('\s', title)):
        #split it up.
        for term in title.split():
            #set the boolean to true for this word
            in_title[term.lower()]=1;
    else:
        #else it's just one word, set its boolean value to 1
        in_title[title] = 1;
    #find the difference between the repository and the main file
    info_add, info_remove = uummuuWord.find_difference(id, repos, desc);
    
    #info remove is the list of words to remove from the index.
    for term in info_remove:
        
        try:
            #delete it from worddoc which is easy to do.
            cursor.execute("DELETE FROM sites_worddoc where word='%s' and doc_id = %d and occurrence = 1;" %(term, id));
            cursor.execute("UPDATE sites_worddoc set occurrence = occurrence-1 where word= '%s' and doc_id = %d;" %(term, id));
        except Exception, e:
            print 'line 25:', e;
            
        cursor.execute("SELECT invert_list from sites_index WHERE word='%s';" %term);
        res = cursor.fetchall();
        try:
            #rem - remove this id from the inverted list if one occurrence otherwise decrement the occurrences
            inverted_index = modify_inverted(id, res[0][0], in_title, term, 'rem');
        except Exception, e:
            print 'line 32:', e;
        try:
            if(len(inverted_index) == 0):
                cursor.execute("DELETE FROM sites_index where word = '%s';" %term);
            else:
                cursor.execute("UPDATE sites_index set invert_list = '%s' WHERE word = '%s';" %(inverted_index, term));
        except Exception, e:
            print 'line 39:', e;
            
    #info add is the list of words to add to the index
    for term in info_add:
        
        try:
            #see if it's in worddoc
            cursor.execute("SELECT id FROM sites_worddoc WHERE word = '%s' and doc_id = %d;" %(term, doc_id));
            res = cursor.fetchall();
            if(len(res)==0):
                #if it's not in there add it
                cursor.execute("INSERT INTO sites_worddoc(word, doc_id, occurrence,weight,in_title) values('%s', %d, 1,0,0);" %(term.lower(), doc_id));
            else:
                #if it's in there, increment it
                cursor.execute("UPDATE sites_worddoc set occurrence = occurrence+1 where word='%s' AND doc_id =%d;" %(term.lower(), doc_id));
        except Exception, e:
            print 'error line 49:', e;
            
        cursor.execute("SELECT invert_list from sites_index WHERE word = '%s';" %term.lower());
        res = cursor.fetchall();
        try:
            #we want to modify the inverted inext to add this word.
            inverted_index = modify_inverted(id, res[0][0], in_title, term, 'add');
        except Exception, e:
            print 'error line 55:', e;
            inverted_index = modify_inverted(id, '', in_title, term, 'add');
        try:
            #try to insert the word. If it's already in there. update its inverted list.
            cursor.execute("INSERT INTO sites_index(word, invert_list,freq, length, num_docs) values('%s', '%s', 0, 0, 0);" %(term.lower(), inverted_index));
        except Exception, e:
            cursor.execute("UPDATE sites_index set invert_list = '%s' WHERE word = '%s';" %(inverted_index, term.lower()));
    conn.commit();

def modify_inverted(id, inverted_index, in_title, term, opp):
    if(opp == 'add'):
        if(inverted_index == ''):
            try:
                return '<'+str(id)+',1,'+str(in_title[term.lower()])+'>';
            except Exception, e:
                print '70:', e;
                return '<'+str(id)+',1,0>';
        else:
            matches = re.search('(<'+str(id)+',(\d)*,[0|1]>)', inverted_index);
            print 'matches is:', matches;
            if(matches):
                try:
                    print 'replacing the word';
                    return inverted_index.replace(matches.groups()[0], '<'+str(id)+','+str(int(matches.groups()[1])+1)+','+str(in_title[term.lower()])+'>');
                except Exception, e:
                    print '80:', e;
                    return inverted_index.replace(matches.groups()[0], '<'+str(id)+','+str(int(matches.groups()[1])+1)+',0>');
            else:
                try:
                    return uummuuWord.add_to_index(inverted_index, id, 1, in_title[term.lower()]);
                except Exception, e:
                    print '86:', e;
                    return uummuuWord.add_to_index(inverted_index, id, 1, 0);
                
    else:
        matches = re.search('(<'+str(id)+',(\d)*,([0|1])>)', inverted_index);
        if (len(matches.groups()) == 0):
            return inverted_index;
        else:
            if(int(matches.groups()[1]) > 1):
                try:
                    return inverted_index.replace(matches.groups()[0], '<'+str(id)+','+str(int(matches.groups()[1])-1)+','+str(in_title[term.lower()])+'>');
                except Exception, e:
                    return inverted_index.replace(matches.groups()[0], '<'+str(id)+','+str(int(matches.groups()[1])-1)+',0>');
            else:
                return inverted_index.replace(matches.groups()[0], '');

def remove_index(doc_id, cursor):
    #get the information to remove it from the indexes
    cursor.execute("SELECT name, information FROM sites_htmlsite where id = %d;" %doc_id);
    res = cursor.fetchall();
    #call the modify indexes command with a blank for each to remove all the words from the index.
    modify_indexes(doc_id, res[0][1], '','');
    cursor.execute("UPDATE sites_htmlsite set name='', description='', information='' where id=%d;" %doc_id);
    cursor.execute("UPDATE sites_lira set link_list = '' WHERE id = %d;" %doc_id);

if __name__ == '__main__':
    doc_id = -1;
    userinfo = userInfo();
    
    counter = 0;
    num_pages_to_do = 20;
    
    ##am_i_blocked_counter is a counter to see if we have triggered some sort of block##
    am_i_blocked_counter = 0;
    
    '''
        NOTE: custom status code: 501 for UUMMUU index is an unsupported file type.
    '''
    
    crawl_domain = '';
    
    if len(sys.argv) > 1:
        crawl_domain = sys.argv[1];
        print 'crawling only:', crawl_domain;
    
    ###connect to the database###
    conn = MySQLdb.connect(host=userinfo.server, user=userinfo.username, passwd=userinfo.password, db=userinfo.database);
    cursor = conn.cursor();
    
    while True:
        index = {};
        total_unique_words = [];
        repository = {};
        ## a list of the links on this page ##
        link_list = [];
        ###set up the variables that will be put in the database. USE THESE IN THE SQL STATEMENT
        site = Site();
        
        
        try:
            if(crawl_domain != ''):
                sql = "SELECT url, id, domain FROM sites_sitequeue WHERE crawled = 1 and id > 0 AND status = 200 AND domain = '%s' ORDER BY last_crawl LIMIT 1;" %(crawl_domain);
                cursor.execute(sql);
            else:
                cursor.execute("SELECT url, id, domain FROM sites_sitequeue WHERE crawled = 1 AND id > 0 AND status = 200 ORDER BY last_crawl LIMIT 1;");
        except Exception,  e:
            print "There was an error selecting the information:", e;
            ###connect to the database###
            conn = MySQLdb.connect(host=userinfo.server, user=userinfo.username, passwd=userinfo.password, db=userinfo.database);
            cursor = conn.cursor();
            if(crawl_domain != ''):
                am_i_blocked_counter += 1;
            #this is to test to see if we have been blocked from this server. Happens when multiple 400 errors are received in a line.
            if(am_i_blocked_counter >= 20):
                print;
                print;
                print 'Looks like we got blocked from the site we were crawling.';
                break;
            continue;
        result = cursor.fetchall();
        
        try:
            site.url = result[0][0];
            print site.url, ' CRAWLING...';
            #site.url = 'http://localhost';
        except Exception,  e:
            print 'error 170:', e;
            break;
            
        myHTML = HTMLObject();
        links = [];
        doc_id = result[0][1];
        site.domain = result[0][2];
        
        try:
            if(not myHTML.getHTML(site.url)):
                cursor.execute('UPDATE sites_sitequeue set status=400 WHERE id = %d;' %doc_id);
                
                #remove the index for this element;
                remove_index(doc_id, cursor);
                
                conn.commit();
                conn.close();
                continue;
        except Exception,  e:
            cursor.execute('UPDATE sites_sitequeue set status=400 WHERE id = %d;' %doc_id);
            
            #remove the index for this element;
            remove_index(doc_id, cursor);
            
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
                cursor.execute("UPDATE sites_sitequeue set last_crawl = now() where id = %d;" %doc_id);
                cursor.execute("SELECT id FROM sites_sitequeue WHERE url = '%s';" %myHTML.redirected_url);
                redirected_to = cursor.fetchall();
                uummuuWord.append_word(link_list, redirected_to[0][0]);
            if(getDomain(site.url) != site.domain):
                site.domain = getDomain(site.url);
                cursor.execute("UPDATE sites_sitequeue SET domain = '%s' where id = %d;" %(site.domain,  doc_id));
        except Exception,  e:
            print 'error 216:', e;
            
            cursor.execute("UPDATE sites_sitequeue set status=300, crawled=1 where id = %d;" %(doc_id));
            conn.commit();
            continue;
        ##initialize the parser ##
        parser = myParser(myurl = site.url, domain = site.domain);
        
        try:
            ## run the parser on the html from this page.##
            parser.parse(myHTML.page);
        except Exception, e:
            print 'error 228:', e;
            cursor.execute("UPDATE sites_sitequeue SET status=400, crawled=1 WHERE id = %d;" %doc_id);
            
            #remove the index for this element;
            remove_index(doc_id, cursor);
            
            conn.commit();
            continue;
        
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
                print 'success line 250:',  e;
                
        links = parser.get_hyperlinks();
        
        for link in links:
            try:
                #take out spaces
                link = link.replace('\s', '%20'); 
                #take out single quotes
                link = link.replace('\'',  '');
                #take out www we don't want that
                link = link.replace('://www.',  '://');
                #not sure why this vvv works but it does...
                link_domain = getDomain(link);
                #if the link is to the domain then we don't care.
                if(len(link) < len(link_domain)+1):
                    #go to the top of the loop and start again
                    continue;
                #put it in the sitequeue
                cursor.execute("INSERT INTO sites_sitequeue(url,  crawled,  date_submitted,  domain,  status,  last_crawl) VALUES('%s',  0,  now(),  '%s', 200,  now());" %(link,  link_domain));
                #get it's id to add to LiRa
                cursor.execute("SELECT id from sites_sitequeue where url = '%s';" %link);
                conn.commit();
                curr_link = cursor.fetchall();
                #add this site's id to LiRa
                uummuuWord.append_word(link_list, curr_link[0][0]);
            except Exception,  e:
                #print 'success line 122:', e;
                cursor.execute("SELECT id from sites_sitequeue where url = '%s';" %link);
                curr_link = cursor.fetchall();
                uummuuWord.append_word(link_list, curr_link[0][0]);
        
        ## get the links from this page and put them into the database;##
        list_str = '';
        for link in link_list:
            if(link != doc_id):
                list_str += str(link) + ',';
        list_str = list_str[0:-1];
        cursor.execute("UPDATE sites_lira set link_list = '%s' where id = %d;" %(list_str, doc_id));
        data = parser.get_data();
        
        
        #set up a string to put all these words in.
        all_words = '';
        
        ## get the parsed data ##
        meta_info = parser.get_meta();
        
        try:
            if((meta_info['title'] is not None) and meta_info['title'] != ''):
                site.title = meta_info['title'];
                all_words += site.title;
        except:
            site.title = site.url;
        try:
            if((meta_info['description'] is not None) and meta_info['description'] != ''):
                site.description = meta_info['description'];
        except:
            site.description = 'no description';
            
        ## escape bad characters. Naughty code be gone! ##    
        site.description = site.description.replace("'", "\'");
        
        
        for sentence in data:
            if(len(all_words) < 4000):
                try:
                    sentence = unicode(sentence, 'utf8');
                    all_words = all_words + ' ' + sentence.encode('utf8');
                except Exception,  e:
                    try:
                        sentence = unicode(sentence, 'latin1');
                        all_words = all_words + ' ' + sentence.encode('latin1');
                    except Exception, e:
                        print "error adding sentence:", e;
                        print sentence;
        cursor.execute("SELECT name, information FROM sites_htmlsite where id = %d;" %doc_id);
        res = cursor.fetchall();
        modify_indexes(doc_id, res[0][1],all_words, site.title);
        site.title = site.title.replace("'",  "\'");
        cursor.execute("UPDATE sites_htmlsite set name='%s', information='%s', description='%s', last_indexed=now() where id = %d;" %(site.title, all_words, site.description, doc_id));
        try:
            cursor.execute("UPDATE sites_sitequeue set last_crawl = now() where id = %d;" %(doc_id));
            counter += 1;
        except Exception,  e:
            print 'error 327:', e;
        ##close out everything and prepare for exit ##
        conn.commit();
        sleep(.2525);
    #cursor.execute("DELETE FROM sites_sitequeue where status == 200;");
    conn.commit();
    conn.close();
