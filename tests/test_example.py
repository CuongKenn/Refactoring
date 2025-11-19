"""
Test suite for Hotel Management System
Comprehensive tests for all modules and features
"""

from datetime import datetime, timedelta

import pytest

from app.example import (
    Guest,
    Hotel,
    PaymentMethod,
    Reservation,
    Room,
    RoomStatus,
    RoomType,
    ServiceType,
    Staff,
    StaffRole,
    calculate_days_between,
    format_currency,
    generate_invoice,
    validate_email,
    validate_phone,
)


class TestRoom:
    def test_room_creation(self):
        room = Room("101", RoomType.DELUXE, 250.0, 1, ["TV", "WiFi", "Mini Bar"])
        assert room.room_number == "101"
        assert room.room_type == RoomType.DELUXE
        assert room.price_per_night == 250.0
        assert room.status == RoomStatus.AVAILABLE

    def test_room_status_change(self):
        room = Room("102", RoomType.SINGLE, 100.0, 1, ["WiFi"])
        result = room.change_status(RoomStatus.OCCUPIED)
        assert result
        assert room.status == RoomStatus.OCCUPIED

    def test_room_maintenance_restriction(self):
        room = Room("103", RoomType.DOUBLE, 150.0, 2, ["TV"])
        room.status = RoomStatus.MAINTENANCE
        result = room.change_status(RoomStatus.OCCUPIED)
        assert result == False

    def test_room_add_maintenance_record(self):
        room = Room("104", RoomType.SUITE, 300.0, 3, ["TV", "WiFi", "Jacuzzi"])
        room.add_maintenance_record("AC broken", "John Doe", 150.0)
        assert len(room.maintenance_history) == 1
        assert room.status == RoomStatus.MAINTENANCE

    def test_room_price_calculation_peak_season(self):
        room = Room("105", RoomType.PRESIDENTIAL, 500.0, 5, ["All"])
        price = room.calculate_price_with_season(True, 3)
        assert price == 500.0 * 3 * 1.5

    def test_room_price_calculation_regular_season(self):
        room = Room("106", RoomType.SINGLE, 100.0, 1, ["Basic"])
        price = room.calculate_price_with_season(False, 2)
        assert price == 200.0


class TestGuest:
    def test_guest_creation(self):
        guest = Guest("G001", "Alice Johnson", "alice@example.com", "+1234567890", "ID123", "USA")
        assert guest.guest_id == "G001"
        assert guest.name == "Alice Johnson"
        assert guest.loyalty_points == 0
        assert guest.vip_status == False

    def test_add_loyalty_points(self):
        guest = Guest("G002", "Bob Smith", "bob@example.com", "+9876543210", "ID456", "UK")
        guest.add_loyalty_points(500)
        assert guest.loyalty_points == 500
        assert guest.vip_status == False

    def test_vip_status_promotion(self):
        guest = Guest("G003", "Charlie Brown", "charlie@example.com", "+1122334455", "ID789", "Canada")
        guest.add_loyalty_points(1000)
        assert guest.vip_status

    def test_use_loyalty_points_success(self):
        guest = Guest("G004", "Diana Prince", "diana@example.com", "+5544332211", "ID999", "USA")
        guest.add_loyalty_points(500)
        result = guest.use_loyalty_points(200)
        assert result
        assert guest.loyalty_points == 300

    def test_use_loyalty_points_insufficient(self):
        guest = Guest("G005", "Eve Adams", "eve@example.com", "+6677889900", "ID111", "Australia")
        guest.add_loyalty_points(100)
        result = guest.use_loyalty_points(200)
        assert result == False
        assert guest.loyalty_points == 100

    def test_guest_discount_rates(self):
        guest = Guest("G006", "Frank Castle", "frank@example.com", "+7788990011", "ID222", "USA")
        assert guest.get_discount_rate() == 0.0
        guest.add_loyalty_points(150)
        assert guest.get_discount_rate() == 0.05
        guest.add_loyalty_points(400)
        assert guest.get_discount_rate() == 0.10
        guest.add_loyalty_points(500)
        assert guest.get_discount_rate() == 0.15


