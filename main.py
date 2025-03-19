from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

import json
import os


class TaskItem(BoxLayout):
    text = StringProperty()
    completed = BooleanProperty(False)
    urgent = BooleanProperty(False)
    parent_list = ObjectProperty()

    def __init__(self, text='', completed=False, urgent=False, parent_list=None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.completed = completed
        self.urgent = urgent
        self.parent_list = parent_list


class ToDoList(BoxLayout):
    task_input = ObjectProperty(None)
    task_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tasks = []
        self.load_tasks()
        self.refresh_task_list()

    def add_task(self):
        task_text = self.task_input.text.strip()
        if task_text:
            self.tasks.append({"text": task_text, "completed": False, "urgent": False})
            self.task_input.text = ''
            self.save_tasks()
            self.refresh_task_list()

    def toggle_complete(self, task_text):
        for task in self.tasks:
            if task["text"] == task_text:
                task["completed"] = not task["completed"]
                break
        self.save_tasks()
        self.refresh_task_list()

    def toggle_urgent(self, task_text):
        for task in self.tasks:
            if task["text"] == task_text:
                task["urgent"] = not task["urgent"]
                break
        self.save_tasks()
        self.refresh_task_list()

    def remove_task(self, task_text):
        self.tasks = [task for task in self.tasks if task["text"] != task_text]
        self.save_tasks()
        self.refresh_task_list()

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)

    def refresh_task_list(self):
        self.task_list.clear_widgets()
        for task in self.tasks:
            task_item = TaskItem(text=task["text"], completed=task["completed"], urgent=task["urgent"],
                                 parent_list=self)
            self.task_list.add_widget(task_item)


class ToDoApp(App):
    def build(self):
        return ToDoList()


if __name__ == '__main__':
    ToDoApp().run()