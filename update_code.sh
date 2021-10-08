#!/bin/bash -xe
# to rebuild lambda code dependencies run build_layer.sh

cd ./code
zip -g ../my-deployment-package.zip ./lambda_add_item.py ./lambda_get_all_items.py ./models.py
cd ..
aws lambda update-function-code --function-name AddAnnouncement --zip-file fileb://my-deployment-package.zip
aws lambda update-function-code --function-name GetAllAnnouncements --zip-file fileb://my-deployment-package.zip
