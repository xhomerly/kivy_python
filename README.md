# TODO list app in kivy 📝✅
This is a simple mobile application built using kivy. It serves as a year-ending project for Mr. Čapek.

- Adding new tasks
- Displaying a task list
- Saving tasks in a local JSON file
- Marking tasks as complete with a checkbox
- Persistent storage of checked state

## 📁 Project Structure

```
todo_app/
├── main.py          # Main Python application file
├── todo.kv          # Kivy language file for UI
├── tasks.json       # Task data stored locally
```

## ▶️ How to Run

1. Install Kivy (if you haven't already):

```bash
pip install kivy
```

2. Run the application:

```bash
python main.py
```

The application window will open with the list of tasks from `tasks.json`. You can check/uncheck tasks, and add new ones.

## 💾 Data Storage

Tasks are saved in a simple JSON file `tasks.json` in the following format:

```json
[
    {
        "title": "Weekly Review",
        "location": "Wanda Square E5",
        "time": "3:00 PM",
        "done": false
    }
]
```