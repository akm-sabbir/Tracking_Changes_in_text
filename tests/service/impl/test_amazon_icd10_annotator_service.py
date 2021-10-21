from unittest import TestCase
from unittest.mock import patch, Mock

from app.exception.service_exception import ServiceException
from app.service.impl.amazon_icd10_annotator_service import AmazonICD10AnnotatorServiceImpl


class TestAmazonICD10AnnotatorService(TestCase):

    @patch('boto3.client')
    def test__get_icd_10_codes__should_return_correct_value__given_correct_text(self, mock_boto3_client: Mock):
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client
        mock_client.infer_icd10_cm = Mock()
        mock_client.infer_icd10_cm.return_value = self.__get_dummy_icd10_response()

        responses = AmazonICD10AnnotatorServiceImpl().get_icd_10_codes("text")
        mock_boto3_client.assert_called_once_with(service_name="comprehendmedical")
        mock_client.infer_icd10_cm.assert_called_once_with(Text="text")

        assert responses[0].medical_condition == "abcd"
        assert responses[0].begin_offset == 1
        assert responses[0].end_offset == 3
        assert responses[0].is_negated
        assert responses[0].score == 0.8

        assert responses[0].suggested_codes[0].code == "A00.1"
        assert responses[0].suggested_codes[0].description == "Disease 1"
        assert responses[0].suggested_codes[0].score == 0.8

        assert responses[0].suggested_codes[1].code == "A00.3"
        assert responses[0].suggested_codes[1].description == "Disease 7"
        assert responses[0].suggested_codes[1].score == 0.5

        assert responses[1].medical_condition == "efgh"
        assert responses[1].begin_offset == 5
        assert responses[1].end_offset == 9
        assert not responses[1].is_negated
        assert responses[1].score == 0.9

        assert responses[1].suggested_codes[0].code == "B00.12"
        assert responses[1].suggested_codes[0].description == "Disease 0"
        assert responses[1].suggested_codes[0].score == 0.45

        assert responses[1].suggested_codes[1].code == "B00.2"
        assert responses[1].suggested_codes[1].description == "Disease 6"
        assert responses[1].suggested_codes[1].score == 0.78

    @patch('boto3.client')
    def test__get_icd_10_codes__should_raise_service_exception__given_internal_exception_raise(self,
                                                                                               mock_boto3_client: Mock):
        mock_client = Mock()
        mock_boto3_client.return_value = mock_client
        mock_client.infer_icd10_cm = Mock()
        mock_client.infer_icd10_cm.side_effect = Mock(side_effect=Exception('Could not get data'))

        with self.assertRaises(ServiceException) as error:
            AmazonICD10AnnotatorServiceImpl().get_icd_10_codes("text")
        assert error.exception.message == "Error getting ICD10 annotation from ACM"

    def __get_dummy_icd10_response(self):
        return {"Entities": [
            {
                "Text": "abcd",
                "BeginOffset": 1,
                "EndOffset": 3,
                "Score": 0.8,
                "ICD10CMConcepts": [
                    {
                        "Code": "A00.1",
                        "Description": "Disease 1",
                        "Score": 0.8
                    },
                    {
                        "Code": "A00.3",
                        "Description": "Disease 7",
                        "Score": 0.5
                    }
                ],
                "Traits": [
                    {
                        "Name": "NEGATION"
                    }
                ]
            },
            {
                "Text": "efgh",
                "BeginOffset": 5,
                "EndOffset": 9,
                "Score": 0.9,
                "ICD10CMConcepts": [
                    {
                        "Code": "B00.12",
                        "Description": "Disease 0",
                        "Score": 0.45
                    },
                    {
                        "Code": "B00.2",
                        "Description": "Disease 6",
                        "Score": 0.78
                    }
                ],
                "Traits": [
                    {
                        "Name": "SOME TRAIT"
                    }
                ]
            }
        ]

        }
