import MySQLdb;
import urllib2;
import socket;
import sgmllib;
import re;
from userInfo import userInfo;
from uummuuWord import in_array;
import time;
from math import sqrt;

if __name__ == "__main__":
    userinfo = userInfo();
    conn = MySQLdb.connect(host=userinfo.server, user=userinfo.username, passwd=userinfo.password, db=userinfo.database);
    cursor = conn.cursor();
    cursor.execute("SELECT count(id) FROM sites_lira WHERE link_list = '';");
    res = cursor.fetchall();
    numDangling = int(res[0][0]);
    
    cursor.execute("SELECT MAX(id),COUNT(id) FROM sites_lira;");
    res = cursor.fetchall();
    count = res[0][0];
    number_pages = int(res[0][1]);
    count += 1;
    
    cursor.execute("UPDATE sites_lira_transposed SET inlinks='';");
    
    for x in xrange(0, count):
        try:
            cursor.execute("SELECT link_list FROM sites_lira WHERE id = %d;" %x);
            results = cursor.fetchall();
            result_array = results[0][0].split(',');
            for el in result_array:
                try:
                    cursor.execute("INSERT INTO sites_lira_transposed(id, inlinks, rank, curr_vect, htmlsite_id) VALUES(%d, '%s', 1, 1, %d);" %(int(el), "<"+str(x)+","+str(round(float(1.00/len(result_array)), 8))+">", int(el)));
                    conn.commit();
                except Exception, e:
                    #print "got an error adding", el, ":", e;
                    try:
                        cursor.execute("SELECT inlinks FROM sites_lira_transposed WHERE id = %d;" %int(el));
                        res = cursor.fetchall();
                        new_link = res[0][0];
                    except Exception, e:
                        #this is only reached when a 400 page is found;
                        #print 'we are now adding:', el, ;
                        cursor.execute("INSERT INTO sites_lira_transposed(id, inlinks, rank, curr_vect, htmlsite_id) VALUES(%d, '%s', 1,1, -1);" %(int(el), '<'+str(x)+','+str(round(float(1.00/len(result_array)), 8))+'>'));
                        continue;
                    #see if this link is already in the array. If so increment it's value
                    #this is because we must think if a user adds more than one link to a certain page, they desire more of their vote to go towards this site.
                    match = re.search(r'<'+str(x)+',([0-9]+\.[0-9]+)>', new_link);
                    if (match):
                        #match.group is in the form <1,0.22, 1> we must cut off the ><, then split by , and take the 2nd in the array.
                        val = float(match.group(0)[1:-1].split(',')[1]);
                        new_link = new_link.replace(match.group(0), "<"+str(x)+","+str(round(float(1.00/len(result_array) + val), 8))+">");
                    else:
                        new_link = new_link + "<"+str(x)+","+str(round(float(1.00/len(result_array)), 8))+">";
                    cursor.execute("UPDATE sites_lira_transposed set inlinks = '%s' where id = %d;" %(new_link,  int(el)));
            cursor.execute("INSERT INTO sites_lira_transposed(id, inlinks, rank, curr_vect, htmlsite_id) VALUES(%d, '', 1, 1, %d);" %(int(x), int(x)));
        except Exception, e:
            pass;
            #print 'got an error page for:', str(x);
            #print 'error 70:', e;
    conn.commit();
    cursor.execute("UPDATE sites_lira_transposed set rank = 1/%d, curr_vect=1/%d;" %(number_pages, number_pages));
            
            
    ##separate part##
    end_counter = 0;
    old_max = 0;
    finished = False;
    total_counter = 0;
    show_me = True;
    
    for x in xrange(0,  count):
        try:
            cursor.execute("SELECT inlinks FROM sites_lira_transposed WHERE id = %d;" %x);
            results = cursor.fetchall();
            if(int(x) == 2):
                show_me = True;
            else:
                show_me = False;
            result_array = results[0][0][1:-1].split("><");
            total = 0;
            try:
                for element in result_array:
                    id, value = element.split(',');
                    cursor.execute("SELECT curr_vect FROM sites_lira_transposed WHERE id = %d;" %int(id));
                    rank = cursor.fetchall();
            except Exception, e:
                pass;
                #print 'line 105:', e;
        except Exception, e:
            pass;
            #print 'line 107:', e;
    try:
        cursor.execute("UPDATE sites_lira_transposed set rank = rank, curr_vect=rank;");
        conn.commit();
    except Exception, e:
        print e;
    while not finished:
        max = 0;
        for x in xrange(0,  count):
            try:
                cursor.execute("SELECT inlinks FROM sites_lira_transposed WHERE id = %d;" %x);
                results = cursor.fetchall();
                if(int(x) == 2):
                    show_me = True;
                else:
                    show_me = False;
                result_array = results[0][0][1:-1].split("><");
                total = 0;
                try:
                    for element in result_array:
                        id, value = element.split(',');
                        cursor.execute("SELECT curr_vect FROM sites_lira_transposed WHERE id = %d;" %int(id));
                        rank = cursor.fetchall();
                        total += (.9*(float(value)*float(rank[0][0])));
                except Exception, e:
                    pass;
                    #print 'error 132:', e;
                total += (.1 * (1.00/number_pages) * (number_pages-numDangling));
                total += ((1.00/number_pages) * numDangling);
                max += total*total;
                try:
                    cursor.execute("UPDATE sites_lira_transposed SET rank = %f where id = %d;" %(total,  int(x)));
                except Exception, e:
                    pass;
                    #print 'error line 139:', e;
            except Exception, e:
                pass;
        try:
            max = 1.0/max;
            max = sqrt(max);
            cursor.execute("UPDATE sites_lira_transposed SET rank=rank*%f, curr_vect = rank;" %round(max, 8));
            conn.commit();
        except Exception, e:
            pass;
            #print "error 148:", e;
        
        if round(max - old_max, 8) <= 0.0000001 and round(max - old_max, 8) >= 0:
            end_counter += 1;
        elif round(max - old_max, 8) >= -0.0000001 and round(max - old_max, 8) <= 0:
            end_counter += 1;
        elif max == old_max:
            end_counter += 1;
        else:
            end_counter = 0;
        if(end_counter >=10):
            finished = True;
        if(total_counter >= 75):
            finished = True;
        else:
            total_counter += 1;
        old_max = max;
    cursor.execute("SELECT sum(rank) from sites_lira_transposed;");
    res = cursor.fetchall();
    cursor.execute("UPDATE sites_lira_transposed set rank = rank/%f;" %float(res[0][0]));
    conn.commit();
    conn.close();
    print "DONE";