class TestReservation:
    def test_reservation_creation(self):
        guest = Guest("G007", "Grace Hopper", "grace@example.com", "+1231231234", "ID333", "USA")
        room = Room("201", RoomType.DELUXE, 250.0, 2, ["TV", "WiFi"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=3)
        reservation = Reservation(guest, room, check_in, check_out, 2)
        assert reservation.guest == guest
        assert reservation.room == room
        assert reservation.num_guests == 2
        assert reservation.status == "pending"

    def test_calculate_total_basic(self):
        guest = Guest("G008", "Henry Ford", "henry@example.com", "+2342342345", "ID444", "USA")
        room = Room("202", RoomType.SINGLE, 100.0, 2, ["WiFi"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=2)
        reservation = Reservation(guest, room, check_in, check_out, 1)
        total = reservation.calculate_total()
        expected = (100.0 * 2) * 1.10
        assert total == expected

    def test_calculate_total_with_discount(self):
        guest = Guest("G009", "Ivy League", "ivy@example.com", "+3453453456", "ID555", "USA")
        guest.add_loyalty_points(1000)
        room = Room("203", RoomType.DOUBLE, 150.0, 2, ["TV", "WiFi"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=2)
        reservation = Reservation(guest, room, check_in, check_out, 2)
        total = reservation.calculate_total()
        room_charge = 150.0 * 2 * 0.85
        expected = room_charge * 1.10
        assert total == expected

    def test_add_service_to_reservation(self):
        guest = Guest("G010", "Jack Ryan", "jack@example.com", "+4564564567", "ID666", "USA")
        room = Room("204", RoomType.SUITE, 300.0, 2, ["All"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=1)
        reservation = Reservation(guest, room, check_in, check_out, 2)
        reservation.add_service(ServiceType.ROOM_SERVICE, "Breakfast", 50.0)
        assert len(reservation.services) == 1

    def test_make_payment(self):
        guest = Guest("G011", "Karen Page", "karen@example.com", "+5675675678", "ID777", "USA")
        room = Room("205", RoomType.SINGLE, 100.0, 2, ["Basic"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=1)
        reservation = Reservation(guest, room, check_in, check_out, 1)
        total = reservation.calculate_total()
        payment = reservation.make_payment(total, PaymentMethod.CASH)
        assert reservation.paid_amount >= total
        assert reservation.status == "paid"

    def test_confirm_reservation(self):
        guest = Guest("G012", "Leo Messi", "leo@example.com", "+6786786789", "ID888", "Argentina")
        room = Room("206", RoomType.DELUXE, 250.0, 2, ["TV", "WiFi"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=2)
        reservation = Reservation(guest, room, check_in, check_out, 1)
        result = reservation.confirm_reservation()
        assert result
        assert reservation.status == "confirmed"
        assert room.status == RoomStatus.RESERVED

    def test_check_in_guest(self):
        guest = Guest("G013", "Maria Garcia", "maria@example.com", "+7897897890", "ID999", "Spain")
        room = Room("207", RoomType.DOUBLE, 150.0, 2, ["WiFi"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=1)
        reservation = Reservation(guest, room, check_in, check_out, 2)
        reservation.confirm_reservation()
        result = reservation.check_in_guest()
        assert result
        assert reservation.status == "checked_in"
        assert room.status == RoomStatus.OCCUPIED

    def test_check_out_guest(self):
        guest = Guest("G014", "Nathan Drake", "nathan@example.com", "+8908908901", "ID1010", "USA")
        room = Room("208", RoomType.SUITE, 300.0, 3, ["All"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=1)
        reservation = Reservation(guest, room, check_in, check_out, 1)
        reservation.confirm_reservation()
        reservation.check_in_guest()
        reservation.calculate_total()
        result = reservation.check_out_guest()
        assert result
        assert reservation.status == "completed"
        assert room.status == RoomStatus.CLEANING


class TestStaff:
    def test_staff_creation(self):
        staff = Staff("S001", "Oliver Queen", StaffRole.MANAGER, 5000.0, "morning")
        assert staff.staff_id == "S001"
        assert staff.name == "Oliver Queen"
        assert staff.role == StaffRole.MANAGER
        assert staff.performance_score == 5.0

    def test_staff_clock_in_out(self):
        staff = Staff("S002", "Peter Parker", StaffRole.RECEPTIONIST, 3000.0, "evening")
        assert staff.on_duty == False
        staff.clock_in()
        assert staff.on_duty
        staff.clock_out()
        assert staff.on_duty == False

    def test_complete_task(self):
        staff = Staff("S003", "Quinn Fabray", StaffRole.HOUSEKEEPING, 2500.0, "morning")
        staff.complete_task("Clean room 301", 30)
        assert len(staff.tasks_completed) == 1

    def test_update_performance(self):
        staff = Staff("S004", "Rachel Green", StaffRole.CONCIERGE, 3500.0, "afternoon")
        initial_score = staff.performance_score
        staff.update_performance(8.0)
        assert staff.performance_score != (initial_score)

    def test_monthly_salary_with_bonus_high_performance(self):
        staff = Staff("S005", "Sam Wilson", StaffRole.MAINTENANCE, 3000.0, "morning")
        staff.performance_score = 9.5
        salary = staff.get_monthly_salary_with_bonus()
        assert salary == 3000.0 * 1.3

    def test_monthly_salary_with_bonus_medium_performance(self):
        staff = Staff("S006", "Tony Stark", StaffRole.MANAGER, 5000.0, "morning")
        staff.performance_score = 7.8
        salary = staff.get_monthly_salary_with_bonus()
        assert salary == 5000.0 * 1.15

    def test_monthly_salary_with_bonus_low_performance(self):
        staff = Staff("S007", "Uma Thurman", StaffRole.RECEPTIONIST, 3000.0, "evening")
        staff.performance_score = 4.0
        salary = staff.get_monthly_salary_with_bonus()
        assert salary == 3000.0


class TestHotel:
    def test_hotel_creation(self):
        hotel = Hotel("Grand Plaza", "123 Main St", 10)
        assert hotel.name == "Grand Plaza"
        assert hotel.address == "123 Main St"
        assert hotel.total_floors == 10

    def test_add_room(self):
        hotel = Hotel("Luxury Inn", "456 Park Ave", 5)
        room = Room("301", RoomType.DELUXE, 200.0, 3, ["TV", "WiFi"])
        result = hotel.add_room(room)
        assert result
        assert "301" in hotel.rooms

    def test_register_guest(self):
        hotel = Hotel("Comfort Suites", "789 Beach Rd", 8)
        guest = Guest("G015", "Victor Hugo", "victor@example.com", "+9019019012", "ID1111", "France")
        result = hotel.register_guest(guest)
        assert result
        assert "G015" in hotel.guests

    def test_hire_staff(self):
        hotel = Hotel("Business Hotel", "321 Corp Blvd", 12)
        staff = Staff("S008", "Wendy Williams", StaffRole.HOUSEKEEPING, 2800.0, "morning")
        result = hotel.hire_staff(staff)
        assert result
        assert "S008" in hotel.staff

    def test_create_reservation_success(self):
        hotel = Hotel("Resort Paradise", "999 Ocean Dr", 6)
        guest = Guest("G016", "Xavier Woods", "xavier@example.com", "+1011011013", "ID1212", "USA")
        room = Room("401", RoomType.SUITE, 350.0, 4, ["All"])
        hotel.register_guest(guest)
        hotel.add_room(room)
        check_in = datetime.now()
        check_out = check_in + timedelta(days=2)
        reservation = hotel.create_reservation("G016", "401", check_in, check_out, 2)
        assert reservation is not None
        assert reservation.guest == guest

    def test_create_reservation_room_unavailable(self):
        hotel = Hotel("City Center", "555 Urban St", 15)
        guest = Guest("G017", "Yvonne Strahovski", "yvonne@example.com", "+2022022024", "ID1313", "Australia")
        room = Room("501", RoomType.DOUBLE, 180.0, 5, ["WiFi"])
        room.status = RoomStatus.OCCUPIED
        hotel.register_guest(guest)
        hotel.add_room(room)
        check_in = datetime.now()
        check_out = check_in + timedelta(days=1)
        reservation = hotel.create_reservation("G017", "501", check_in, check_out, 2)
        assert reservation is None

    def test_process_check_in(self):
        hotel = Hotel("Mountain Lodge", "777 Summit Peak", 4)
        guest = Guest("G018", "Zoe Saldana", "zoe@example.com", "+3033033035", "ID1414", "USA")
        room = Room("601", RoomType.DELUXE, 220.0, 6, ["TV", "WiFi"])
        hotel.register_guest(guest)
        hotel.add_room(room)
        check_in = datetime.now()
        check_out = check_in + timedelta(days=1)
        reservation = hotel.create_reservation("G018", "601", check_in, check_out, 1)
        reservation.confirm_reservation()
        result = hotel.process_check_in(reservation.reservation_id)
        assert result

    def test_process_check_out(self):
        hotel = Hotel("Seaside Resort", "888 Coastal Hwy", 7)
        guest = Guest("G019", "Adam Driver", "adam@example.com", "+4044044046", "ID1515", "USA")
        room = Room("701", RoomType.PRESIDENTIAL, 600.0, 7, ["Premium"])
        hotel.register_guest(guest)
        hotel.add_room(room)
        check_in = datetime.now()
        check_out = check_in + timedelta(days=1)
        reservation = hotel.create_reservation("G019", "701", check_in, check_out, 1)
        reservation.confirm_reservation()
        hotel.process_check_in(reservation.reservation_id)
        reservation.calculate_total()
        result = hotel.process_check_out(reservation.reservation_id)
        assert result["success"]

    def test_search_available_rooms(self):
        hotel = Hotel("Downtown Plaza", "111 City Center", 9)
        room1 = Room("801", RoomType.SINGLE, 120.0, 8, ["Basic"])
        room2 = Room("802", RoomType.DOUBLE, 180.0, 8, ["WiFi"])
        room3 = Room("803", RoomType.SUITE, 350.0, 8, ["All"])
        hotel.add_room(room1)
        hotel.add_room(room2)
        hotel.add_room(room3)
        available = hotel.search_available_rooms(min_price=100, max_price=200)
        assert len(available) == 2

    def test_get_occupancy_rate(self):
        hotel = Hotel("Airport Inn", "222 Terminal Rd", 5)
        room1 = Room("901", RoomType.SINGLE, 130.0, 9, ["WiFi"])
        room2 = Room("902", RoomType.DOUBLE, 170.0, 9, ["TV"])
        room1.status = RoomStatus.OCCUPIED
        hotel.add_room(room1)
        hotel.add_room(room2)
        rate = hotel.get_occupancy_rate()
        assert rate == 50.0

    def test_schedule_maintenance(self):
        hotel = Hotel("Historic Hotel", "333 Heritage Lane", 6)
        room = Room("1001", RoomType.DELUXE, 240.0, 10, ["Classic"])
        staff = Staff("S009", "Bruce Wayne", StaffRole.MAINTENANCE, 3200.0, "morning")
        hotel.add_room(room)
        hotel.hire_staff(staff)
        result = hotel.schedule_maintenance("1001", "Plumbing issue", "S009", 200.0)
        assert result

    def test_assign_cleaning_task(self):
        hotel = Hotel("Garden Suites", "444 Flora Ave", 4)
        room = Room("1101", RoomType.SINGLE, 110.0, 11, ["Basic"])
        staff = Staff("S010", "Clark Kent", StaffRole.HOUSEKEEPING, 2700.0, "afternoon")
        room.status = RoomStatus.CLEANING
        hotel.add_room(room)
        hotel.hire_staff(staff)
        result = hotel.assign_cleaning_task("1101", "S010")
        assert result
        assert room.status == RoomStatus.AVAILABLE


class TestUtilityFunctions:
    def test_validate_email_valid(self):
        assert validate_email("test@example.com")
        assert validate_email("user.name@domain.co.uk")

    def test_validate_email_invalid(self):
        assert validate_email("invalid-email") == False
        assert validate_email("missing@domain") == False

    def test_validate_phone_valid(self):
        assert validate_phone("+1234567890")
        assert validate_phone("(123) 456-7890")

    def test_validate_phone_invalid(self):
        assert validate_phone("123") == False
        assert validate_phone("abc-def-ghij") == False

    def test_calculate_days_between(self):
        date1 = datetime(2025, 1, 1)
        date2 = datetime(2025, 1, 5)
        days = calculate_days_between(date1, date2)
        assert days == 4

    def test_format_currency(self):
        result = format_currency(1234.56, "USD")
        assert result == "USD 1,234.56"

    def test_generate_invoice(self):
        guest = Guest("G020", "Diana Ross", "diana@example.com", "+5055055057", "ID1616", "USA")
        room = Room("1201", RoomType.SUITE, 400.0, 12, ["Premium"])
        check_in = datetime.now()
        check_out = check_in + timedelta(days=2)
        reservation = Reservation(guest, room, check_in, check_out, 2)
        reservation.calculate_total()
        invoice = generate_invoice(reservation)
        assert "invoice_id" in invoice
        assert invoice["guest_name"] == "Diana Ross"
