from io import BytesIO
import base64
import gzip
import io
import json

output = []
# Metadata to be added to the log events, can be added as environment variables
company_metadata = {"company_id": "1234567", "code": "12222", "city": "NYC"}

def gzip_b64encode(data):
    compressed = BytesIO()
    with gzip.GzipFile(fileobj=compressed, mode='w') as f:
        json_response = json.dumps(data)
        f.write(json_response.encode('utf-8'))
    return base64.b64encode(compressed.getvalue()).decode('ascii')

def lambda_handler(event, context):
    for record in event['records']:
        compressed_payload = base64.b64decode(record['data'])
        uncompressed_payload = gzip.decompress(compressed_payload) #decompress payload
        payload = json.loads(uncompressed_payload)
        
        processed_events = []
        #loop through log events and add metadata to log string
        for log_event in payload['logEvents']:
            message = json.dumps(company_metadata) + ' ' + log_event['message'] + ' ' 
            log_event['message'] = message
            
            processed_events.append(log_event)
            
        payload['logEvents'] = processed_events
        
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': gzip_b64encode(payload)
        }
        
        output.append(output_record)
        
    print('Successfully processed {}        records.'.format(len(event['records'])))
    return {'records': output}