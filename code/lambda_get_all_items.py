import json
import logging
import os
from typing import Union

import boto3

dynamo_client = boto3.client("dynamodb")
table_name = os.environ["TABLE_NAME"]


def get_all_items(db_client: boto3.client) -> list:
    """Get all items from DynamoDB.

    :param db_client: boto3.client
    :return: all items from DB.
    """
    response = db_client.scan(TableName=table_name)
    logging.info("Getting all items from DB.")
    return response.get("Items")


def respond(status_code: str, body: Union[list, str]) -> dict:
    """Return a response with JSON-formatted body.

    :param status_code: HTTP status code of the response;
    :param body: content of the response's body;
    :return: response with JSON-formatted body.
    """
    logging.info("Sending the respond.")
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET",
        },
    }


def list_announcements(event, context) -> dict:
    """Return all announcements from DynamoDB.

    :param event: dict representing a request;
    :param context: context of the request
    :return: Return a response with JSON-formatted body.
    """
    http_method = event["httpMethod"]
    if http_method == "GET":
        logging.info("httpMethod match.")
        all_items = get_all_items(dynamo_client)
        if all_items:
            logging.info("Items are received from DB.")
            return respond("200", all_items)
        else:
            return respond("204", "No Content")
    else:
        # API Gateway responds: 403 - {"message":"Missing Authentication Token"}
        # I'l leave it here for future research
        return respond("405", "Method Not Allowed")
