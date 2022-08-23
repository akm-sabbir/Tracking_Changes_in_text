from unittest import TestCase
from unittest.mock import Mock, patch

from app.service.downloader.s3_downloader import S3DownloaderService


class TestS3DownloaderService(TestCase):
    def setUp(self) -> None:
        self.s3_downloader_service = S3DownloaderService()
        self.mock_boto = Mock()
        self.s3_downloader_service.s3 = self.mock_boto

    def test__download_from_s3__when_can_not_download_file__raise_S3DownloadException(self):
        self.s3_downloader_service.s3.meta.client.download_file.side_effect = Exception

        with self.assertRaises(RuntimeError) as context:
            self.s3_downloader_service.download_from_s3('model_bucket', 'model_key', 'local_file')

        self.assertEqual('Could not download the file from s3.', str(context.exception))

    @patch("app.service.downloader.s3_downloader.os")
    def test__download_from_s3__when_file_is_already_downloaded(self, mocked_os):
        mocked_os.path.os.exists.return_value = True

        self.s3_downloader_service.download_from_s3('model_bucket', 'model_key', 'local_file')

        mocked_os.path.exists.assert_called_once()

    @patch("app.service.downloader.s3_downloader.os")
    def test__download_from_s3__when_file_is_not_downloaded(self, mocked_os):
        mocked_os.path.exists.return_value = False
        self.s3_downloader_service.s3.meta.client.download_file.return_value = None

        self.s3_downloader_service.download_from_s3('model_bucket', 'model_key', 'local_file')

        mocked_os.path.exists.assert_called_once()
