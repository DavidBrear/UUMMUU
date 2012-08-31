/*
 * @author: David Brear
 * @date: 11/10/08
 * @version: 03/15/09
 */

package uummuu_data_server;
import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;
import java.sql.*;
import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.regex.*;
import java.util.HashMap;
/**
 *
 * @author David
 */
public class Server extends Thread 
{
    private ServerSocket svr;
    MysqlDataSource my = new MysqlDataSource();
    Connection c = null;
    ResultSet rs;
    HashMap ranks = new HashMap();
    int query_counter;
    public Server()
    {
        query_counter = 0;
        try
        {
        my.setUrl("jdbc:mysql://"+UserInfo.host+":3306/"+UserInfo.db);
        my.setUser(UserInfo.user);
        my.setPassword(UserInfo.pword);
        c = my.getConnection();
        rs = c.createStatement().executeQuery(
                "SELECT id, rank FROM sites_lira_transposed;");
        while(rs.next())
        {
            ranks.put(Integer.parseInt(rs.getString(1)), rs.getString(2));
        }
        }
        catch(Exception exp)
        {
            System.out.println("Connecting to db: " + exp.getMessage());
        }
    }
    @Override
    public void run()
    {
        try
        {
            System.out.println("Binding to port");
            //connect to the port 8888
            svr = new ServerSocket(8888);
            System.out.println("Created Server Socket on port: " 
                    + svr.getLocalPort());
        }
        catch(IOException exp)
        {
            System.out.println("IOException caught: " + exp.getMessage());
        }
        while(true)
        {
            try
            {
                Socket conn = svr.accept();
                BufferedReader in = new BufferedReader(
                      new InputStreamReader(conn.getInputStream()));
                DataOutputStream out = new DataOutputStream(
                        conn.getOutputStream());
                printDatabase(in, out);
                conn.close();
            }
            catch(IOException exp)
            {
                System.out.println("error: " + exp.getMessage());
            }
        }
    }
    private void printDatabase(BufferedReader in, DataOutputStream out)
    {
        String input = "";
        String output = "";
        String [] word_array;
        try
        {
            input = in.readLine();
            input = input.replaceAll("_", " ");
            input = input.replaceAll("-", "");
            //create an array of strings
            word_array = input.split(" ");
            String solution = "";
            if(input.equals("Hey how many queries have you served?"))
            {
                solution = "<br>I have served: " + query_counter + " queries";
            }
            else
            {
                solution += findWord(word_array);
                query_counter++;
            }
            out.writeBytes(solution + "\n\r");
        }
        catch(Exception exp)
        {
            System.out.println("The Error was: " + exp.getMessage());
        }
    }
    
