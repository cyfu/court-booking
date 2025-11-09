#!/usr/bin/env python3
"""
SMS Notifier using Twilio
Sends SMS notifications for court availability results
"""

import os
import logging
from typing import List, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SMSNotifier:
    """SMS notification service using Twilio"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize SMS notifier with Twilio credentials

        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

        # Get Twilio credentials from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.messaging_service_sid = os.getenv('TWILIO_MESSAGING_SERVICE_SID')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')  # Fallback if no messaging service
        self.to_number = os.getenv('TWILIO_TO_PHONE_NUMBER')

        # Validate credentials
        # Either messaging_service_sid OR from_number is required
        has_sender = bool(self.messaging_service_sid or self.from_number)
        if not all([self.account_sid, self.auth_token, has_sender, self.to_number]):
            self.logger.warning(
                "Twilio credentials not fully configured. SMS notifications will be disabled.\n"
                "Required environment variables:\n"
                "  - TWILIO_ACCOUNT_SID\n"
                "  - TWILIO_AUTH_TOKEN\n"
                "  - TWILIO_MESSAGING_SERVICE_SID (preferred) OR TWILIO_PHONE_NUMBER\n"
                "  - TWILIO_TO_PHONE_NUMBER (recipient phone number)"
            )
            self.client = None
        else:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.logger.info("Twilio SMS notifier initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize Twilio client: {e}")
                self.client = None

    def is_configured(self) -> bool:
        """Check if SMS notifier is properly configured"""
        return self.client is not None

    def format_message(self, slots: List[dict]) -> str:
        """
        Format court availability slots into SMS message

        Args:
            slots: List of slot dictionaries with 'formatted' key

        Returns:
            Formatted SMS message string
        """
        if not slots:
            return "Tennis Court Availability：\n\nNo available slots found."

        # Format message header (matching user's example format)
        message = "Tennis Court Availability：\n\n"

        # Add all available slots
        for slot in slots:
            message += f"{slot['formatted']}\n"

        return message

    def send_sms(self, message: str) -> bool:
        """
        Send SMS message

        Args:
            message: Message text to send

        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.is_configured():
            self.logger.warning("SMS notifier not configured, skipping SMS send")
            return False

        try:
            # Prepare message parameters
            message_params = {
                'body': message,
                'to': self.to_number
            }

            # Use messaging service SID if available (preferred), otherwise use from_number
            if self.messaging_service_sid:
                message_params['messaging_service_sid'] = self.messaging_service_sid
            else:
                message_params['from_'] = self.from_number

            # Send SMS
            message_obj = self.client.messages.create(**message_params)

            self.logger.info(
                f"SMS sent successfully. SID: {message_obj.sid}, "
                f"Status: {message_obj.status}"
            )
            return True

        except TwilioException as e:
            self.logger.error(f"Twilio error sending SMS: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending SMS: {e}")
            return False

    def send_availability_notification(self, slots: List[dict]) -> bool:
        """
        Send court availability notification via SMS

        Args:
            slots: List of slot dictionaries with 'formatted' key

        Returns:
            True if notification sent successfully, False otherwise
        """
        if not self.is_configured():
            return False

        message = self.format_message(slots)
        return self.send_sms(message)

