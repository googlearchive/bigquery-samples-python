package com.google.cloud.bigquery.samples.test;

import com.google.cloud.bigquery.samples.AsyncQuerySample;

import org.junit.*;

import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.CoreMatchers.not;
import static org.junit.Assert.assertThat;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;

public class AsyncQuerySampleTest extends BigquerySampleTest{

  @Test
  public void testInteractive() throws IOException, InterruptedException{
    ByteArrayOutputStream boas = new ByteArrayOutputStream();
    PrintStream out = new PrintStream(boas);
    AsyncQuerySample.run(PROJECT_ID, QUERY, false, 5000, 5, out);
    out.flush();
    assertThat(boas.size(), is(not(0)));
  }
  
  
  @Test
  @Ignore // Batches can take up to 3 hours to run, probably shouldn't use this
  public void testBatch() throws IOException, InterruptedException{
    ByteArrayOutputStream boas = new ByteArrayOutputStream();
    PrintStream out = new PrintStream(boas);
    AsyncQuerySample.run(PROJECT_ID, QUERY, true, 5000, 5, out);
    out.flush();
    assertThat(boas.size(), is(not(0)));
  }
  
  
}
