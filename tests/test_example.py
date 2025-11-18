# tests/test_example.py
"""
Tests for Library - LỖI FORMAT
"""
import pytest
from app.example import Book,Member,Library,generate_isbn,calculate_late_fee


class TestBook:
    """Test Book"""
    
    def test_book_creation(self):
        """Test create"""
        book=Book(1,"Python","John","ISBN123",5)
        
        assert book.book_id==1
        assert book.title=="Python"
        assert book.quantity==5
    
    def test_book_borrow(self):
        """Test borrow"""
        book=Book(1,"Test","Author","ISBN",2)
        
        assert book.borrow()==True
        assert book.available==1
        
        assert book.borrow()==True
        assert book.available==0
        
        assert book.borrow()==False
    
    def test_book_return(self):
        """Test return"""
        book=Book(1,"Test","Author","ISBN",2)
        book.available=0
        
        assert book.return_book()==True
        assert book.available==1


class TestMember:
    """Test Member"""
    
    def test_member_creation(self):
        """Test create"""
        member=Member(1,"John","john@test.com","0123456789")
        
        assert member.member_id==1
        assert member.name=="John"
        assert len(member.borrowed_books)==0
    
    def test_can_borrow(self):
        """Test can borrow"""
        member=Member(1,"Test","test@test.com","0123")
        
        assert member.can_borrow(5)==True
        
        member.borrowed_books=[1,2,3,4,5]
        assert member.can_borrow(5)==False


class TestLibrary:
    """Test Library"""
    
    def test_library_creation(self):
        """Test create"""
        library=Library("City Library")
        
        assert library.name=="City Library"
        assert len(library.books)==0
    
    def test_add_book(self):
        """Test add book"""
        library=Library("Test")
        book=library.add_book("Python","John","ISBN",3)
        
        assert book.book_id==1
        assert len(library.books)==1
    
    def test_register_member(self):
        """Test register"""
        library=Library("Test")
        member=library.register_member("Jane","jane@test.com","0987")
        
        assert member.member_id==1
        assert len(library.members)==1
    
    def test_borrow_book_success(self):
        """Test borrow OK"""
        library=Library("Test")
        book=library.add_book("Book","Author","ISBN",2)
        member=library.register_member("User","test@test.com","0123")
        
        result=library.borrow_book(member.member_id,book.book_id)
        
        assert result["success"]==True
        assert book.available==1
    
    def test_return_book_success(self):
        """Test return OK"""
        library=Library("Test")
        book=library.add_book("Book","Author","ISBN",1)
        member=library.register_member("User","test@test.com","0123")
        
        library.borrow_book(member.member_id,book.book_id)
        result=library.return_book(member.member_id,book.book_id)
        
        assert result["success"]==True
        assert book.available==1
    
    def test_search_books(self):
        """Test search"""
        library=Library("Test")
        library.add_book("Python Programming","John","ISBN1")
        library.add_book("Java Basics","Jane","ISBN2")
        
        results=library.search_books("Python")
        assert len(results)==1
    
    def test_get_statistics(self):
        """Test stats"""
        library=Library("Test")
        library.add_book("Book 1","Author","ISBN1",3)
        library.add_book("Book 2","Author","ISBN2",2)
        member=library.register_member("Test","test@test.com","0123")
        library.borrow_book(member.member_id,1)
        
        stats=library.get_statistics()
        
        assert stats["total_books"]==5
        assert stats["borrowed_books"]==1


def test_generate_isbn():
    """Test ISBN"""
    isbn=generate_isbn()
    
    assert isbn.startswith("978-")
    assert len(isbn)>=15


def test_calculate_late_fee():
    """Test late fee"""
    assert calculate_late_fee(0)==0.0
    assert calculate_late_fee(3)==15000.0
    assert calculate_late_fee(10)==50000.0