    private String findWord(String [] words)
    {
        String ret_val = "";//the final return string
        String database_sol = "";//the database solution
        
        String query = "";
        String response = "";
        boolean added_first = false;
        
        /**
         * These following are for each response.
         */
        
        String response_url = "";
        String response_name = "";
        String response_info = "";
        
        //ArrayLists
        ArrayList total_doc_ids = new ArrayList();
        ArrayList top_ten = new ArrayList();
        int top_ten_counter = 0;
        try
        {
            for(int i = 0; i < words.length; i++)
            {
                query = "SELECT invert_list from sites_index where word = '"
                        + words[i] + "';";
                //use a try catch block to make sure that there is a result
                //for this term.
                try
                {
                    //execute the SQL query for this inverted list
                    rs = c.createStatement().executeQuery(query);
                
                    //while there is another entry. 
                    //(There should only be one each time.)
                    response = "";
                    while(rs.next())
                    {
                        response = rs.getString(1); //get this inverted_list
                    }
                    rs.close();
                    response = response.substring(1, response.length()-1);
                    for(String element : response.split("><"))
                    {
                        String [] parts = element.split(",");
                        int doc_id = Integer.parseInt(parts[0]);
                        double rank = 0;
                        //How much are we giving pages as a boost for having
                        //this word in their title?
                        double in_title_addition = 1.5;
                        // 50% is a good addition to rank.
                        double weight = Double.parseDouble(parts[1]);
                        boolean in_title = parts[3].equals("1") ? true : false;

                        rank = Double.parseDouble(ranks.get(doc_id).toString());
                        rank = rank + weight;
                        if(in_title)
                        {
                            rank *= in_title_addition;
                        }
                        add_docID(doc_id, rank, total_doc_ids);

                    }
                }
                catch(Exception exp)
                {
                    System.out.println("caught the exception: " + exp.getMessage());
                }
            }
            for(int j = 0; j < total_doc_ids.size(); j++)
            {
                int doc_id = ((Document)total_doc_ids.get(j)).get_docid();
                double rank = ((Document)total_doc_ids.get(j)).get_rank();
                
                add_via_rank(doc_id, rank, top_ten);
                if(top_ten.size() > 10)
                {
                    top_ten.trimToSize();
                    top_ten.remove(10);
                }
            }
            for(Object obj : top_ten.toArray())
            {
                int doc_id = ((Document)(obj)).get_docid();
                query = "SELECT url, name, information FROM sites_htmlsite "+
                        "inner join sites_sitequeue on "+
                        "sites_htmlsite.id = sites_sitequeue.id WHERE" + 
                        " sites_sitequeue.id = " + doc_id + ";";
                rs = c.createStatement().executeQuery(query);
                while(rs.next())
                {
                    response_url = rs.getString(1);
                    response_name = rs.getString(2);
                    response_info = highlight_terms(
                            rs.getString(3).substring(
                            response_name.length()), words);
                    if(response_name.length() == 0)
                    {
                        response_name = response_url;
                    }
                }
                //append this result to the top 10 from this server.
                ret_val += "<rank>"+((Document)(obj)).get_rank()+"</rank>";
                ret_val += "<div class='entry'>";
                ret_val += "<div class='name'><a href='"+ 
                        response_url+ "'>"+response_name+"</a></div>";
                ret_val += "<div class='result_desc'>"+
                        response_info+"</div>";
                ret_val += "<div class='result_url'>"+response_url+"</div>";
                ret_val += "</div>";
            }
        }
        catch(Exception exp)
        {
            System.out.println("Got an error: " + exp.getMessage());
        }
        return ret_val;
    }
    
    /**
     * highlight_terms takes in an array of terms and a long string and
     * highlights up to the first 4 occurrences of words in the string.
     * @param str the long string to be highlighted
     * @param words the array of words to search for
     * @return a string with the terms highlighted.
     */
    private String highlight_terms(String str, String [] words)
    {
        String ret_str = "";
        String lower_version = str.toLowerCase();
        int occ_counter = 0;
        int total_words = 0;
        this_for_loop:
        while(true)
        {
            for(String word : words)
            {
                int start_pos = lower_version.indexOf(' '+
                        word.toLowerCase()+' ');
                int end_pos = start_pos + word.length();
                if(start_pos == -1)
                {
                    occ_counter++;
                    if(occ_counter >= words.length)
                    {
                        break this_for_loop;
                    }
                }
                else
                {
                    occ_counter = 0;
                    int first_space = 
                            lower_version.substring(0, 
                            start_pos-1).lastIndexOf(" ");
                    int last_space = lower_version.indexOf(" ", end_pos);
                    int word_count = 0;
                    this_after_while:
                    while( word_count <= 5)
                    {
                        int temp_last = lower_version.indexOf(" ",
                                last_space+1);
                        if(temp_last == -1)
                            break this_after_while;
                        last_space = temp_last;
                        word_count++;
                    }
                    word_count = 0;
                    this_before_while:
                    while( word_count <= 3)
                    {
                        int temp_last = 
                                lower_version.lastIndexOf(" ", first_space-1);
                        if(temp_last == -1)
                            break this_before_while;
                        first_space = temp_last;
                        word_count++;
                    }
                    lower_version = lower_version.substring(0, start_pos) +
                            " <b>"+word+"</b> " +
                            lower_version.substring(end_pos+1);
                    ret_str += str.substring(first_space, start_pos);
                    ret_str += " <b>" + str.substring(start_pos, end_pos+1) +
                            "</b> ";
                    ret_str += str.substring(end_pos+1, last_space);
                    ret_str += "...";
                    str = str.substring(0,start_pos) +
                            " <b>"+str.substring(start_pos+1,end_pos+1)+
                            "</b> " + str.substring(end_pos+1);
                    total_words++;
                }
            }
        }
        if(total_words == 0)
        {
            int len = str.length() > 400 ? 400 : str.length();
            ret_str = str.substring(0, len);
        }
        return ret_str;
    }
    
