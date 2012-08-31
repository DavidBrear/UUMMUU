package uummuu_data_server;
import java.io.*;
/**
 *
 * @author David
 * @version 1.0
 * @date 11/24/08
 */
public class Main 
{

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) 
    {
        //start the server
        Server svr = new Server();
        svr.run();
    }

}
