import json
import os
from datetime import datetime, timezone
from typing import Union, List, Dict, Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from pydantic import ValidationError

from models import NewAnnouncement

# TableName provided by template.yaml
TABLE_NAME = os.environ["TABLE_NAME"]


def get_db_table_object():
    """Instantiate DynamoDB table resource object and return it."""
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(TABLE_NAME)


def add_item(table_object, new_announcement: dict) -> tuple:
    """Add a new announcement to DynamoDB.

    :param table_object: DynamoDB table resource object;
    :param new_announcement: attributes of new announcement (title and
    description) to add to DB;
    :return: info about added entity.
    """
    new_item = {
        "title": new_announcement.get("title"),
        "description": new_announcement.get("description"),
        "date-time": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
    }
    print(new_item)
    print(type(new_item))
    try:
        response = table_object.put_item(Item=new_item)
        print("dynamo response", response)
    except ClientError as error:
        return (
            error.response["ResponseMetadata"]["HTTPStatusCode"],
            error.response["Error"]["Code"],
            error.response["Error"]["Message"],
        )
    except BotoCoreError as error:
        return "400", "Client side error", error
    else:
        return "201", "Added a new announcement", new_item


def respond(status_code: str, message: str, details: Union[dict, str, List[Dict[str, Any]]
]) -> dict:
    """Return a response with JSON-formatted body.

    :param status_code: HTTP status code of the response;
    :param message: message for status code;
    :param details: info about added to DB item or error;
    :return: response with JSON-formatted body.
    """
    body = {"message": message, "details": details}
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
    }


def add_announcement(event, context) -> dict:
    """Add to the DynamoDB the payload from a request body.

    :param event: dict representing a request;
    :param context: context of the request
    :return: Return a response with JSON-formatted body.
    """
    payload = event.get("body")
    print(payload)
    print(type(payload))
    if isinstance(payload, str):
        payload = json.loads(payload)
        print(type(payload))
    try:
        new_announcement = NewAnnouncement.parse_obj(payload)
    except ValidationError as e:
        print(e.args)
        print()
        return respond("415", "Unsupported Media Type", e.errors())
    return respond(*add_item(get_db_table_object(), new_announcement.dict()))
