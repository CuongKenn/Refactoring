"""Unit tests for Task Management System"""

import pytest
from datetime import datetime,timedelta
from app.example import(Task,Project,User,TaskPriority,TaskStatus,ProjectStatus,create_task_with_defaults,calculate_project_progress,find_overdue_tasks,get_high_priority_tasks,estimate_project_delay)


class TestTask:
    def test_task_creation(self):
        due_date=datetime.now()+timedelta(days=7)
        task=Task(task_id="T001",title="Test Task",description="Test Description",priority=TaskPriority.HIGH,due_date=due_date)
        assert task.task_id=="T001"
        assert task.status==TaskStatus.TODO
        assert task.assigned_to is None
        
    def test_task_assignment(self):
        due_date=datetime.now()+timedelta(days=7)
        task=Task(task_id="T002",title="Test Task",description="Test Description",priority=TaskPriority.MEDIUM,due_date=due_date)
        result=task.assign_to("USER001")
        assert result==True
        assert task.assigned_to=="USER001"
        assert task.status==TaskStatus.IN_PROGRESS
        
    def test_task_status_update(self):
        due_date=datetime.now()+timedelta(days=7)
        task=Task(task_id="T003",title="Test Task",description="Test Description",priority=TaskPriority.LOW,due_date=due_date)
        task.update_status(TaskStatus.DONE)
        assert task.status==TaskStatus.DONE
        assert task.completed_at is not None
        
    def test_task_overdue_check(self):
        past_date=datetime.now()-timedelta(days=1)
        task=Task(task_id="T004",title="Overdue Task",description="Test",priority=TaskPriority.URGENT,due_date=past_date)
        assert task.is_overdue()==True


class TestProject:
    def test_project_creation(self):
        start=datetime.now()
        end=start+timedelta(days=30)
        project=Project(project_id="P001",name="Test Project",description="Test Desc",start_date=start,end_date=end)
        assert project.project_id=="P001"
        assert project.status==ProjectStatus.PLANNING
        assert len(project.tasks)==0
        
    def test_add_task_to_project(self):
        start=datetime.now()
        end=start+timedelta(days=30)
        project=Project(project_id="P002",name="Test Project",description="Test Desc",start_date=start,end_date=end)
        task=Task(task_id="T005",title="Project Task",description="Task Desc",priority=TaskPriority.HIGH,due_date=end)
        result=project.add_task(task)
        assert result==True
        assert len(project.tasks)==1
        
    def test_add_team_member(self):
        start=datetime.now()
        end=start+timedelta(days=30)
        project=Project(project_id="P003",name="Test Project",description="Test Desc",start_date=start,end_date=end)
        result=project.add_team_member("USER001")
        assert result==True
        assert"USER001"in project.team_members
        
    def test_project_task_stats(self):
        start=datetime.now()
        end=start+timedelta(days=30)
        project=Project(project_id="P004",name="Test Project",description="Test Desc",start_date=start,end_date=end)
        task1=Task(task_id="T006",title="Task 1",description="Desc",priority=TaskPriority.LOW,due_date=end)
        task2=Task(task_id="T007",title="Task 2",description="Desc",priority=TaskPriority.MEDIUM,due_date=end)
        project.add_task(task1)
        project.add_task(task2)
        task1.update_status(TaskStatus.DONE)
        stats=project.get_task_stats()
        assert stats["total"]==2
        assert stats["completed"]==1


class TestUser:
    def test_user_creation(self):
        user=User(user_id="U001",name="John Doe",email="john@example.com",role="Developer")
        assert user.user_id=="U001"
        assert user.completed_tasks_count==0
        
    def test_user_assign_task(self):
        user=User(user_id="U002",name="Jane Doe",email="jane@example.com",role="Manager")
        task=Task(task_id="T008",title="User Task",description="Desc",priority=TaskPriority.HIGH,due_date=datetime.now()+timedelta(days=5))
        result=user.assign_task(task)
        assert result==True
        assert len(user.assigned_tasks)==1
        
    def test_user_complete_task(self):
        user=User(user_id="U003",name="Bob Smith",email="bob@example.com",role="Developer")
        task=Task(task_id="T009",title="Complete Task",description="Desc",priority=TaskPriority.MEDIUM,due_date=datetime.now()+timedelta(days=3))
        user.assign_task(task)
        result=user.complete_task(task)
        assert result==True
        assert user.completed_tasks_count==1


class TestUtilityFunctions:
    def test_create_task_with_defaults(self):
        task=create_task_with_defaults(title="Default Task",description="Test Description")
        assert task.priority==TaskPriority.MEDIUM
        assert task.status==TaskStatus.TODO
        
    def test_calculate_project_progress(self):
        start=datetime.now()
        end=start+timedelta(days=30)
        project=Project(project_id="P005",name="Progress Test",description="Test",start_date=start,end_date=end)
        task1=Task(task_id="T010",title="Task 1",description="Desc",priority=TaskPriority.LOW,due_date=end)
        task2=Task(task_id="T011",title="Task 2",description="Desc",priority=TaskPriority.LOW,due_date=end)
        project.add_task(task1)
        project.add_task(task2)
        task1.update_status(TaskStatus.DONE)
        progress=calculate_project_progress(project)
        assert progress==50.0
        
    def test_find_overdue_tasks(self):
        past_date=datetime.now()-timedelta(days=1)
        future_date=datetime.now()+timedelta(days=1)
        task1=Task(task_id="T012",title="Overdue",description="Desc",priority=TaskPriority.HIGH,due_date=past_date)
        task2=Task(task_id="T013",title="On Time",description="Desc",priority=TaskPriority.LOW,due_date=future_date)
        overdue=find_overdue_tasks([task1,task2])
        assert len(overdue)==1
        assert overdue[0].task_id=="T012"
        
    def test_get_high_priority_tasks(self):
        due=datetime.now()+timedelta(days=7)
        task1=Task(task_id="T014",title="High",description="Desc",priority=TaskPriority.HIGH,due_date=due)
        task2=Task(task_id="T015",title="Low",description="Desc",priority=TaskPriority.LOW,due_date=due)
        task3=Task(task_id="T016",title="Urgent",description="Desc",priority=TaskPriority.URGENT,due_date=due)
        high_priority=get_high_priority_tasks([task1,task2,task3])
        assert len(high_priority)==2
        
    def test_estimate_project_delay(self):
        past_end=datetime.now()-timedelta(days=5)
        start=past_end-timedelta(days=30)
        project=Project(project_id="P006",name="Delayed Project",description="Test",start_date=start,end_date=past_end)
        delay=estimate_project_delay(project)
        assert delay>=5
