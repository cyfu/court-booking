import pytest
import json
from PerfectMindSession import PerfectMindSession


class TestParseAvailabilityData:
    """Test cases for parse_availability_data method"""

    def setup_method(self):
        """Setup test instance"""
        self.session = PerfectMindSession()

    def load_test_data(self):
        """Load test data from response.json"""
        with open('tests/fixtures/response.json', 'r') as f:
            # The file contains Python dict format, need to evaluate it
            content = f.read()
            # Convert Python dict string to actual dict
            return eval(content)

    def test_parse_availability_data_basic(self):
        """Test basic parsing functionality"""
        test_data = self.load_test_data()
        slots = self.session.parse_availability_data(test_data)

        assert isinstance(slots, list)
        assert len(slots) > 0

    def test_parse_availability_data_structure(self):
        """Test that parsed slots have correct structure"""
        test_data = self.load_test_data()
        slots = self.session.parse_availability_data(test_data)

        # Check first slot structure
        slot = slots[0]
        required_keys = ['date', 'time', 'duration', 'group', 'title', 'ticks', 'is_disabled']
        for key in required_keys:
            assert key in slot

    def test_parse_availability_data_dates(self):
        """Test that dates are correctly parsed"""
        test_data = self.load_test_data()
        slots = self.session.parse_availability_data(test_data)

        # Should have slots for multiple dates
        dates = set(slot['date'] for slot in slots)
        assert len(dates) == 6  # 6 days in test data
        print(dates)
        # Check date format
        for date in dates:
            assert len(date) == 10  # YYYY-MM-DD format
            assert date.count('-') == 2

        # Assert dates are from 2025-10-07 to 2025-10-12
        expected_dates = {'2025-10-06', '2025-10-07', '2025-10-08',
                          '2025-10-09', '2025-10-10', '2025-10-11'}
        assert dates == expected_dates

    def test_parse_availability_data_times(self):
        """Test that times are correctly formatted"""
        test_data = self.load_test_data()
        slots = self.session.parse_availability_data(test_data)

        # Check time format
        for slot in slots:
            time = slot['time']
            assert len(time) == 5  # HH:MM format
            assert time.count(':') == 1

            hours, minutes = time.split(':')
            assert 0 <= int(hours) <= 23
            assert 0 <= int(minutes) <= 59

    def test_parse_availability_data_groups(self):
        """Test that booking groups are correctly identified"""
        test_data = self.load_test_data()
        slots = self.session.parse_availability_data(test_data)

        # Should have different groups
        groups = set(slot['group'] for slot in slots)
        expected_groups = {'Morning', 'Afternoon', 'Late'}
        assert groups.issubset(expected_groups)

    def test_parse_availability_data_empty_input(self):
        """Test handling of empty input"""
        assert self.session.parse_availability_data(None) == []
        assert self.session.parse_availability_data({}) == []
        assert self.session.parse_availability_data({'availabilities': []}) == []

    def test_parse_availability_data_count(self):
        """Test expected number of slots"""
        test_data = self.load_test_data()
        slots = self.session.parse_availability_data(test_data)

        # Should have multiple slots across 6 days
        assert len(slots) > 10  # Reasonable minimum

        # Group by date to verify distribution
        slots_by_date = {}
        for slot in slots:
            date = slot['date']
            if date not in slots_by_date:
                slots_by_date[date] = []
            slots_by_date[date].append(slot)

        # Each date should have at least 1 slot
        for date, date_slots in slots_by_date.items():
            assert len(date_slots) >= 1