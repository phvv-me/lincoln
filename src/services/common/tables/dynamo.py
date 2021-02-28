from functools import wraps

import boto3

class DynamoResponse:
    """
    scan: {'Items': [], 'Count': 0, 'ScannedCount': 0, 'ResponseMetadata': {'RequestId': '8Q4252D4FI3NOATO13N52AO61BVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 28 Feb 2021 13:32:36 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '39', 'connection': 'keep-alive', 'x-amzn-requestid': '8Q4252D4FI3NOATO13N52AO61BVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '3413411624'}, 'RetryAttempts': 0}}
    put_item: {'ResponseMetadata': {'RequestId': 'O2QUSA21SHH33VADRNAL6436NJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 28 Feb 2021 13:37:25 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'connection': 'keep-alive', 'x-amzn-requestid': 'O2QUSA21SHH33VADRNAL6436NJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
    delete: {'ResponseMetadata': {'RequestId': '5L47BAL1GEJLL2BQFM7RS95DTBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 28 Feb 2021 13:38:21 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '2', 'connection': 'keep-alive', 'x-amzn-requestid': '5L47BAL1GEJLL2BQFM7RS95DTBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2745614147'}, 'RetryAttempts': 0}}
    """

    def __init__(self, raw_response):
        self.raw_response = raw_response

    @property
    def is_successful(self) -> bool:
        try:
            return self.raw_response['ResponseMetadata']['HTTPStatusCode'] == 200
        except KeyError:
            return False

    @property
    def data(self):
        if self.is_successful and 'Items' in self.raw_response:
            return self.raw_response['Items']
        return []


def handle_errors(func):
    @wraps
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:  # boto3 has a strange exception handling
            # TODO: log error and access it from discord
            return DynamoResponse({})
    return wrapper


class DynamoRepository:

    scan_limit = 100

    def __init__(self, name: str):
        dynamodb = boto3.resource('dynamodb')

        self.name = name
        self.table = dynamodb.Table(self.name)

    @handle_errors
    def put(self, **kwargs):
        raw_response = self.table.put_item(Item=kwargs)
        return DynamoResponse(raw_response)

    @handle_errors
    def delete(self, **kwargs):
        raw_response = self.table.delete_item(Key=kwargs)
        return DynamoResponse(raw_response)

    @handle_errors
    def scan(self):
        raw_response = self.table.scan(Limit=self.scan_limit)
        return DynamoResponse(raw_response)


Table = DynamoRepository
