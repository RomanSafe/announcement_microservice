#!/bin/bash -xe
# Clean up AWS resources: delete CloudFormation stack and S3 bucket

# Print helpFunction in case parameters are empty
if [ -z "$1" ] || [ -z "$2" ]
  then
    echo "Arguments 'stack name' and 'bucket name' are required"
    exit 1
fi

STACK_NAME=$1
BUCKET_NAME=$2

aws cloudformation delete-stack --stack-name "${STACK_NAME}"
aws cloudformation wait stack-delete-complete \
--stack-name "${STACK_NAME}"
#aws s3 rb --force "s3://${BUCKET_NAME}"
