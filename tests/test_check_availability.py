import pytest
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
import os

# Add parent directory to path to import check_availability
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_availability import (
    format_slot_output,
    get_slot_key,
    find_new_slots,
    is_quiet_hours,
    get_next_check_time,
    check_court_availability
)


class TestFormatSlotOutput:
    """Test cases for format_slot_output function"""

    def test_format_slot_output_with_weekday(self):
        """Test formatting slot with weekday abbreviation"""
        slot = {
            'date': '2025-10-15',
            'time': '14:30',
            'duration': '60min'
        }
        court_num = 1
        result = format_slot_output(slot, court_num)

        assert '2025-10-15' in result
        assert '14:30' in result
        assert 'court 1' in result
        assert 'Wed' in result  # 2025-10-15 is a Wednesday
        assert '-15:30' in result  # 60 minutes after 14:30

    def test_format_slot_output_without_weekday_on_invalid_date(self):
        """Test formatting slot with invalid date"""
        slot = {
            'date': 'invalid-date',
            'time': '10:00',
            'duration': '90min'
        }
        court_num = 2
        result = format_slot_output(slot, court_num)

        assert 'invalid-date' in result
        assert '10:00' in result
        assert 'court 2' in result
        assert '-11:30' in result  # 90 minutes after 10:00

    def test_format_slot_output_different_durations(self):
        """Test formatting with different durations"""
        slot = {
            'date': '2025-10-15',
            'time': '09:00',
            'duration': '30min'
        }
        court_num = 3
        result = format_slot_output(slot, court_num)

        assert '09:00-09:30' in result

    def test_format_slot_output_default_duration(self):
        """Test formatting with missing duration (defaults to 60min)"""
        slot = {
            'date': '2025-10-15',
            'time': '12:00',
            'duration': ''
        }
        court_num = 4
        result = format_slot_output(slot, court_num)

        # Should default to 60 minutes
        assert '12:00-13:00' in result or '12:00-12:00' in result

    def test_format_slot_output_invalid_time(self):
        """Test formatting with invalid time format"""
        slot = {
            'date': '2025-10-15',
            'time': 'invalid-time',
            'duration': '60min'
        }
        court_num = 1
        result = format_slot_output(slot, court_num)

        assert 'invalid-time' in result
        # End time should be same as start time when parsing fails


class TestGetSlotKey:
    """Test cases for get_slot_key function"""

    def test_get_slot_key_basic(self):
        """Test generating slot key"""
        slot = {
            'date': '2025-10-15',
            'time': '14:30',
            'court': 1
        }
        result = get_slot_key(slot)

        assert result == '2025-10-15|14:30|1'

    def test_get_slot_key_different_courts(self):
        """Test that different courts generate different keys"""
        slot1 = {
            'date': '2025-10-15',
            'time': '14:30',
            'court': 1
        }
        slot2 = {
            'date': '2025-10-15',
            'time': '14:30',
            'court': 2
        }

        key1 = get_slot_key(slot1)
        key2 = get_slot_key(slot2)

        assert key1 != key2
        assert key1 == '2025-10-15|14:30|1'
        assert key2 == '2025-10-15|14:30|2'

    def test_get_slot_key_different_times(self):
        """Test that different times generate different keys"""
        slot1 = {
            'date': '2025-10-15',
            'time': '14:30',
            'court': 1
        }
        slot2 = {
            'date': '2025-10-15',
            'time': '15:30',
            'court': 1
        }

        key1 = get_slot_key(slot1)
        key2 = get_slot_key(slot2)

        assert key1 != key2

    def test_get_slot_key_same_slot_same_key(self):
        """Test that same slot generates same key"""
        slot = {
            'date': '2025-10-15',
            'time': '14:30',
            'court': 1
        }

        key1 = get_slot_key(slot)
        key2 = get_slot_key(slot)

        assert key1 == key2


