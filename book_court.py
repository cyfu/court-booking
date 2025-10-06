#!/usr/bin/env python3
"""
Court Booking System
Handles booking tennis courts at Angus Glen Tennis Centre
"""

import json
import sys
from datetime import datetime, timedelta
import pytz
from PerfectMindSession import PerfectMindSession


class CourtBooker:
    """Handles court booking functionality"""

    def __init__(self):
        self.session_manager = PerfectMindSession()

    def find_available_slot(self, preferred_time=None, preferred_duration=60):
        """Find the first available slot across all courts"""
        print("🔍 Searching for available slots...")

        # Load court configuration
        with open('court-info.json', 'r') as f:
            courts_config = json.load(f)

        all_available_slots = []

        # Check all courts
        results = self.session_manager.check_all_courts(courts_config)

        for court_num, data in results.items():
            if data['availability']:
                slots = self.session_manager.parse_availability_data(data['availability'])

                for slot in slots:
                    slot['court'] = court_num
                    all_available_slots.append(slot)

        if not all_available_slots:
            print("❌ No available slots found across all courts")
            return None

        # Sort by date and time
        all_available_slots.sort(key=lambda x: (x.get('date', ''), x.get('time', '')))

        print(f"✅ Found {len(all_available_slots)} available slots:")
        for i, slot in enumerate(all_available_slots[:5]):  # Show first 5
            print(f"  {i+1}. Court {slot['court']} - {slot.get('date')} at {slot.get('time')}")

        if len(all_available_slots) > 5:
            print(f"  ... and {len(all_available_slots) - 5} more")

        return all_available_slots[0]  # Return the first available slot

    def book_court(self, slot):
        """Book a specific time slot"""
        if not slot:
            print("❌ No slot provided for booking")
            return False

        print(f"\n🎾 Attempting to book:")
        print(f"  Court: {slot.get('court')}")
        print(f"  Date: {slot.get('date')}")
        print(f"  Time: {slot.get('time')}")
        print(f"  Duration: {slot.get('duration')} minutes")

        # This is where you would implement the actual booking logic
        # For now, we'll simulate the booking process

        print("\n⚠️  BOOKING SIMULATION:")
        print("  This is a simulation - no actual booking will be made")
        print("  To implement real booking, you would need to:")
        print("  1. Get user authentication (login)")
        print("  2. Send booking request to the booking API")
        print("  3. Handle payment processing")
        print("  4. Confirm booking details")

        # Simulate booking success
        print(f"\n✅ SIMULATED BOOKING SUCCESSFUL!")
        print(f"  Booking ID: BK{datetime.now().strftime('%Y%m%d%H%M%S')}")
        print(f"  Court: {slot.get('court')}")
        print(f"  Time: {slot.get('date')} {slot.get('time')}")

        return True

    def auto_book_next_available(self):
        """Automatically book the next available slot"""
        print("🤖 Auto-booking next available slot...")

        slot = self.find_available_slot()

        if slot:
            return self.book_court(slot)
        else:
            print("❌ No slots available for auto-booking")
            return False


def main():
    """Main booking interface"""
    print("🎾 Angus Glen Tennis Centre - Court Booking System")
    print("=" * 60)

    booker = CourtBooker()

    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "check":
            print("📊 Checking availability only...")
            slot = booker.find_available_slot()
            if slot:
                print(f"\n✅ Next available slot: Court {slot['court']} on {slot.get('date')} at {slot.get('time')}")
            else:
                print("\n❌ No available slots found")

        elif command == "book":
            print("🎾 Auto-booking next available slot...")
            success = booker.auto_book_next_available()
            if success:
                print("\n🎉 Booking completed successfully!")
            else:
                print("\n💥 Booking failed!")

        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: check, book")
    else:
        # Interactive mode
        print("\nChoose an option:")
        print("1. Check availability")
        print("2. Auto-book next available slot")
        print("3. Exit")

        try:
            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                slot = booker.find_available_slot()
                if slot:
                    print(f"\n✅ Next available slot: Court {slot['court']} on {slot.get('date')} at {slot.get('time')}")
                else:
                    print("\n❌ No available slots found")

            elif choice == "2":
                success = booker.auto_book_next_available()
                if success:
                    print("\n🎉 Booking completed successfully!")
                else:
                    print("\n💥 Booking failed!")

            elif choice == "3":
                print("👋 Goodbye!")

            else:
                print("❌ Invalid choice")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            print(f"\n💥 Error: {e}")


if __name__ == "__main__":
    main()
