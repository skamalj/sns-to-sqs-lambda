import json
import boto3
from email import policy
from email.parser import BytesParser
import os
import email.utils

# Initialize SQS client
sqs = boto3.client("sqs")

# Environment variable for the SQS Queue URL
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL")

def lambda_handler(event, context):
    # Parse SNS message
    sns_message = event["Records"][0]["Sns"]["Message"]
    ses_notification = json.loads(sns_message)

    # Get raw MIME content (encoded as UTF-8)
    raw_email = ses_notification["content"].encode('utf-8')

    # Parse MIME content
    mime_message = BytesParser(policy=policy.default).parsebytes(raw_email)

    # Extract headers
    sender = mime_message["From"]
    subject = mime_message["Subject"]

    # Extract plain text body (ignore HTML)
    text_body = None
    if mime_message.is_multipart():
        for part in mime_message.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                text_body = part.get_payload(decode=True).decode(charset)
                break
    else:
        if mime_message.get_content_type() == "text/plain":
            charset = mime_message.get_content_charset() or "utf-8"
            text_body = mime_message.get_payload(decode=True).decode(charset)

    if not text_body:
        text_body = "No plain text content found."

    parsed_name, emailid = email.utils.parseaddr(sender)

    # Prepare message for SQS
    sqs_message = {
        "name": parsed_name,
        "channel_type": "email",
        "from": emailid,
        "messages": f"Subject: {subject}\n\nMessage Body: {text_body}"
    }

    # Send message to SQS
    response = sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(sqs_message)
    )

    print(f"SQS Response: {response} for message {sqs_message}")

    return 
