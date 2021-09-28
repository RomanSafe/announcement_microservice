# Announcement application
Description: A serverless application with a RESTful API endpoints using Amazon API Gateway,
which read/write to DynamoDB.

## To package and deploy in single command
run shell script package_deploy_stack.sh with name of environment:
```shell
./package_deploy_stack.sh dev
```

## To delete CloudFormation stack and S3 bucket
run shell script ./stack_clean_up.sh with names of stack and bucket:
```shell
./stack_clean_up.sh stack_name bucket_name
```
