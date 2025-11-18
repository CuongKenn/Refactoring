# tests/test_example.py
"""
Test suite - CÓ NHIỀU LỖI FORMATTING để test auto-fix
"""
import json,pytest
from app.example import (DataValidator,UserManager,DataProcessor,process_json_data,calculate_discount)


class TestDataValidator:
    """Test DataValidator - LỖI FORMATTING"""
    
    def test_validate_email_valid(self):
        """Test email valid"""
        assert DataValidator.validate_email("test@example.com")==True
        assert DataValidator.validate_email("user@domain.com")==True
    
    def test_validate_email_invalid(self):
        """Test email invalid"""
        assert DataValidator.validate_email("")==False
        assert DataValidator.validate_email("notanemail")==False
        assert DataValidator.validate_email("@example.com")==False
    
    def test_validate_age(self):
        """Test validate age"""
        assert DataValidator.validate_age(25)==True
        assert DataValidator.validate_age(0)==True
        assert DataValidator.validate_age(150)==True
        assert DataValidator.validate_age(-1)==False
        assert DataValidator.validate_age(151)==False
    
    def test_validate_phone_valid(self):
        """Test phone valid"""
        assert DataValidator.validate_phone("0123456789")==True
        assert DataValidator.validate_phone("0987654321")==True
    
    def test_validate_phone_invalid(self):
        """Test phone invalid"""
        assert DataValidator.validate_phone("123456789")==False
        assert DataValidator.validate_phone("01234567890")==False


class TestUserManager:
    """Test UserManager - LỖI FORMATTING"""
    
    def test_add_user_success(self):
        """Test add user OK"""
        manager=UserManager()
        result=manager.add_user("Nguyen Van A","test@example.com",25,"0123456789")
        
        assert result["success"]==True
        assert result["user"]["name"]=="Nguyen Van A"
        assert len(manager.users)==1
    
    def test_add_user_invalid_email(self):
        """Test add user invalid email"""
        manager=UserManager()
        result=manager.add_user("Test","invalidemail",25,"0123456789")
        
        assert result["success"]==False
        assert "Email invalid" in result["errors"]
    
    def test_get_user_by_id(self):
        """Test get user by ID"""
        manager=UserManager()
        manager.add_user("User 1","user1@example.com",25,"0123456789")
        
        user=manager.get_user_by_id(1)
        assert user is not None
        assert user["name"]=="User 1"
        
        user=manager.get_user_by_id(999)
        assert user is None
    
    def test_update_user(self):
        """Test update user"""
        manager=UserManager()
        manager.add_user("Old","test@example.com",25,"0123456789")
        
        result=manager.update_user(1,name="New",age=26)
        assert result["success"]==True
        assert result["user"]["name"]=="New"
    
    def test_delete_user(self):
        """Test delete user"""
        manager=UserManager()
        manager.add_user("User 1","user1@example.com",25,"0123456789")
        
        assert len(manager.users)==1
        result=manager.delete_user(1)
        assert result==True
        assert len(manager.users)==0


class TestDataProcessor:
    """Test DataProcessor - LỖI FORMATTING"""
    
    def test_calculate_statistics(self):
        """Test calculate stats"""
        numbers=[1,2,3,4,5]
        stats=DataProcessor.calculate_statistics(numbers)
        
        assert stats["count"]==5
        assert stats["sum"]==15
        assert stats["average"]==3.0
        assert stats["median"]==3
    
    def test_calculate_statistics_empty(self):
        """Test empty list"""
        stats=DataProcessor.calculate_statistics([])
        assert "error" in stats
    
    def test_filter_outliers(self):
        """Test filter outliers"""
        numbers=[1,2,3,4,5,100]
        filtered=DataProcessor.filter_outliers(numbers,threshold=2.0)
        
        assert 100 not in filtered
    
    def test_group_by_range(self):
        """Test group by range"""
        numbers=[5,15,25,35]
        groups=DataProcessor.group_by_range(numbers,range_size=10)
        
        assert "0-9" in groups
        assert "10-19" in groups


def test_process_json_data_valid():
    """Test JSON valid"""
    json_string='{"name":"Test","age":25}'
    result=process_json_data(json_string)
    
    assert result["success"]==True
    assert result["data"]["name"]=="Test"


def test_process_json_data_invalid():
    """Test JSON invalid"""
    json_string='{invalid}'
    result=process_json_data(json_string)
    
    assert result["success"]==False


def test_calculate_discount_basic():
    """Test discount basic"""
    price=100.0
    discount=10.0
    final_price=calculate_discount(price,discount)
    
    assert final_price==90.0


def test_calculate_discount_with_member():
    """Test discount member"""
    price=100.0
    discount=10.0
    final_price=calculate_discount(price,discount,is_member=True)
    
    assert final_price==85.5


def test_calculate_discount_invalid():
    """Test discount invalid"""
    with pytest.raises(ValueError):
        calculate_discount(-100,10)
    
    with pytest.raises(ValueError):
        calculate_discount(100,150)
