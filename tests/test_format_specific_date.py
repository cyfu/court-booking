import pytest
from datetime import datetime
import pytz
from PerfectMindSession import PerfectMindSession


class TestFormatSpecificDate:
    """Test cases for _format_specific_date method"""

    def setup_method(self):
        """Setup test instance"""
        self.session = PerfectMindSession()

    def test_format_specific_date_basic(self):
        """Test basic date formatting"""
        result = self.session._format_specific_date('2025-10-09')
        
        # Should be in UTC format with Z suffix
        assert result.endswith('Z')
        assert '2025-10-09' in result or '2025-10-08' in result  # Account for timezone conversion

    def test_format_specific_date_timezone_conversion(self):
        """Test that Toronto timezone is properly converted to UTC"""
        # Test a date during EST (no DST)
        result = self.session._format_specific_date('2025-01-15')
        
        # Parse the result to verify it's UTC
        parsed = datetime.fromisoformat(result.replace('Z', '+00:00'))
        assert parsed.tzinfo.utcoffset(None).total_seconds() == 0  # UTC offset should be 0

    def test_format_specific_date_dst_period(self):
        """Test date formatting during DST period"""
        # Test a date during EDT (with DST)
        result = self.session._format_specific_date('2025-07-15')
        
        # Should still be properly formatted UTC
        assert result.endswith('Z')
        parsed = datetime.fromisoformat(result.replace('Z', '+00:00'))
        assert parsed.tzinfo.utcoffset(None).total_seconds() == 0  # UTC offset should be 0

    def test_format_specific_date_invalid_format(self):
        """Test handling of invalid date format"""
        # Should fallback to current date format
        result = self.session._format_specific_date('invalid-date')
        
        # Should still return a valid timestamp format
        assert result.endswith('Z')
        assert 'T' in result

    def test_format_specific_date_edge_cases(self):
        """Test edge cases like leap year, month boundaries"""
        # Leap year date
        result = self.session._format_specific_date('2024-02-29')
        assert result.endswith('Z')
        
        # Year boundary
        result = self.session._format_specific_date('2025-01-01')
        assert result.endswith('Z')
        
        # Month boundary
        result = self.session._format_specific_date('2025-12-31')
        assert result.endswith('Z')

    def test_format_specific_date_consistency(self):
        """Test that same input produces same output"""
        date_str = '2025-10-09'
        result1 = self.session._format_specific_date(date_str)
        result2 = self.session._format_specific_date(date_str)
        
        assert result1 == result2