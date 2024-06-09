import sqlite3

class TodoList:
    def __init__(self, db_path='todo.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()
        self.migrate_schema()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    task TEXT NOT NULL,
                    completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)),
                    starred BOOLEAN NOT NULL CHECK (starred IN (0, 1)) DEFAULT 0
                )
            ''')

    def migrate_schema(self):
        try:
            self.conn.execute('ALTER TABLE tasks ADD COLUMN starred BOOLEAN NOT NULL DEFAULT 0')
        except sqlite3.OperationalError:
            # Column already exists
            pass

    def add_task(self, task):
        with self.conn:
            self.conn.execute('INSERT INTO tasks (task, completed, starred) VALUES (?, ?, ?)', (task, False, False))

    def get_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, task, completed, starred FROM tasks ORDER BY starred DESC, id')
        tasks = cursor.fetchall()
        return [{'id': row[0], 'task': row[1], 'completed': bool(row[2]), 'starred': bool(row[3])} for row in tasks]

    def mark_task_complete(self, task_id):
        with self.conn:
            self.conn.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))

    def delete_task(self, task_id):
        with self.conn:
            self.conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    def put_back_task(self, task_id):
        with self.conn:
            self.conn.execute('UPDATE tasks SET completed = 0 WHERE id = ?', (task_id,))

    def star_task(self, task_id):
        with self.conn:
            self.conn.execute('UPDATE tasks SET starred = 1 WHERE id = ?', (task_id,))

    def unstar_task(self, task_id):
        with self.conn:
            self.conn.execute('UPDATE tasks SET starred = 0 WHERE id = ?', (task_id,))
