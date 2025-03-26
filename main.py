import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class TaskItem(BoxLayout):
    time = StringProperty()
    title = StringProperty()
    location = StringProperty()
    done = BooleanProperty(False)

    def toggle_done(self, checkbox, value):
        self.done = value
        tasks = load_tasks()
        for task in tasks:
            if task['title'] == self.title and task['time'] == self.time:
                task['done'] = value
        save_tasks(tasks)

class MainScreen(Screen):
    def on_pre_enter(self):
        self.update_tasks()

    def update_tasks(self):
        self.ids.tasks_box.clear_widgets()
        tasks = load_tasks()
        for task in tasks:
            self.ids.tasks_box.add_widget(TaskItem(
                time=task['time'],
                title=task['title'],
                location=task['location'],
                done=task.get('done', False)
            ))

class AddTaskScreen(Screen):
    def save_task(self):
        title = self.ids.task_title.text
        location = self.ids.task_location.text
        time = self.ids.task_time.text

        if not title or not time:
            return

        tasks = load_tasks()
        tasks.append({
            'title': title,
            'location': location,
            'time': time,
            'done': False
        })
        save_tasks(tasks)

        self.manager.current = 'main'

        self.ids.task_title.text = ''
        self.ids.task_location.text = ''
        self.ids.task_time.text = ''

class TodoApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AddTaskScreen(name='add'))
        return sm

if __name__ == "__main__":
    TodoApp().run()
