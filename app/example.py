"""
Hotel Management System - Comprehensive Demo
Features: Room management, Reservations, Staff, Services, Payments, Analytics
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Set


class RoomType(Enum):
    SINGLE = 1
    DOUBLE = 2
    SUITE = 3
    DELUXE = 4
    PRESIDENTIAL = 5


class RoomStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    RESERVED = "reserved"
    CLEANING = "cleaning"


class PaymentMethod(Enum):
    CASH = "cash"
    CREDIT_CARD = "credit"
    DEBIT_CARD = "debit"
    ONLINE = "online"
    BANK_TRANSFER = "bank"


class StaffRole(Enum):
    MANAGER = "manager"
    RECEPTIONIST = "receptionist"
    HOUSEKEEPING = "housekeeping"
    MAINTENANCE = "maintenance"
    CONCIERGE = "concierge"


class ServiceType(Enum):
    ROOM_SERVICE = "room_service"
    LAUNDRY = "laundry"
    SPA = "spa"
    RESTAURANT = "restaurant"
    TRANSPORTATION = "transportation"


# Room Management
class Room:
    def __init__(self, room_number: str, room_type: RoomType, price_per_night: float, floor: int, amenities: List[str]):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.floor = floor
        self.amenities = amenities
        self.status = RoomStatus.AVAILABLE
        self.last_cleaned = datetime.now()
        self.maintenance_history: List[Dict] = []

    def get_info(self) -> Dict:
        return {
            "room_number": self.room_number,
            "type": self.room_type.name,
            "price": self.price_per_night,
            "floor": self.floor,
            "status": self.status.value,
            "amenities": self.amenities,
            "last_cleaned": self.last_cleaned.isoformat(),
        }

    def change_status(self, new_status: RoomStatus) -> bool:
        if self.status == RoomStatus.MAINTENANCE and new_status != RoomStatus.AVAILABLE:
            return False
        self.status = new_status
        if new_status == RoomStatus.AVAILABLE:
            self.last_cleaned = datetime.now()
        return True

    def add_maintenance_record(self, issue: str, fixed_by: str, cost: float):
        record = {"date": datetime.now().isoformat(), "issue": issue, "fixed_by": fixed_by, "cost": cost}
        self.maintenance_history.append(record)
        self.status = RoomStatus.MAINTENANCE

    def calculate_price_with_season(self, is_peak_season: bool, days: int) -> float:
        base_price = self.price_per_night * days
        if is_peak_season:
            return base_price * 1.5
        return base_price


# Guest Management
class Guest:
    def __init__(self, guest_id: str, name: str, email: str, phone: str, id_number: str, nationality: str):
        self.guest_id = guest_id
        self.name = name
        self.email = email
        self.phone = phone
        self.id_number = id_number
        self.nationality = nationality
        self.loyalty_points = 0
        self.reservation_history: List[str] = []
        self.preferences: Dict[str, any] = {}
        self.vip_status = False

    def add_loyalty_points(self, points: int):
        self.loyalty_points += points
        if self.loyalty_points >= 1000 and not self.vip_status:
            self.vip_status = True

    def use_loyalty_points(self, points: int) -> bool:
        if self.loyalty_points >= points:
            self.loyalty_points -= points
            return True
        return False

    def get_discount_rate(self) -> float:
        if self.vip_status:
            return 0.15
        elif self.loyalty_points >= 500:
            return 0.10
        elif self.loyalty_points >= 100:
            return 0.05
        return 0.0

    def add_preference(self, key: str, value: any):
        self.preferences[key] = value

    def get_profile(self) -> Dict:
        return {
            "guest_id": self.guest_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "nationality": self.nationality,
            "loyalty_points": self.loyalty_points,
            "vip_status": self.vip_status,
            "total_reservations": len(self.reservation_history),
        }


# Reservation System
class Reservation:
    _reservation_counter = 1000

    def __init__(self, guest: Guest, room: Room, check_in: datetime, check_out: datetime, num_guests: int):
        Reservation._reservation_counter += 1
        self.reservation_id = f"RES{Reservation._reservation_counter}"
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.num_guests = num_guests
        self.total_amount = 0.0
        self.paid_amount = 0.0
        self.services: List[Dict] = []
        self.status = "pending"
        self.special_requests: List[str] = []
        self.is_peak_season = False

    def calculate_total(self) -> float:
        days = (self.check_out - self.check_in).days
        if days <= 0:
            days = 1
        room_charge = self.room.calculate_price_with_season(self.is_peak_season, days)
        discount_rate = self.guest.get_discount_rate()
        room_charge = room_charge * (1 - discount_rate)
        service_charge = sum(s["price"] for s in self.services)
        tax = 0.10
        self.total_amount = (room_charge + service_charge) * (1 + tax)
        return self.total_amount

    def add_service(self, service_type: ServiceType, description: str, price: float):
        service = {
            "type": service_type.value,
            "description": description,
            "price": price,
            "timestamp": datetime.now().isoformat(),
        }
        self.services.append(service)

    def add_special_request(self, request: str):
        self.special_requests.append(request)

    def make_payment(self, amount: float, method: PaymentMethod) -> Dict:
        if self.total_amount == 0:
            self.calculate_total()
        self.paid_amount += amount
        remaining = self.total_amount - self.paid_amount
        payment_record = {
            "amount": amount,
            "method": method.value,
            "timestamp": datetime.now().isoformat(),
            "remaining": remaining,
        }
        if remaining <= 0:
            self.status = "paid"
        return payment_record

    def confirm_reservation(self) -> bool:
        if self.room.status == RoomStatus.AVAILABLE:
            self.room.change_status(RoomStatus.RESERVED)
            self.status = "confirmed"
            self.guest.reservation_history.append(self.reservation_id)
            return True
        return False

    def check_in_guest(self) -> bool:
        if self.status == "confirmed":
            self.room.change_status(RoomStatus.OCCUPIED)
            self.status = "checked_in"
            return True
        return False

    def check_out_guest(self) -> bool:
        if self.status == "checked_in" or self.status == "paid":
            self.room.change_status(RoomStatus.CLEANING)
            self.status = "completed"
            loyalty_points = int(self.total_amount / 10)
            self.guest.add_loyalty_points(loyalty_points)
            return True
        return False

    def get_reservation_details(self) -> Dict:
        return {
            "reservation_id": self.reservation_id,
            "guest_name": self.guest.name,
            "room_number": self.room.room_number,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
            "num_guests": self.num_guests,
            "total_amount": self.total_amount,
            "paid_amount": self.paid_amount,
            "status": self.status,
            "services_count": len(self.services),
            "special_requests": self.special_requests,
        }


# Staff Management
class Staff:
    def __init__(self, staff_id: str, name: str, role: StaffRole, salary: float, shift: str):
        self.staff_id = staff_id
        self.name = name
        self.role = role
        self.salary = salary
        self.shift = shift
        self.performance_score = 5.0
        self.tasks_completed: List[Dict] = []
        self.on_duty = False

    def clock_in(self):
        self.on_duty = True

    def clock_out(self):
        self.on_duty = False

    def complete_task(self, task_description: str, duration_minutes: int):
        task = {"description": task_description, "duration": duration_minutes, "completed_at": datetime.now().isoformat()}
        self.tasks_completed.append(task)

    def update_performance(self, score: float):
        self.performance_score = (self.performance_score + score) / 2

    def get_monthly_salary_with_bonus(self) -> float:
        bonus_multiplier = 1.0
        if self.performance_score >= 9.0:
            bonus_multiplier = 1.3
        elif self.performance_score >= 7.5:
            bonus_multiplier = 1.15
        elif self.performance_score >= 6.0:
            bonus_multiplier = 1.05
        return self.salary * bonus_multiplier


# Hotel Management System
class Hotel:
    def __init__(self, name: str, address: str, total_floors: int):
        self.name = name
        self.address = address
        self.total_floors = total_floors
        self.rooms: Dict[str, Room] = {}
        self.guests: Dict[str, Guest] = {}
        self.reservations: Dict[str, Reservation] = {}
        self.staff: Dict[str, Staff] = {}
        self.revenue: float = 0.0
        self.expenses: float = 0.0

    def add_room(self, room: Room) -> bool:
        if room.room_number not in self.rooms:
            self.rooms[room.room_number] = room
            return True
        return False

    def register_guest(self, guest: Guest) -> bool:
        if guest.guest_id not in self.guests:
            self.guests[guest.guest_id] = guest
            return True
        return False

    def hire_staff(self, staff: Staff) -> bool:
        if staff.staff_id not in self.staff:
            self.staff[staff.staff_id] = staff
            return True
        return False

    def create_reservation(
        self, guest_id: str, room_number: str, check_in: datetime, check_out: datetime, num_guests: int
    ) -> Optional[Reservation]:
        if guest_id not in self.guests or room_number not in self.rooms:
            return None
        guest = self.guests[guest_id]
        room = self.rooms[room_number]
        if room.status != RoomStatus.AVAILABLE:
            return None
        reservation = Reservation(guest, room, check_in, check_out, num_guests)
        self.reservations[reservation.reservation_id] = reservation
        return reservation

    def process_check_in(self, reservation_id: str) -> bool:
        if reservation_id in self.reservations:
            reservation = self.reservations[reservation_id]
            return reservation.check_in_guest()
        return False

    def process_check_out(self, reservation_id: str) -> Dict:
        if reservation_id in self.reservations:
            reservation = self.reservations[reservation_id]
            if reservation.check_out_guest():
                self.revenue += reservation.total_amount
                return {
                    "success": True,
                    "total_amount": reservation.total_amount,
                    "loyalty_points_earned": int(reservation.total_amount / 10),
                }
        return {"success": False}

    def search_available_rooms(
        self, room_type: Optional[RoomType] = None, min_price: float = 0, max_price: float = float("inf")
    ) -> List[Room]:
        available_rooms = []
        for room in self.rooms.values():
            if room.status == RoomStatus.AVAILABLE:
                if min_price <= room.price_per_night <= max_price:
                    if room_type is None or room.room_type == room_type:
                        available_rooms.append(room)
        return sorted(available_rooms, key=lambda r: r.price_per_night)

    def get_occupancy_rate(self) -> float:
        if not self.rooms:
            return 0.0
        occupied_rooms = sum(1 for room in self.rooms.values() if room.status == RoomStatus.OCCUPIED)
        return (occupied_rooms / len(self.rooms)) * 100

    def get_revenue_report(self) -> Dict:
        total_reservations = len(self.reservations)
        completed_reservations = sum(1 for r in self.reservations.values() if r.status == "completed")
        pending_revenue = sum(r.total_amount - r.paid_amount for r in self.reservations.values() if r.status != "completed")
        return {
            "total_revenue": self.revenue,
            "total_expenses": self.expenses,
            "net_profit": self.revenue - self.expenses,
            "total_reservations": total_reservations,
            "completed_reservations": completed_reservations,
            "pending_revenue": pending_revenue,
            "occupancy_rate": self.get_occupancy_rate(),
        }

    def schedule_maintenance(self, room_number: str, issue: str, staff_id: str, cost: float) -> bool:
        if room_number not in self.rooms or staff_id not in self.staff:
            return False
        room = self.rooms[room_number]
        staff = self.staff[staff_id]
        if staff.role != StaffRole.MAINTENANCE:
            return False
        room.add_maintenance_record(issue, staff.name, cost)
        self.expenses += cost
        staff.complete_task(f"Maintenance: {issue} in room {room_number}", 60)
        return True

    def assign_cleaning_task(self, room_number: str, staff_id: str) -> bool:
        if room_number not in self.rooms or staff_id not in self.staff:
            return False
        room = self.rooms[room_number]
        staff = self.staff[staff_id]
        if staff.role != StaffRole.HOUSEKEEPING:
            return False
        if room.status == RoomStatus.CLEANING:
            room.change_status(RoomStatus.AVAILABLE)
            staff.complete_task(f"Cleaned room {room_number}", 30)
            return True
        return False

    def get_staff_performance_report(self) -> List[Dict]:
        report = []
        for staff in self.staff.values():
            report.append(
                {
                    "staff_id": staff.staff_id,
                    "name": staff.name,
                    "role": staff.role.value,
                    "performance_score": staff.performance_score,
                    "tasks_completed": len(staff.tasks_completed),
                    "monthly_salary": staff.get_monthly_salary_with_bonus(),
                }
            )
        return sorted(report, key=lambda s: s["performance_score"], reverse=True)

    def get_guest_statistics(self) -> Dict:
        total_guests = len(self.guests)
        vip_guests = sum(1 for g in self.guests.values() if g.vip_status)
        avg_loyalty_points = sum(g.loyalty_points for g in self.guests.values()) / total_guests if total_guests > 0 else 0
        return {
            "total_guests": total_guests,
            "vip_guests": vip_guests,
            "regular_guests": total_guests - vip_guests,
            "average_loyalty_points": avg_loyalty_points,
        }


# Utility functions
def validate_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[1]


def validate_phone(phone: str) -> bool:
    cleaned = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")
    return cleaned.isdigit() and len(cleaned) >= 10


def calculate_days_between(date1: datetime, date2: datetime) -> int:
    return abs((date2 - date1).days)


def format_currency(amount: float, currency: str = "USD") -> str:
    return f"{currency} {amount:,.2f}"


def generate_invoice(reservation: Reservation) -> Dict:
    invoice = {
        "invoice_id": f"INV-{reservation.reservation_id}",
        "guest_name": reservation.guest.name,
        "room_number": reservation.room.room_number,
        "check_in": reservation.check_in.strftime("%Y-%m-%d"),
        "check_out": reservation.check_out.strftime("%Y-%m-%d"),
        "room_charges": reservation.room.calculate_price_with_season(
            reservation.is_peak_season, (reservation.check_out - reservation.check_in).days
        ),
        "service_charges": sum(s["price"] for s in reservation.services),
        "discount": reservation.room.calculate_price_with_season(
            reservation.is_peak_season, (reservation.check_out - reservation.check_in).days
        )
        * reservation.guest.get_discount_rate(),
        "tax": 0.10,
        "total_amount": reservation.total_amount,
        "paid_amount": reservation.paid_amount,
        "balance_due": reservation.total_amount - reservation.paid_amount,
    }
    return invoice