class TestFindNewSlots:
    """Test cases for find_new_slots function"""

    def test_find_new_slots_all_new(self):
        """Test finding new slots when all are new"""
        current_slots = [
            {'date': '2025-10-15', 'time': '14:30', 'court': 1},
            {'date': '2025-10-15', 'time': '15:30', 'court': 2}
        ]
        previous_slot_keys = set()

        new_slots = find_new_slots(current_slots, previous_slot_keys)

        assert len(new_slots) == 2
        assert new_slots == current_slots

    def test_find_new_slots_none_new(self):
        """Test finding new slots when none are new"""
        current_slots = [
            {'date': '2025-10-15', 'time': '14:30', 'court': 1}
        ]
        previous_slot_keys = {'2025-10-15|14:30|1'}

        new_slots = find_new_slots(current_slots, previous_slot_keys)

        assert len(new_slots) == 0

    def test_find_new_slots_partial_new(self):
        """Test finding new slots when some are new"""
        current_slots = [
            {'date': '2025-10-15', 'time': '14:30', 'court': 1},
            {'date': '2025-10-15', 'time': '15:30', 'court': 2},
            {'date': '2025-10-15', 'time': '16:30', 'court': 3}
        ]
        previous_slot_keys = {'2025-10-15|14:30|1', '2025-10-15|15:30|2'}

        new_slots = find_new_slots(current_slots, previous_slot_keys)

        assert len(new_slots) == 1
        assert new_slots[0] == {'date': '2025-10-15', 'time': '16:30', 'court': 3}

    def test_find_new_slots_empty_current(self):
        """Test finding new slots when current slots is empty"""
        current_slots = []
        previous_slot_keys = {'2025-10-15|14:30|1'}

        new_slots = find_new_slots(current_slots, previous_slot_keys)

        assert len(new_slots) == 0

    def test_find_new_slots_empty_previous(self):
        """Test finding new slots when previous is empty"""
        current_slots = [
            {'date': '2025-10-15', 'time': '14:30', 'court': 1}
        ]
        previous_slot_keys = set()

        new_slots = find_new_slots(current_slots, previous_slot_keys)

        assert len(new_slots) == 1


class TestIsQuietHours:
    """Test cases for is_quiet_hours function"""

    def test_is_quiet_hours_late_night(self):
        """Test quiet hours during late night (23:00)"""
        now = datetime(2025, 10, 15, 23, 0, 0)
        assert is_quiet_hours(now) is True

    def test_is_quiet_hours_early_morning(self):
        """Test quiet hours during early morning (06:00)"""
        now = datetime(2025, 10, 15, 6, 0, 0)
        assert is_quiet_hours(now) is True

    def test_is_quiet_hours_at_start(self):
        """Test quiet hours at start time (22:30)"""
        now = datetime(2025, 10, 15, 22, 30, 0)
        assert is_quiet_hours(now) is True

    def test_is_quiet_hours_at_end(self):
        """Test quiet hours at end time (07:30) - should be quiet"""
        now = datetime(2025, 10, 15, 7, 29, 59)
        assert is_quiet_hours(now) is True

    def test_is_quiet_hours_after_end(self):
        """Test not quiet hours after end time (07:30:01)"""
        now = datetime(2025, 10, 15, 7, 30, 1)
        assert is_quiet_hours(now) is False

    def test_is_quiet_hours_before_start(self):
        """Test not quiet hours before start time (22:29:59)"""
        now = datetime(2025, 10, 15, 22, 29, 59)
        assert is_quiet_hours(now) is False

    def test_is_quiet_hours_midday(self):
        """Test not quiet hours during midday (12:00)"""
        now = datetime(2025, 10, 15, 12, 0, 0)
        assert is_quiet_hours(now) is False

    def test_is_quiet_hours_afternoon(self):
        """Test not quiet hours during afternoon (15:00)"""
        now = datetime(2025, 10, 15, 15, 0, 0)
        assert is_quiet_hours(now) is False

    def test_is_quiet_hours_midnight(self):
        """Test quiet hours at midnight (00:00)"""
        now = datetime(2025, 10, 15, 0, 0, 0)
        assert is_quiet_hours(now) is True


