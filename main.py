import requests
import json
import os

from time import strftime
from datetime import datetime


class OrderHandler:
    def __init__(self):
        try:
            self._response_todos = requests.get('https://json.medrating.org/todos')
            self._response_users = requests.get('https://json.medrating.org/users')
        except requests.exceptions.ConnectionError:
            print('Connection Error')
        try:
            self.todos = json.loads(self._response_todos.text)
            self.users = json.loads(self._response_users.text)
        except AttributeError:
            print('Not have data from api')

    def get_data(self):
        files_path = self.create_dir()
        try:
            for user in self.users:
                true_todo = self.find_true_todo(user)
                false_todo = self.find_false_todo(user)
                self.check_report(files_path, user)
                self.write_todos(files_path, user, true_todo, false_todo)
        except AttributeError:
            print('Not users')

    @staticmethod
    def create_dir():
        """Create dir for reports"""
        path = os.getcwd()
        try:
            os.mkdir('tasks')
        except OSError:
            print(f'Creation of the directory {path} failed')
        print(f'Successfully created the directory {path}')
        files_path = f'{path}/tasks'
        return files_path

    @staticmethod
    def check_report(files_path, user):
        """Check old reports"""
        file_path = f'{files_path}//{user["username"]}.txt'
        if os.path.exists(file_path):
            time_of_create_file = os.path.getmtime(file_path)
            new_time = datetime.fromtimestamp(
                time_of_create_file
            ).strftime('%Y-%m-%dT%H:%M')
            new_file_path = f'{files_path}//{user["username"]}_{new_time}.txt'
            os.rename(file_path, new_file_path)

    def write_todos(self, files_path, user, true_todo, false_todo):
        """Write task in on disk"""
        time = strftime('%d.%m.%Y %H:%M')
        file_path = f'{files_path}//{user["username"]}.txt'
        try:
            with open(file_path, 'w+') as f:
                # message in begin of file
                start_message = (
                    f'{user["name"]} <{user["email"]}> {time}\n'
                    f'{user["company"]["name"]}\n\n'
                    'Завершенные задачи: \n'
                )
                f.write(start_message)
                self.file_write_todos(f, true_todo)
                f.write(f'\nОставшиеся задачи:\n')
                self.file_write_todos(f, false_todo)
        except OSError:
            print('Fail write to disk')

    @staticmethod
    def file_write_todos(f, todos):
        """Write todos in file"""
        for todo in todos:
            f.write(f'{todo}\n')

    def find_true_todo(self, user):
        """Find true tasks"""
        true_todo = []
        for todo in self.todos:
            if todo.get('userId') == user['id']:
                new_todo_title = self.rename_task_title(todo.get('title'))
                if todo.get('completed'):
                    true_todo.append(new_todo_title)
        true_todo = tuple(true_todo)
        return true_todo

    def find_false_todo(self, user):
        """Find false tasks"""
        false_todo = []
        for todo in self.todos:
            if todo.get('userId') == user['id']:
                new_todo_title = self.rename_task_title(todo.get('title'))
                if not todo.get('completed'):
                    false_todo.append(new_todo_title)
        false_todo = tuple(false_todo)
        return false_todo

    @staticmethod
    def rename_task_title(title):
        """Splice title task if length of title > 50"""
        if len(title) > 50:
            new_title_task = f"{title[:50]}..."
        else:
            new_title_task = title
        return new_title_task


if __name__ == "__main__":
    order = OrderHandler()
    order.get_data()
