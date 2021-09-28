#!/bin/bash -xe

APP_NAME="announcement-app"

aws cloudformation delete-stack --stack-name ${APP_NAME}
aws cloudformation wait stack-delete-complete \
--stack-name ${APP_NAME}
aws s3 rb --force "s3://${APP_NAME}"
