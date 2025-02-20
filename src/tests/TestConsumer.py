import unittest
from unittest.mock import patch, MagicMock
import json
from src.config import settings
from src.messaging.consumer import callback, send_feedback, detect_typos,remove

class TestResumeConsumer(unittest.TestCase):

    def test_detect_typos(self):
        """Test the detect_typos function for accurate typo detection"""
        text = "This is a smple txt with errrs."
        actual_typos = detect_typos(text)

        # Assert the number of typos detected
        self.assertEqual(len(actual_typos), 3)



    @patch("src.messaging.consumer.pika.BlockingConnection")
    def test_send_feedback(self, mock_pika):
        """Test that send_feedback publishes messages correctly"""
        mock_channel = MagicMock()
        mock_pika.return_value.channel.return_value = mock_channel

        feedback = {
            "resumeId": "123",
            "parsed_text": "Sample text",
            "typos": ["smple"],
            "status": "typos_found"
        }

        send_feedback(mock_channel, feedback)

        mock_channel.basic_publish.assert_called_once_with(
            exchange="",
            routing_key=settings.settings.feedback_queue,
            body=json.dumps(feedback).encode("utf-8")
        )

    @patch("src.messaging.consumer.text_extract")
    @patch("src.messaging.consumer.send_feedback")
    @patch("src.messaging.consumer.remove")
    @patch("tempfile.NamedTemporaryFile")
    def test_callback(self, mock_temp_file, mock_remove, mock_send_feedback, mock_extract_text):
        """Test the RabbitMQ callback function end-to-end"""
        
        # Mocking RabbitMQ channel, method, and properties
        mock_channel = MagicMock()
        mock_method = MagicMock()
        mock_properties = MagicMock()
        mock_properties.correlation_id = "12345"

        # Simulate binary content of a PDF
        fake_pdf_content = b"%PDF-1.4 Fake PDF content"

        # Mock temporary file behavior
        temp_mock = MagicMock()
        temp_mock.name = "temp_resume.pdf"
        mock_temp_file.return_value.__enter__.return_value = temp_mock

        # Call the callback function
        callback(mock_channel, mock_method, mock_properties, fake_pdf_content)
        print(settings.settings.feedback_queue)
        # Assertions
        mock_send_feedback.assert_called_once()
        mock_remove.assert_called_once_with("temp_resume.pdf")
        mock_channel.basic_ack.assert_called_once_with(delivery_tag=mock_method.delivery_tag)

if __name__ == "__main__":
    unittest.main()
