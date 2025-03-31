# SNS to SQS Message Processor

This AWS Lambda function processes email messages from an SNS topic (originating from SES) and forwards them to an SQS queue in a standardized format.

## Overview

The solution consists of a serverless application that:
1. Receives email notifications from Amazon SES via SNS
2. Parses the email content (MIME format)
3. Extracts relevant information (sender, subject, body)
4. Forwards standardized messages to an SQS queue

## Architecture


SES -> SNS -> Lambda -> SQS


## Components

### Lambda Function
- Runtime: Python 3.12
- Architecture: ARM64
- Trigger: SNS Topic subscription
- Output: SQS Queue

### Message Format

The Lambda function standardizes messages into the following format before sending to SQS:


{
    "name": "Sender Name",
    "channel_type": "email",
    "from": "sender@email.com",
    "messages": "Subject: Email Subject\n\nMessage Body: Email Content"
}


## Configuration

### Environment Variables
- `SQS_QUEUE_URL`: The URL of the target SQS queue

### AWS Secrets Manager
The following secrets are required:
- `ses-to-sns-agent-topic`: ARN of the SNS topic
- `unified-queue`: Name of the target SQS queue

### IAM Permissions
The function requires:
- Permission to send messages to SQS
- Permission to read secrets from AWS Secrets Manager

## Deployment

The application is deployed using AWS SAM (Serverless Application Model). The `template.yaml` file defines the infrastructure as code.

### Prerequisites
1. AWS SAM CLI installed
2. AWS credentials configured
3. Required secrets set up in AWS Secrets Manager

### Deployment Steps
1. Clone the repository
2. Navigate to the project directory
3. Run SAM build and deploy commands:
bash
sam build
sam deploy


## Error Handling

- If no plain text content is found in the email, the message will contain "No plain text content found."
- The function handles both multipart and single-part email messages
- Character encoding is handled with fallback to UTF-8

## Monitoring

The function logs its operations to CloudWatch Logs, including:
- SQS response details
- Processed message content

You can monitor the function's execution through the AWS Lambda console and CloudWatch Logs.

## Output

The SAM template provides the following output:
- `ProcessorFunctionArn`: The ARN of the deployed Lambda function