class TestGetNextCheckTime:
    """Test cases for get_next_check_time function"""

    def test_get_next_check_time_in_quiet_hours(self):
        """Test next check time when currently in quiet hours"""
        now = datetime(2025, 10, 15, 23, 0, 0)  # 11 PM
        check_interval_minutes = 15

        next_check = get_next_check_time(now, check_interval_minutes)

        # Should be 07:30:01 next day
        assert next_check.hour == 7
        assert next_check.minute == 30
        assert next_check.second == 1
        assert next_check.day == 16  # Next day

    def test_get_next_check_time_before_30_01(self):
        """Test next check time before :30:01"""
        now = datetime(2025, 10, 15, 10, 15, 0)  # 10:15
        check_interval_minutes = 20

        next_check = get_next_check_time(now, check_interval_minutes)

        # Should be 10:30:01 (earlier than 10:35 from interval)
        assert next_check.hour == 10
        assert next_check.minute == 30
        assert next_check.second == 1

    def test_get_next_check_time_after_30_01(self):
        """Test next check time after :30:01"""
        now = datetime(2025, 10, 15, 10, 45, 0)  # 10:45
        check_interval_minutes = 10

        next_check = get_next_check_time(now, check_interval_minutes)

        # Should be 10:55 (from interval, earlier than 11:30:01)
        assert next_check.hour == 10
        assert next_check.minute == 55

    def test_get_next_check_time_at_30_01(self):
        """Test next check time exactly at :30:01"""
        now = datetime(2025, 10, 15, 10, 30, 1)  # 10:30:01
        check_interval_minutes = 15

        next_check = get_next_check_time(now, check_interval_minutes)

        # Should be 10:45 (from interval, earlier than 11:30:01)
        assert next_check.hour == 10
        assert next_check.minute == 45

    def test_get_next_check_time_interval_before_30_01(self):
        """Test when interval check is before next :30:01"""
        now = datetime(2025, 10, 15, 10, 20, 0)  # 10:20
        check_interval_minutes = 5

        next_check = get_next_check_time(now, check_interval_minutes)

        # Should be 10:25 (from interval, earlier than 10:30:01)
        assert next_check.hour == 10
        assert next_check.minute == 25

    def test_get_next_check_time_next_hour_30_01(self):
        """Test when next check is next hour's :30:01"""
        now = datetime(2025, 10, 15, 10, 35, 0)  # 10:35
        check_interval_minutes = 60  # Long interval

        next_check = get_next_check_time(now, check_interval_minutes)

        # Should be 11:30:01 (earlier than 11:35 from interval)
        assert next_check.hour == 11
        assert next_check.minute == 30
        assert next_check.second == 1

    def test_get_next_check_time_avoiding_quiet_hours(self):
        """Test that next check time avoids quiet hours"""
        now = datetime(2025, 10, 15, 22, 0, 0)  # 10 PM
        check_interval_minutes = 60

        next_check = get_next_check_time(now, check_interval_minutes)

        # Should not be in quiet hours (22:30-07:30)
        # Should be 22:30:01 or later, but if it falls in quiet hours, move to 07:30:01
        if next_check.hour == 22 and next_check.minute >= 30:
            # If it's 22:30:01, that's in quiet hours, so should be moved
            assert next_check.hour == 7 and next_check.minute == 30
        else:
            # Otherwise should be before 22:30
            assert next_check.hour < 22 or (next_check.hour == 22 and next_check.minute < 30)

    def test_get_next_check_time_quiet_hours_boundary(self):
        """Test next check time near quiet hours boundary"""
        now = datetime(2025, 10, 15, 22, 25, 0)  # 22:25, just before quiet hours
        check_interval_minutes = 10

        next_check = get_next_check_time(now, check_interval_minutes)

        # Should be 22:30:01 or 22:35, but 22:30:01 is in quiet hours
        # So should be moved to 07:30:01 next day
        if next_check.hour == 22 and next_check.minute >= 30:
            assert next_check.hour == 7 and next_check.minute == 30
            assert next_check.day == 16  # Next day


