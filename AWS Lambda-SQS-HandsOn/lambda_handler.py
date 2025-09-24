import json

def lambda_handler(event, context):
    # 1. Log the entire event for debugging
    print("Received event:", json.dumps(event))

    # 2. Loop through each record (SQS delivers messages in Records array)
    for record in event['Records']:
        message_body = record['body']   # extract the message
        print("Message Body:", message_body)

        # Count words
        word_count_in_message = len(message_body.split())
        print("Word count:", word_count_in_message)

        # Categorize message
        message_category = 'Default'
        if 'AWS'.lower() in message_body.lower():
            message_category = 'Cloud'
        print("Category:", message_category)

    # 3. Return response
    return {
        'statusCode': 200,
        'body': json.dumps("Message processed successfully")
    }
