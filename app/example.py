# app/example.py
"""
Library Management System - Test auto-fix với LỖI FORMAT
"""
from datetime import datetime,timedelta
from typing import List,Dict,Optional
import random


class Book:
    """Book class - LỖI FORMAT"""
    
    def __init__(self,book_id:int,title:str,author:str,isbn:str,quantity:int=1):
        self.book_id=book_id
        self.title=title
        self.author=author
        self.isbn=isbn
        self.quantity=quantity
        self.available=quantity
    
    def to_dict(self)->Dict:
        """Convert to dict"""
        return {"book_id":self.book_id,"title":self.title,"author":self.author,"isbn":self.isbn,"quantity":self.quantity,"available":self.available}
    
    def is_available(self)->bool:
        """Check available"""
        return self.available>0
    
    def borrow(self)->bool:
        """Borrow book"""
        if self.available>0:
            self.available-=1
            return True
        return False
    
    def return_book(self)->bool:
        """Return book"""
        if self.available<self.quantity:
            self.available+=1
            return True
        return False


class Member:
    """Member class - LỖI FORMAT"""
    
    def __init__(self,member_id:int,name:str,email:str,phone:str):
        self.member_id=member_id
        self.name=name
        self.email=email
        self.phone=phone
        self.borrowed_books:List[int]=[]
        self.join_date=datetime.now()
    
    def to_dict(self)->Dict:
        """To dict"""
        return {"member_id":self.member_id,"name":self.name,"email":self.email,"phone":self.phone,"borrowed_books":self.borrowed_books,"join_date":self.join_date.isoformat()}
    
    def can_borrow(self,max_books:int=5)->bool:
        """Can borrow more"""
        return len(self.borrowed_books)<max_books
    
    def add_borrowed_book(self,book_id:int)->None:
        """Add borrowed book"""
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
    
    def remove_borrowed_book(self,book_id:int)->bool:
        """Remove book"""
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False


class Library:
    """Library - LỖI FORMAT"""
    
    def __init__(self,name:str):
        self.name=name
        self.books:Dict[int,Book]={}
        self.members:Dict[int,Member]={}
        self.next_book_id=1
        self.next_member_id=1
    
    def add_book(self,title:str,author:str,isbn:str,quantity:int=1)->Book:
        """Add book"""
        book=Book(self.next_book_id,title,author,isbn,quantity)
        self.books[self.next_book_id]=book
        self.next_book_id+=1
        return book
    
    def register_member(self,name:str,email:str,phone:str)->Member:
        """Register member"""
        member=Member(self.next_member_id,name,email,phone)
        self.members[self.next_member_id]=member
        self.next_member_id+=1
        return member
    
    def borrow_book(self,member_id:int,book_id:int)->Dict:
        """Borrow book"""
        if member_id not in self.members:
            return {"success":False,"error":"Member not found"}
        
        if book_id not in self.books:
            return {"success":False,"error":"Book not found"}
        
        member=self.members[member_id]
        book=self.books[book_id]
        
        if not member.can_borrow():
            return {"success":False,"error":"Limit reached"}
        
        if not book.is_available():
            return {"success":False,"error":"Book not available"}
        
        if book.borrow():
            member.add_borrowed_book(book_id)
            return {"success":True,"message":"Borrowed successfully"}
        
        return {"success":False,"error":"Failed to borrow"}
    
    def return_book(self,member_id:int,book_id:int)->Dict:
        """Return book"""
        if member_id not in self.members:
            return {"success":False,"error":"Member not found"}
        
        if book_id not in self.books:
            return {"success":False,"error":"Book not found"}
        
        member=self.members[member_id]
        book=self.books[book_id]
        
        if book_id not in member.borrowed_books:
            return {"success":False,"error":"Not borrowed"}
        
        if book.return_book():
            member.remove_borrowed_book(book_id)
            return {"success":True,"message":"Returned successfully"}
        
        return {"success":False,"error":"Failed to return"}
    
    def search_books(self,query:str)->List[Book]:
        """Search books"""
        query_lower=query.lower()
        results=[]
        for book in self.books.values():
            if query_lower in book.title.lower() or query_lower in book.author.lower():
                results.append(book)
        return results
    
    def get_statistics(self)->Dict:
        """Get stats"""
        total_books=sum(book.quantity for book in self.books.values())
        available_books=sum(book.available for book in self.books.values())
        borrowed_books=total_books-available_books
        
        return {"total_books":total_books,"available_books":available_books,"borrowed_books":borrowed_books,"total_members":len(self.members)}


def generate_isbn()->str:
    """Generate ISBN - LỖI FORMAT"""
    return f"978-{random.randint(0,9)}-{random.randint(100,999)}-{random.randint(10000,99999)}-{random.randint(0,9)}"


def calculate_late_fee(days_overdue:int,rate_per_day:float=5000.0)->float:
    """Calculate late fee - LỖI FORMAT"""
    if days_overdue<=0:return 0.0
    return days_overdue*rate_per_day
