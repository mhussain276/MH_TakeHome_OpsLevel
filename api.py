from flask import Flask, request, jsonify

app = Flask(__name__)

todo_items = {}
next_id = 1


class InvalidUsage(Exception):
    """Custom exception class for validation or logical errors."""
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'error': self.message}


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handles custom InvalidUsage errors."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(404)
def not_found(error):
    """Handles 404 Not Found errors."""
    return jsonify({'error': 'Resource not found'}), 404


def get_priority(task_tuple):
    """Returns the priority of a task for sorting."""
    return task_tuple[1]['priority']


@app.route('/tasks', methods=['POST'])
def add_task():
    """
    Adds a new task with a given name and priority.
    Expects JSON with 'name' (string) and 'priority' (positive int).
    """
    global next_id
    data = request.get_json()

    if not data:
        raise InvalidUsage('Missing JSON payload')

    name = data.get('name', '').strip()
    priority = data.get('priority')

    if not name:
        raise InvalidUsage('Task name cannot be empty')
    if not isinstance(priority, int):
        raise InvalidUsage('Priority must be an integer')
    if priority <= 0:
        raise InvalidUsage('Priority must be greater than 0')

    todo_items[next_id] = {'name': name, 'priority': priority}
    next_id += 1
    return jsonify({'message': 'Task added'}), 201


@app.route('/tasks', methods=['GET'])
def list_tasks():
    """
    Returns a list of all tasks sorted by priority.
    Each task includes its ID, name, and priority.
    """
    sorted_tasks = sorted(todo_items.items(), key=get_priority)
    tasks_with_id = [
        {'id': tid, 'name': data['name'], 'priority': data['priority']}
        for tid, data in sorted_tasks
    ]
    return jsonify(tasks_with_id)


@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Deletes the task with the specified ID.
    Returns an error if the ID is invalid or the task is not found.
    """
    try:
        task_id = int(task_id)
        if task_id <= 0:
            raise ValueError
    except ValueError:
        raise InvalidUsage("Task ID must be a positive integer")

    if task_id not in todo_items:
        raise InvalidUsage(f'Task with ID {task_id} not found', status_code=404)

    del todo_items[task_id]
    return jsonify({'message': 'Task deleted'}), 200


@app.route('/tasks/missing_priorities', methods=['GET'])
def missing_priorities():
    """
    Returns a list of missing priority numbers between 1 and the maximum assigned priority.
    """
    if not todo_items:
        return jsonify({'missing_priorities': []})

    priorities = [item['priority'] for item in todo_items.values()]
    max_priority = max(priorities)
    existing_set = set(priorities)

    missing = [p for p in range(1, max_priority + 1) if p not in existing_set]
    return jsonify({'missing_priorities': missing})


if __name__ == '__main__':
    app.run(debug=True)
