# AWS Lambda + SQS Mini Lab : 

## Overview
This is a mini hands-on lab for practicing AWS Cloud concepts for the AWS Certified Cloud Practitioner (CCP) exam.  
The lab demonstrates how to create a Lambda function that reads messages from an Amazon SQS queue, processes them, 
count words in message body and log the message as either "Cloud message" or "Default message" based on the 
presence of keyword "AWS" in the message

## Prerequisites
- AWS Free Tier Account
- Basic knowledge of EC2, SQS, Lambda
- Python 3.13 runtime (for Lambda)
- IAM role with Lambda permissions to access SQS

## Architecture [SQS Queue] --> [Lambda Function] --> [CloudWatch Logs]
1. SQS Queue – holds messages to be processed
2. Lambda Function – reads/polls messages from SQS and processes them
3. CloudWatch Logs – captures Lambda execution logs

## Steps / Procedure

### 1. Create an SQS Queue
- Go to SQS in AWS Console
- Click **Create queue**
- Name: `MyTestQueue`
- Type: Standard
- Leave other settings default
- Click **Create**
  
### 2. Send a Test Message
- Select the queue
- Click **Send message**
- Enter message body: `"This is a test message and it has AWS keyword"`
- Click **Send message**

### 3. Create a Lambda Function
- Go to Lambda in AWS Console
- Click **Create function**
- Choose **Author from scratch**
- Name: `MyTestLambdaSQSProcessor`
- Runtime: Python 3.13
- Role: **Create new role from AWS policy templates**
- Select policy template: **Amazon SQS Poller**
- Click **Create function**

### 4. Add Lambda Code to process messages from SQS and print the word count in each message and log the message as `Cloud` or `Default`.Click Deploy for the changes to take effect.

### 5. Connect Lambda to SQS
- Go to Function Overview → **Add trigger**
- Select SQS
- Choose your queue: `MyTestQueue`
- Click Add

 ### 6. Test the Flow
- Send another message to the queue
- Check **CloudWatch** Logs for Lambda execution output
- Verify message processed successfully
- Logs word count, Cloud/ Default category

### 7. Cleanup / Deletion
- Delete Lambda function
- Delete SQS queue
- Delete IAM role created for this lab (if created manually)
- Delete any security groups created by launch wizards (optional)

