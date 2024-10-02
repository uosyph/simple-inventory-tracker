from app import app, Ingredient
from app.utils.send_email import send_low_stock_email
from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture
def ingredient():
    return Ingredient(name="Beef", stock=9.0, initial_stock=20.0)


@patch("smtplib.SMTP")
def test_send_low_stock_email(mock_smtp, ingredient):
    # Mock the SMTP connection and its methods
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value = mock_smtp_instance
    mock_smtp_instance.sendmail.return_value = {}

    result = send_low_stock_email(ingredient)

    assert result is True


@patch("app.utils.send_email.SMTP")
def test_send_low_stock_email_success(mock_smtp, ingredient):
    # Create a mock SMTP instance and return the mock instance
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

    mock_smtp_instance.ehlo.return_value = None
    mock_smtp_instance.starttls.return_value = None
    mock_smtp_instance.login.return_value = None
    mock_smtp_instance.sendmail.return_value = {}

    result = send_low_stock_email(ingredient)

    assert result is True
    mock_smtp_instance.ehlo.assert_called()
    mock_smtp_instance.starttls.assert_called()
    mock_smtp_instance.login.assert_called_with(
        app.config["EMAIL"], app.config["PASSWORD"]
    )
    mock_smtp_instance.sendmail.assert_called_once()


@patch("app.utils.send_email.SMTP")
def test_send_low_stock_email_failure(mock_smtp, ingredient):
    # Create a mock SMTP instance and raise an exception on sendmail
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    mock_smtp_instance.sendmail.side_effect = Exception("SMTP Error")

    result, error_message = send_low_stock_email(ingredient)

    assert result is False
    assert "SMTP Error" in error_message
