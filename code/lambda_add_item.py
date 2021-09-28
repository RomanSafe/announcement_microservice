import json
import logging
import os
from datetime import datetime, timezone
from typing import Optional

import boto3

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.info("Dependencies are imported; logging is configured.")

# TableName provided by template.yaml
TABLE_NAME = os.environ["TABLE_NAME"]


def get_db_table_object():
    """Instantiate DynamoDB table resource object and return it."""
    dynamodb = boto3.resource("dynamodb")
    logging.info("Table is instantiated.")
    return dynamodb.Table(TABLE_NAME)


def validate_payload(payload: dict) -> bool:
    """Validate payload (body of the request).

    :param payload: body of the request;
    :return: True if payload pass validation, otherwise False.
    """
    valid = False
    if (
        payload
        and "Title" in payload
        and "Description" in payload
        and len(payload["Title"]) > 3
        and len(payload["Description"]) > 3
    ):
        valid = True
    return valid


def add_item(table_object, payload: dict):
    """Add a new item to DynamoDB from payload.

    The value of "Date-time" is a timestamp - string representing the current UTC date and time
    in ISO 8601 format: YYYY-MM-DDTHH:MM:SS.ffffff+HH:MM

    :param table_object: DynamoDB table resource object;
    :param payload: body of the request;
    """
    logging.info("Adding an item to DynamoDB.")
    new_item = {
        "Title": payload["Title"],
        "Date-time": datetime.now(timezone.utc).isoformat(timespec="microseconds"),
        "Description": payload["Description"],
    }
    table_object.put_item(Item=new_item)
    return new_item


def respond(status_code: str, message: str, added_item: Optional[dict] = None) -> dict:
    """Return a response with JSON-formatted body.

    :param status_code: HTTP status code of the response;
    :param message: message for status code;
    :param added_item: content of added to DB item;
    :return: response with JSON-formatted body.
    """
    logging.info("Sending the respond.")
    body = {"Message": message, "Added_item": added_item}
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
    http_method = event["httpMethod"]
    if http_method == "POST":
        logging.info("httpMethod match.")
        payload = event["body"]
        if isinstance(payload, str):
            payload = json.loads(payload)
        if validate_payload(payload):
            logging.info("Payload is found.")
            return respond(
                "201",
                "Added a new announcement",
                add_item(get_db_table_object(), payload),
            )
        else:
            return respond("415", "Unsupported Media Type")
    else:
        # API Gateway responds: 403 - {"message":"Missing Authentication Token"}
        # I'l leave it here for future research
        return respond("405", "Method Not Allowed")
