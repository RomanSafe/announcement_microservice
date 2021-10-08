import boto3
from datetime import datetime, timezone

TABLE_NAME = "announcements"
client = boto3.client("dynamodb")

# A single call to BatchWriteItem can write up to 16 MB of data,
# which can comprise as many as 25 put or delete requests.
for batch_number in range(1, 501):
    request_items = {TABLE_NAME: []}
    for request_number in range(1, 26):
        request_items[TABLE_NAME].append(
            {
                "PutRequest": {
                    "Item": {
                        "title": {
                            "S": f"batch and request numbers: {batch_number}, {request_number}"
                        },
                        "date-time": {
                            "S": datetime.now(timezone.utc).isoformat(
                                timespec="microseconds"
                            )
                        },
                        "description": {
                            "S": f"batch and request numbers: {batch_number}, {request_number}"
                        },
                    }
                }
            }
        )
    response = client.batch_write_item(
        RequestItems=request_items,
        ReturnConsumedCapacity="TOTAL",
    )
    print(response)
