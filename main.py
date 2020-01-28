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
        path = os.getcwd()
        try:
            os.mkdir('tasks')
        except OSError:
            print(f'Creation of the directory {path} failed')
        else:
            print(f'Successfully created the directory {path}')
        files_path = f'{path}/tasks'
        return files_path

    @staticmethod
    def check_report(files_path, user):
        # check old report
        # '23.09.2020 15:25'
        file_path = f'{files_path}//{user["username"]}.txt'
        if os.path.exists(file_path):
            time_of_create_file = os.path.getmtime(file_path)
            new_time = datetime.fromtimestamp(time_of_create_file).strftime('%Y-%m-%dT%H:%M')
            new_file_path = f'{files_path}//{user["username"]}_{new_time}.txt'
            os.rename(file_path, new_file_path)

    @staticmethod
    def write_todos(files_path, user, true_todo, false_todo):
        # write task in report on disk
        time = strftime('%d.%m.%Y %H:%M')
        file_path = f'{files_path}//{user["username"]}.txt'
        try:
            f = open(file_path, 'w+')
            # message in begin of file
            start_message = (
                f'{user["name"]} - <{user["email"]}> {time}\n'
                f'{user["company"]["name"]}\n\n'
                'Завершенные задачи: \n'
            )
            f.write(start_message)
            for todo in true_todo:
                f.write(f'{todo}...\n')
            f.write(f'\n\nОставшиеся задачи:\n')
            for todo in false_todo:
                f.write(f'{todo}...\n')
            f.close()
        except OSError:
            print('Fail write to disk')

    def find_true_todo(self, user):
        # find true task and return tuple for speed
        true_todo = []
        for todo in self.todos:
            if todo.get('userId') == user['id']:
                new_todo_title = todo['title'][:50] if len(todo['title']) > 50 else todo['title']
                if todo.get('completed'):
                    true_todo.append(new_todo_title)
        true_todo = tuple(true_todo)
        return true_todo

    def find_false_todo(self, user):
        # find false task and return tuple for speed
        false_todo = []
        for todo in self.todos:
            if todo.get('userId') == user['id']:
                new_todo_title = todo['title'][:50] if len(todo['title']) > 50 else todo['title']
                if not todo.get('completed'):
                    false_todo.append(new_todo_title)
        false_todo = tuple(false_todo)
        return false_todo


if __name__ == "__main__":
    order = OrderHandler()
    order.get_data()
