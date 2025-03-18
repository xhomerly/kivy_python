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
            new_task = {
                "text": task_text,
                "completed": False,
                "urgent": False,
                "order": len(self.tasks)  # Pořadí podle aktuální délky seznamu
            }
            self.tasks.append(new_task)
            self.task_input.text = ''
            self.save_tasks()
            self.refresh_task_list()

    def move_task(self, task_text, direction):
        """ Přesune úkol nahoru nebo dolů podle direction ('up' nebo 'down') """
        index = next((i for i, task in enumerate(self.tasks) if task["text"] == task_text), None)
        if index is not None:
            if direction == "up" and index > 0:
                self.tasks[index], self.tasks[index - 1] = self.tasks[index - 1], self.tasks[index]
            elif direction == "down" and index < len(self.tasks) - 1:
                self.tasks[index], self.tasks[index + 1] = self.tasks[index + 1], self.tasks[index]

            # Aktualizujeme "order" podle nové pozice
            for i, task in enumerate(self.tasks):
                task["order"] = i

            self.save_tasks()
            self.refresh_task_list()

    def save_tasks(self):
        """ Uloží úkoly se správným pořadím """
        data = {
            "count": len(self.tasks),
            "tasks": sorted(self.tasks, key=lambda x: x["order"])  # Seřadíme podle pořadí
        }
        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        """ Načte úkoly a seřadí je podle pořadí """
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                data = json.load(f)
                self.tasks = sorted(data.get("tasks", []), key=lambda x: x.get("order", 0))  # Zajistíme správné pořadí

    def refresh_task_list(self):
        """ Obnoví seznam úkolů v UI """
        self.task_list.clear_widgets()
        for task in sorted(self.tasks, key=lambda x: x["order"]):  # Seřadíme podle pořadí
            task_item = TaskItem(
                text=task["text"],
                completed=task["completed"],
                urgent=task["urgent"],
                parent_list=self
            )
            self.task_list.add_widget(task_item)


class ToDoApp(App):
    def build(self):
        return ToDoList()


if __name__ == '__main__':
    ToDoApp().run()