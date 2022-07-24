import logging
import os

import boto3

from app.exception.exception_messages import S3_DOWNLOAD_ERROR


class S3DownloaderService:
    __logger = logging.getLogger(__name__)

    def __init__(self):
        self.s3 = boto3.resource('s3')

    def download_from_s3(self, bucket: str, key, local_file_name) -> None:
        try:
            if not os.path.exists(local_file_name):
                self.s3.meta.client.download_file(bucket, key, local_file_name)
            else:
                self.__logger.error(f'{bucket}/{key} is already downloaded by someone else')
        except Exception as e:
            error_message = "Error occurred during downloading file: " + key + " from bucket " + bucket + \
                            " to -> " + local_file_name + " Reason: " + str(e)
            self.__logger.error(error_message)

            raise RuntimeError(S3_DOWNLOAD_ERROR)
