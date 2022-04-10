import simplejson as json
import logging
from decimal import Decimal
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key

from app.service.db_service import DBService


class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

class DynamoDbService(DBService):
    dynamodb = None

    def __init__(self, table_name: str):
        self.__logger = logging.getLogger(__name__)
        if self.dynamodb is None:
            self.dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
        self.table = self.dynamodb.Table(table_name)

    def get_item(self, item_id: Any):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('id').eq(item_id)
            )
            return response['Items']
        except Exception:
            self.__logger.error("Error getting data from DynamoDB. Item Id: " + item_id, exc_info=True)
            return []

    def save_item(self, model: Any):
        model_dict = json.loads(
            json.dumps(model, default=lambda o: getattr(o, '__dict__', str(o))), parse_float=Decimal)
        try:
            response = self.table.put_item(
                Item=model_dict
            )
            return response
        except Exception:
            self.__logger.error("Error saving data to DynamoDB. Data:" + json.dumps(model_dict), exc_info=True)
