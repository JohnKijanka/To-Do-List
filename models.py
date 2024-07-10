import sqlite3

class Task:
    def __init__(self, id, task_name, is_completed=False):
        self.id = id
        self.task_name = task_name
        self.is_completed = is_completed

    @staticmethod
    def connect():
        return sqlite3.connect('tasks.db')

    @staticmethod
    def create_table():
        with Task.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    is_completed BOOLEAN NOT NULL CHECK (is_completed IN (0, 1))
                )
            ''')
            conn.commit()

    def save(self):
        with Task.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (id, task_name, is_completed) VALUES (?, ?, ?)
            ''', (self.id, self.task_name, self.is_completed))
            conn.commit()

    @staticmethod
    def get_task(identifier):
        query = ''
        if isinstance(identifier, int):
            query = 'SELECT * FROM tasks WHERE id = ?'
        elif isinstance(identifier, str):
            query = 'SELECT * FROM tasks WHERE task_name = ?'
        else:
            return None
        
        with Task.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (identifier,))
            row = cursor.fetchone()
            if row:
                return Task(*row)
            return None

    def update(self):
        with Task.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET task_name = ?, is_completed = ?
                WHERE id = ?
            ''', (self.task_name, self.is_completed, self.id))
            conn.commit()

    @staticmethod
    def delete(task_id):
        with Task.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()

    @staticmethod
    def get_first_unused_id():
        with Task.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM tasks ORDER BY id')
            rows = cursor.fetchall()
            if not rows:
                return 1  # If there are no tasks, return 1 as the first ID

            ids = [row[0] for row in rows]
            for i in range(1, len(ids) + 1):
                if i != ids[i - 1]:
                    return i
            return len(ids) + 1

    @staticmethod
    def get_all_tasks():
        with Task.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks')
            rows = cursor.fetchall()
            return [Task(*row) for row in rows]

    def __repr__(self):
        return f'Task(id={self.id}, task_name="{self.task_name}", is_completed={self.is_completed})'