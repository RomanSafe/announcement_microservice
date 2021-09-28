#!/bin/bash -xe
# automation of packaging and deployment of CloudFoundation stack

if [ -z "$1" ]
  then
    echo "Argument 'stage' is required"
    exit 1
fi

STAGE=$1
APP_NAME="announcement-app"
REGION="eu-north-1"

#aws s3 mb "s3://${APP_NAME}"

aws cloudformation package \
--template-file ./template.yaml \
--output-template-file "./packaged-template-${STAGE}.yaml" \
--s3-bucket ${APP_NAME} \
--s3-prefix "artifacts/${STAGE}" \
--region ${REGION}

aws cloudformation deploy \
--template-file "./packaged-template-${STAGE}.yaml" \
--stack-name "${APP_NAME}-${STAGE}" \
--capabilities CAPABILITY_IAM \
--region ${REGION} \
--parameter-overrides "Stage=${STAGE}"
