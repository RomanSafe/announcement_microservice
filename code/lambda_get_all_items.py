import json
import logging
import os
from typing import Mapping, Optional, Union

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from models import Pagination, PositiveResponse
from pydantic import ValidationError

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.info("Dependencies are imported; logging is configured.")

# TableName provided by template.yaml
TABLE_NAME = os.environ["TABLE_NAME"]


def get_db_table_object():
    """Instantiate DynamoDB table resource object and return it."""
    client = boto3.resource("dynamodb")
    logging.info("Table is instantiated.")
    return client.Table(TABLE_NAME)


def get_all_items(
    table_object,
    endpoint_url: str,
    query_parameters: Optional[Mapping[str, Union[str, int]]] = None,
):
    """Get all items from DynamoDB.

    :param table_object: DynamoDB table resource object;
    :return: generator iterator to yield all items from DB.

    :param table_object:
    :param endpoint_url:
    :param query_parameters:
    :return:
    """
    scan_kwargs = {"TableName": TABLE_NAME}
    page_number = 1
    next_page_url = None
    if query_parameters:
        logging.info(f"query_parameters: {query_parameters}")
        try:
            pagination = Pagination.parse_obj(query_parameters).dict()
        except ValidationError as error:
            return "422", error.json()
        page_number = pagination["next_page_number"]
        scan_kwargs["ExclusiveStartKey"] = {
            "title": pagination["title"],
            "date-time": pagination["date_time"],
        }
        logging.info(f"scan_kwargs['ExclusiveStartKey']: {scan_kwargs['ExclusiveStartKey']}")
    try:
        logging.info("Getting all items from DB.")
        response = table_object.scan(**scan_kwargs)
    except ClientError as error:
        return error.response["ResponseMetadata"]["HTTPStatusCode"], json.dumps(
            error.response["Error"]
        )
    except BotoCoreError as error:
        return "400", json.dumps(error)
    else:
        announcements: list = response.get("Items", [])
        logging.info(f"{len(announcements)} items are received from DB.")
        last_evaluated_key = response.get("LastEvaluatedKey")
        logging.info(f"LastEvaluatedKey is {last_evaluated_key}.")
        if last_evaluated_key:
            next_page_url = (
                f"{endpoint_url}?title={last_evaluated_key['title']}"
                f"&date-time={last_evaluated_key['date-time']}"
                f"&next-page-number={page_number + 1}"
            )
            logging.info(f"next_page_url: {next_page_url}")
        positive_response = PositiveResponse(
            page=page_number, announcements=announcements, next_page=next_page_url
        ).json()
        return "200", positive_response


def respond(status_code: str, body: str) -> dict:
    """Return a response with JSON-formatted body.

    :param status_code: HTTP status code of the response;
    :param body: a dict with number of page, items from DynamoDB, and
    optionally - path to the next page;
    :return: response with JSON-formatted body.
    """
    logging.info("Sending the respond.")
    return {
        "statusCode": status_code,
        "body": body,
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
    endpoint_url = (
        f"https://{event['requestContext']['domainName']}"
        f"{event['requestContext']['path']}"
    )
    query_parameters = event.get("queryStringParameters")
    logging.info(f"query_parameters: {query_parameters}")
    return respond(
        *get_all_items(get_db_table_object(), endpoint_url, query_parameters)
    )
