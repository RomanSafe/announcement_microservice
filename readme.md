# Announcement application
Description: A serverless application with a RESTful API endpoints using Amazon API Gateway,
which read/write to DynamoDB.

## How to package:
```shell
aws cloudformation package \
--template-file ./template.yaml \
--s3-bucket announcement-app \
--output-template-file packaged-template.yaml
```

## How to deploy:
```shell
aws cloudformation deploy \
--template-file /home/roman/Projects/serverless_python_app/packaged-template.yaml \
--stack-name announcement-app \
--capabilities CAPABILITY_IAM
```

## How to delete CloudFormation stack:
```shell
aws cloudformation delete-stack --stack-name announcement-app
```
