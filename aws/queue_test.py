# import boto3
# import json

# # Create an SQS client
# sqs = boto3.client('sqs')

# # Specify the queue name
# queue_name = 'llm-queue'

# try:
#     # Get the queue URL
#     response = sqs.get_queue_url(QueueName=queue_name)
#     queue_url = response['QueueUrl']

#     # Create a JSON message
#     message_dict = {
#         "type": "solutions",
#         "use_case_id":"00010fdf-26d0-4953-bcba-3044faf2b770",
#         "use_case_name" : "AI-facilitated Focus Groups",
#         "use_case_description" : "Employ AI-powered tools to facilitate and analyze focus groups, providing insights into employee perceptions and sentiments.",
#         "industry_name" : "consulting_strategy",
#         "industry_category_name" : "Crisis Management & Turnaround",
#         "timestamp": "2023-05-24T10:30:00Z"
#     }

#     # Convert the dictionary to a JSON string
#     message_body = json.dumps(message_dict)

#     # Send the JSON message to the queue
#     response = sqs.send_message(
#         QueueUrl=queue_url,
#         MessageBody=message_body
#     )

#     print(f"JSON message sent. MessageId: {response['MessageId']}")

# except Exception as e:
#     print(f"An error occurred: {str(e)}")
# 2024/07/10/[$LATEST]16d23f1af7a947c4a82e951b64a9f4ff




import boto3
import json
from queue_test_solutions import find_usecases

# Create an SQS client
sqs = boto3.client('sqs')

# Specify the queue name
queue_name = 'llm-queue-2'

try:
    # Get the queue URL
    response = sqs.get_queue_url(QueueName=queue_name)
    queue_url = response['QueueUrl']

    entries = []
    usecases=find_usecases()
    print(usecases)

    for i in range(100):
        # Create a JSON message
        usecase = usecases[i]

        # Create a JSON message
        message_dict = {
            "type": f"solutions-{i}",
            "use_case_id": usecase["case_id"],
            "use_case_name": usecase["name"],
            "use_case_description": usecase["description"],
            "industry_name": usecase["industry_name"],
            "industry_category_name": usecase["industry_category_name"],
            "timestamp": "2023-05-24T10:30:00Z"
        }


        # Convert the dictionary to a JSON string
        message_body = json.dumps(message_dict)

        entries.append({
            'Id': str(i),
            'MessageBody': message_body
        })

        # Send the JSON message to the queue
        if i > 0 and i % 9 == 0:
            response = sqs.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries
            )
            entries = []
            # response = sqs.send_message(
            #     QueueUrl=queue_url,
            #     MessageBody=message_body
            # )

            print(response)
            for success in response['Successful']:
                print(f"JSON message sent. MessageId: {success['MessageId']}")

            if 'Failed' in response:
                for failure in response['Failed']:
                    print(f"Failed to send message. Code: {failure['Code']}, Message: {failure['Message']}")

    if (len(entries) > 0):
        response = sqs.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries
        )
        entries = []
        # response = sqs.send_message(
        #     QueueUrl=queue_url,
        #     MessageBody=message_body
        # )

        for success in response['Successful']:
            print(f"JSON message sent. MessageId: {success['MessageId']}")

        if 'Failed' in response:
            for failure in response['Failed']:
                print(f"Failed to send message. Code: {failure['Code']}, Message: {failure['Message']}")

except Exception as e:
    print(e)
    print(f"An error occurred: {str(e)}")