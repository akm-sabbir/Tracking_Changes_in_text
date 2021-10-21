from unittest import TestCase
from unittest.mock import patch, Mock

from boto3.exceptions import ResourceNotExistsError

from app.dto.core.pipeline.sentence import Sentence
from app.service.impl.dynamo_db_service import DynamoDbService


class TestDynamoDBService(TestCase):
    @patch("app.service.impl.dynamo_db_service.boto3")
    def test__get_item__given_correct_input__should_return_correct_output(self, mock_boto3: Mock):
        dynamo_db_service = DynamoDbService("TestTable")
        dynamo_db_service.table = Mock()

        mock_query = Mock()
        mock_query.return_value = {"Items": [{"data": 123}, {"data2": 123}]}

        dynamo_db_service.table.query = mock_query

        result = dynamo_db_service.get_item("123")
        assert result[0] == {"data": 123}
        assert result[1] == {"data2": 123}

        query_args = mock_query.call_args[1]["KeyConditionExpression"]._values
        assert query_args[0].name == "id"
        assert query_args[1] == "123"

    @patch("app.service.impl.dynamo_db_service.boto3")
    def test__get_item__given_incorrect_table_name__should_raise_error(self, mock_boto3: Mock):
        dynamo_db_service = DynamoDbService("TestTable")
        dynamo_db_service.table = Mock()

        dynamo_db_service.table.query = Mock()
        dynamo_db_service.table.query.side_effect = ResourceNotExistsError("DynamoDB", "", False)

        mock_error = Mock()
        dynamo_db_service._DynamoDbService__logger = Mock()
        dynamo_db_service._DynamoDbService__logger.error = mock_error

        dynamo_db_service.get_item("123")
        mock_error.assert_called_once_with("Error getting data from DynamoDB. Item Id: 123", exc_info=True)

    @patch("app.service.impl.dynamo_db_service.boto3")
    def test__save_item__given_correct_input__should_return_correct_output(self, mock_boto3: Mock):
        dynamo_db_service = DynamoDbService("TestTable")
        dynamo_db_service.table = Mock()

        mock_put_item = Mock()
        mock_put_item.return_value = "data inserted"
        dynamo_db_service.table.put_item = mock_put_item

        result = dynamo_db_service.save_item(Sentence("abc", 1, 4))
        assert mock_put_item.call_args[1] == {"Item": {'text': 'abc', 'start': 1, 'end': 4}}
        assert result == "data inserted"

    @patch("app.service.impl.dynamo_db_service.boto3")
    def test__save_item__given_incorrect_table_name__should_raise_error(self, mock_boto3: Mock):
        dynamo_db_service = DynamoDbService("TestTable")
        dynamo_db_service.table = Mock()

        dynamo_db_service.table.put_item = Mock()
        dynamo_db_service.table.put_item.side_effect = ResourceNotExistsError("DynamoDB", "", False)

        mock_error = Mock()
        dynamo_db_service._DynamoDbService__logger = Mock()
        dynamo_db_service._DynamoDbService__logger.error = mock_error

        dynamo_db_service.save_item(Sentence("abc", 1, 4))
        mock_error.assert_called_once_with('Error saving data to DynamoDB. Data:{"text": "abc", "start": 1, "end": 4}', exc_info=True)
