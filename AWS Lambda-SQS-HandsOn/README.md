# AWS Lambda + SQS Mini Lab

## Overview
This is a mini hands-on lab for practicing AWS Cloud concepts for the AWS Certified Cloud Practitioner (CCP) exam.  
The lab demonstrates how to create a Lambda function that reads messages from an Amazon SQS queue, processes them, 
count words in message body and log the message as either "Cloud message" or "Default message" based on the 
presence of keyword "AWS" in the message.

---

## Prerequisites
- AWS Free Tier Account
- Basic knowledge of EC2, SQS, Lambda
- Python 3.13 runtime (for Lambda)
- IAM role with Lambda permissions to access SQS

---

## Architecture
1. SQS Queue – holds messages to be processed
2. Lambda Function – reads/polls messages from SQS and processes them
3. CloudWatch Logs – captures Lambda execution logs