    /**
     * add_via_rank is a method to sort the documents based off their rankings.
     * This method is going to be primarily used to gather the top ten ranked
     * document for a query.
     * @param doc_id - the id of this document
     * @param rank - the rank of this document
     * @param top_ten - the currently ranked top ten documents.
     */
    private void add_via_rank(int doc_id, double rank, ArrayList top_ten)
    {
        int end = top_ten.size();
        int mid = (int)Math.floor((end*1.0)/2);
        int start = 0;
        boolean found = false;
        if(end == 0)
        {
            top_ten.add(0, new Document(doc_id, rank));
            found = true;
        }
        while(start < end-1 && !found)
        {
            if(((Document)top_ten.get(mid)).get_rank() == rank)
            {
                if(((Document)top_ten.get(mid)).get_docid() != doc_id)
                    top_ten.add(mid, new Document(doc_id, rank));
                found = true;
            }
            else if( ((Document)top_ten.get(mid)).get_rank() > rank)
            {
                start = mid;
                mid = start + (end-start)/2;
            }
            else if(((Document)top_ten.get(mid)).get_rank() < rank)
            {
                end = mid;
                mid = start + (end-start)/2;
            }
        }
        if(!found)
        {
            if(((Document)top_ten.get(mid)).get_rank() < rank)
            {
                top_ten.add(mid, new Document(doc_id, rank));
            }
            else
            {
                top_ten.add(mid+1, new Document(doc_id, rank));
            }
        }
    }
    
    
    /**
     * add_docID is a merge sort operation to sort document ids. This method
     * is made to detect repitition in the document ids.
     * @param doc_id - the document id to add
     * @param rank - the rank of this document
     * @param total_doc_ids - the list of sorted document ids
     */
    private void add_docID(int doc_id, double rank, ArrayList total_doc_ids)
    {
        int end = total_doc_ids.size();
        int mid = (int)Math.ceil((end*1.0)/2);
        int start = 0;
        boolean found = false;
        if(end == 0)
        {
            total_doc_ids.add(0, new Document(doc_id, rank));
            found = true;
        }
        if(end == 1)
        {
            if(((Document)total_doc_ids.get(start)).get_docid() == doc_id)
            {
               ((Document)total_doc_ids.get(start)).inc_occur(rank);
            }
            else
            {
                total_doc_ids.add(0, new Document(doc_id, rank));
            }
            found = true;
        }
        while(start < end-1 && !found)
        {
            if(((Document)total_doc_ids.get(mid)).get_docid() == doc_id)
            {
                ((Document)total_doc_ids.get(mid)).inc_occur(rank);
                found = true;
            }
            else if( ((Document)total_doc_ids.get(mid)).get_docid() < doc_id)
            {
                start = mid;
                mid = start + (end-start)/2;
            }
            else if(((Document)total_doc_ids.get(mid)).get_docid() > doc_id)
            {
                end = mid;
                mid = start + (end-start)/2;
            }
        }
        if(!found)
        {
            if(((Document)total_doc_ids.get(mid)).get_docid() < doc_id)
            {
                total_doc_ids.add(mid, new Document(doc_id, rank));
            }
            else
            {
                total_doc_ids.add(mid+1, new Document(doc_id, rank));
            }
        }
    }
}
