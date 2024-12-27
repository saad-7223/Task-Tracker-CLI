import argparse
import os 
import json 
from datetime import datetime

class Task_Manager:
     
    def __init__(self , filename="tasks.json"): #default file name 
        self.filename = filename
        self.tasks = self.load_tasks()

    """ load tasks : loads the task into the file if it exists else creates a new one """
    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename , 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error : corrupted {self.filename} file. creating a new one")
                return {}
        return {}
    
    """ save tasks : saves the tasks to the given file """
    def save_tasks(self):
        with open(self.filename , 'w') as f:
            json.dump(self.tasks , f , indent=2)
            """indent means the number of spaces"""

    def add_tasks(self, title , description):
        if not title:
            raise ValueError("Task title cannot be empty")
        
        task_id = str(len(self.tasks) + 1)
        self.tasks[task_id] = {
            'title' : title,
            'description' : description,
            'status' : "not_done",
            'created_at' : datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'updated_at' : datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        self.save_tasks()
        print(f"Task {title} added succescfully with ID : {task_id}")
    
    def update_tasks(self, task_id, title=None , description = None):
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found")
        if title : 
            self.tasks[task_id]['title'] = title
        if description : 
            self.tasks[task_id]['description'] = description

        self.tasks[task_id]['updated_at'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.save_tasks()
        print(f"task {task_id} updated succesfully")

    def delete_tasks(self,task_id):
        if task_id not in self.tasks:
            raise ValueError(f"Task with Id {task_id} not found")
        
        del self.tasks[task_id]
        self.save_tasks()
        print(f"Task {task_id} deleted succesfully")
    
    def update_status(self,task_id,status):
        if task_id not in self.tasks:
            raise ValueError(f"Task with Id {task_id} not found")

        self.tasks[task_id]['status'] = status
        self.tasks[task_id]['updated_at'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.save_tasks()
        print(f"Task {task_id} marked as {status}") 

    def list_tasks(self , status=None):
        if not self.tasks:
            print("No task found")
        filter_tasks = self.tasks
        if status:
            filter_tasks = {k : v for k,v in self.tasks.items() if v['status'] == status}
            if not filter_tasks:
                print(f"No tasks found with status : {status}")
        print("\nTasks:")
        print("-"*50)
        for task_id , task in filter_tasks.items():
            print(f"ID : {task_id}")
            print(f"Title : {task['title']}")
            print(f"Description : {task['description']}")
            print(f"Status : {task['status']}")
            print(f"Created : {task['created_at']}")
            print(f"Upadted : {task['updated_at']}")
            print('='*50)

def main():
    parser = argparse.ArgumentParser(description='Task Manager CLI')
    subparser = parser.add_subparsers(dest='command',help="Commands")

    add_parser = subparser.add_parser('add' , help='Add a new task')
    add_parser.add_argument('title',help='Task title')
    add_parser.add_argument('description',help='Task description')

    update_parser = subparser.add_parser('update', help='Update a task')
    update_parser.add_argument('task_id', help='Task ID')
    update_parser.add_argument('--title', help='New task title')
    update_parser.add_argument('--description', help='New task description')

    delete_parser = subparser.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', help='Task ID')

    status_parser = subparser.add_parser('status', help='Update task status')
    status_parser.add_argument('task_id', help='Task ID')
    status_parser.add_argument('status', choices=['not_done', 'in_progress', 'done'], help='New status')

    list_parser = subparser.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', choices=['not_done', 'in_progress', 'done'], help='Filter by status')

    args = parser.parse_args()
    task_manager = Task_Manager()

    try:
        if args.command == 'add':
            task_manager.add_tasks(args.title,args.description)
        elif args.command == 'update':
            task_manager.update_tasks(args.task_id,args.title,args.description)
        elif args.command == 'delete':
            task_manager.delete_tasks(args.task_id)
        elif args.command == "status":
            task_manager.update_status(args.task_id,args.status)
        elif args.command == "list":
            task_manager.list_tasks(args.status)
        else:
            parser.print_help()
    except ValueError as e:
        print(f"Error : {str(e)}")
    except Exception as e:
        print(f"An unexpected error as occurred: {str(e)}")

if __name__ == '__main__':
    main()