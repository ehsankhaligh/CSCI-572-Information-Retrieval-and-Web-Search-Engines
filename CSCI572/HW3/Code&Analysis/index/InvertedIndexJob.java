/*
   Source code credit: https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Example:_WordCount_v1.0
                       Tutorialspoint java tutorial
                       https://docs.oracle.com/javase/8/docs/api/java/util/HashMap.html
*/
import java.io.IOException;
import java.util.StringTokenizer;

import java.util.HashMap;
import java.util.Map;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class InvertedIndexJob {

  public static class MyMapper extends Mapper<Object, Text, Text, LongWritable> {

          private Text word = new Text();

          private LongWritable DocumentID = new LongWritable();

          public void map(Object key, Text value, Context context) throws IOException, InterruptedException{

                  String item_array[] = value.toString().split("\t", 2);
                  DocumentID.set(Long.parseLong(item_array[0]));

                  String extracteditems = item_array[1].toLowerCase().replaceAll("[^a-z]+", " ");

                  StringTokenizer itr = new StringTokenizer(extracteditems);

                  while (itr.hasMoreTokens()) {
                          word.set(itr.nextToken());
                          context.write(word, DocumentID);
                  }
          }
  }

  public static class MyReducer extends Reducer<Text,LongWritable,Text,Text> {

    private Text outcome = new Text();

    public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {

      //document ID -> long, count -> int
      HashMap<Long, Integer> wordCounter = new HashMap<Long, Integer>();

      for (LongWritable item : values) {
        Long DocumentID = item.get();

        //if item not in hashmap
        if (wordCounter.containsKey(DocumentID)){
             wordCounter.put(DocumentID, wordCounter.get(DocumentID) + 1);
        }else{
             wordCounter.put(DocumentID, 1);
        }
      }

      String counting = "";

      for (Map.Entry<Long, Integer> hashitem : wordCounter.entrySet()) {
        counting += hashitem.getKey() + ":" + hashitem.getValue() + " ";
      }

      outcome.set(counting);
      context.write(key, outcome);
    }
  }

  public static void main(String[] args) throws Exception {
          if (args.length != 2) {
                  System.err.println("Usage: Word indexing <in> <out>");
                  System.exit(-1);
          }

          Job job = new Job();

          job.setJarByClass(InvertedIndexJob.class);
          job.setJobName("Word indexing");

          job.setMapperClass(MyMapper.class);
          job.setReducerClass(MyReducer.class);
          job.setMapOutputKeyClass(Text.class);
          job.setMapOutputValueClass(LongWritable.class);
          job.setOutputKeyClass(Text.class);
          job.setOutputValueClass(Text.class);

          FileInputFormat.addInputPath(job, new Path(args[0]));
          FileOutputFormat.setOutputPath(job, new Path(args[1]));

          System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