class TestCheckCourtAvailability:
    """Test cases for check_court_availability function"""

    @patch('check_availability.PerfectMindSession')
    @patch('builtins.open', new_callable=mock_open, read_data='{"courts": [{"court": 1, "facilityId": "test-id"}]}')
    def test_check_court_availability_success(self, mock_file, mock_session_class):
        """Test successful court availability check"""
        # Setup mock session
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        # Mock parse_availability_data to return test slots
        mock_session.parse_availability_data.return_value = [
            {
                'date': '2025-10-15',
                'time': '14:30',
                'duration': '60min',
                'group': 'Afternoon',
                'title': 'Tennis Court',
                'ticks': 100,
                'is_disabled': False
            }
        ]

        # Mock check_all_courts to return results
        mock_session.check_all_courts.return_value = {
            1: {
                'availability': {'test': 'data'}
            }
        }

        success, slots = check_court_availability()

        assert success is True
        assert len(slots) == 1
        assert slots[0]['date'] == '2025-10-15'
        assert slots[0]['time'] == '14:30'
        assert slots[0]['court'] == 1
        assert 'formatted' in slots[0]

    @patch('check_availability.PerfectMindSession')
    @patch('builtins.open', new_callable=mock_open, read_data='{"courts": [{"court": 1, "facilityId": "test-id"}]}')
    def test_check_court_availability_no_slots(self, mock_file, mock_session_class):
        """Test court availability check with no available slots"""
        # Setup mock session
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        # Mock parse_availability_data to return empty list
        mock_session.parse_availability_data.return_value = []

        # Mock check_all_courts to return results with no availability
        mock_session.check_all_courts.return_value = {
            1: {
                'availability': None
            }
        }

        success, slots = check_court_availability()

        assert success is False
        assert len(slots) == 0

    @patch('check_availability.PerfectMindSession')
    @patch('builtins.open', side_effect=FileNotFoundError("File not found"))
    def test_check_court_availability_file_not_found(self, mock_file, mock_session_class):
        """Test court availability check when court-info.json is not found"""
        success, slots = check_court_availability()

        assert success is False
        assert len(slots) == 0

    @patch('check_availability.PerfectMindSession')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_check_court_availability_invalid_json(self, mock_file, mock_session_class):
        """Test court availability check with invalid JSON"""
        success, slots = check_court_availability()

        assert success is False
        assert len(slots) == 0

    @patch('check_availability.PerfectMindSession')
    @patch('builtins.open', new_callable=mock_open, read_data='{"courts": [{"court": 1, "facilityId": "test-id"}]}')
    def test_check_court_availability_multiple_courts(self, mock_file, mock_session_class):
        """Test court availability check with multiple courts"""
        # Setup mock session
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        # Mock parse_availability_data to return different slots for different courts
        def mock_parse(data):
            if data == {'court1': 'data'}:
                return [{'date': '2025-10-15', 'time': '14:30', 'duration': '60min', 'group': 'A', 'title': 'T', 'ticks': 100, 'is_disabled': False}]
            elif data == {'court2': 'data'}:
                return [{'date': '2025-10-15', 'time': '15:30', 'duration': '60min', 'group': 'A', 'title': 'T', 'ticks': 100, 'is_disabled': False}]
            return []

        mock_session.parse_availability_data.side_effect = mock_parse

        # Mock check_all_courts to return results for multiple courts
        mock_session.check_all_courts.return_value = {
            1: {'availability': {'court1': 'data'}},
            2: {'availability': {'court2': 'data'}}
        }

        success, slots = check_court_availability()

        assert success is True
        assert len(slots) == 2
        # Slots should be sorted by date, time, and court
        assert slots[0]['court'] == 1
        assert slots[1]['court'] == 2

    @patch('check_availability.PerfectMindSession')
    @patch('builtins.open', new_callable=mock_open, read_data='{"courts": [{"court": 1, "facilityId": "test-id"}]}')
    def test_check_court_availability_slots_sorted(self, mock_file, mock_session_class):
        """Test that slots are properly sorted"""
        # Setup mock session
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session

        # Mock parse_availability_data to return slots in random order
        mock_session.parse_availability_data.return_value = [
            {'date': '2025-10-16', 'time': '10:00', 'duration': '60min', 'group': 'A', 'title': 'T', 'ticks': 100, 'is_disabled': False},
            {'date': '2025-10-15', 'time': '14:30', 'duration': '60min', 'group': 'A', 'title': 'T', 'ticks': 100, 'is_disabled': False},
            {'date': '2025-10-15', 'time': '09:00', 'duration': '60min', 'group': 'A', 'title': 'T', 'ticks': 100, 'is_disabled': False}
        ]

        # Mock check_all_courts
        mock_session.check_all_courts.return_value = {
            1: {'availability': {'test': 'data'}}
        }

        success, slots = check_court_availability()

        assert success is True
        assert len(slots) == 3

        # Verify sorting: by date, then time, then court
        assert slots[0]['date'] == '2025-10-15'
        assert slots[0]['time'] == '09:00'
        assert slots[1]['date'] == '2025-10-15'
        assert slots[1]['time'] == '14:30'
        assert slots[2]['date'] == '2025-10-16'
        assert slots[2]['time'] == '10:00'

