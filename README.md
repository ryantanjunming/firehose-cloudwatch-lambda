# firehose-cloudwatch-lambda
Python code used as a transformation lambda of AWS Kinesis Firehose when ingesting AWS Cloudwatch Logs. This adds a JSON string to the start of the log message before being sent out. Might have a very large memory footprint (and cost increase) due to decompressing/recompressing as cloudwatch logs are gziped when entering firehose.
