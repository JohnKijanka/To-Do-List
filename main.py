from fastapi import FastAPI
from models import Task
from typing import Optional

app = FastAPI()

#Load table from database if its already made
Task.create_table()

@app.get("/")
def print_to_do_list():
    tasks = Task.get_all_tasks()
    return tasks

@app.post("/add_task/{task_name}")
def add_task(task_name: str, q: Optional[bool] = False):
    # Create new task
    task1 = Task(Task.get_first_unused_id(), task_name, q)
    task1.save()
    return task1

@app.get("/task/{task_id}")
def print_task(task_id: int):
    # print a single task
    task1 = Task.get_task(task_id)
    return task1

@app.delete("/delete_task/{task_id}")
def delete_task(task_id: int):
    # delete a single task
    Task.delete(task_id)
    return True

@app.put("/mark_completed/{task_id}")
def mark_completed(task_id: int):
    # complete a single task
    task1 = Task.get_task(task_id)
    task1.is_completed = True
    task1.update()
    return True

@app.put("/mark_uncompleted/{task_id}")
def mark_uncompleted(task_id: int):
    # uncomplete a single task
    task1 = Task.get_task(task_id)
    task1.is_completed = False
    task1.update()
    return True