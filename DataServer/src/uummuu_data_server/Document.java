/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package uummuu_data_server;

/**
 *
 * @author David
 */
public class Document 
{
    private int occur;
    private int docid;
    private double rank;
    public Document(int d, double r)
    {
        docid = d;
        occur = 1;
        rank = r;
    }
    public int get_occurrence()
    {
        return occur;
    }
    public int get_docid()
    {
        return docid;
    }
    public double get_rank()
    {
        return rank;
    }
    public void inc_occur( double r)
    {
        occur++;
        rank += r;
    }
}
