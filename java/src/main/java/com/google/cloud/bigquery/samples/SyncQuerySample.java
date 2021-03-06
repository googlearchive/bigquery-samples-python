package com.google.cloud.bigquery.samples;

import com.google.api.services.bigquery.Bigquery;
import com.google.api.services.bigquery.Bigquery.Jobs.GetQueryResults;
import com.google.api.services.bigquery.model.GetQueryResultsResponse;
import com.google.api.services.bigquery.model.QueryRequest;
import com.google.api.services.bigquery.model.QueryResponse;

import java.io.IOException;
import java.util.Iterator;
import java.util.Scanner;
/**
 * TODO: Insert description here. (generated by elibixby)
 */
public class SyncQuerySample extends BigqueryUtils{


  //[START main]
 /**
  * @param args
  * @throws IOException
  */
 public static void main(String[] args) 
     throws IOException{

  
   Scanner scanner = new Scanner(System.in);
   System.out.println("Enter your project id: ");
   String projectId = scanner.nextLine();
   System.out.println("Enter your query string: ");
   String queryString = scanner.nextLine();
   System.out.println("Enter how long to wait for the query to complete (in milliseconds):\n " +
                      "(if longer than 10 seconds, use an asynchronous query)");
   long waitTime = scanner.nextLong();
   scanner.close();
   Iterator<GetQueryResultsResponse> pages = run(projectId, queryString, waitTime);
   while(pages.hasNext()){
     printRows(pages.next().getRows(), System.out);
   }
 }
 // [END main]
  

 // [START run]
 public static Iterator<GetQueryResultsResponse> run(String projectId, 
     String queryString, 
     long waitTime) throws IOException{
   Bigquery bigquery = BigqueryServiceFactory.getService();
   //Wait until query is done with 10 second timeout, at most 5 retries on error
   QueryResponse query = bigquery.jobs().query(
       projectId,
       new QueryRequest().setTimeoutMs(waitTime).setQuery(queryString)).execute();
   
   //Make a request to get the results of the query 
   //(timeout is zero since job should be complete)
   
   GetQueryResults getRequest = bigquery.jobs().getQueryResults(
       query.getJobReference().getProjectId(),
       query.getJobReference().getJobId());
   
   
   return getPages(getRequest);
 }
 // [END run]
 

}
