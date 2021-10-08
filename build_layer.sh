#!/bin/bash
set -eo pipefail
rm -rf package
pip install --target ./package -r requirements.txt
cd package
zip -r ../my-deployment-package.zip .
cd ..
