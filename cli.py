import requests

BASE_URL = "http://127.0.0.1:5000"


class TodoCLI:
    def show_menu(self):
        """Display the main menu options."""
        print("\n-- ToDo CLI App (via API) --")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Delete Task")
        print("4. View Missing Priorities")
        print("5. Exit")

    def add_task(self):
        """Add a new task by sending a POST request to the API."""
        name = input("Enter task name: ").strip()
        if not name:
            print("Task name cannot be empty.")
            return

        try:
            priority = int(input("Enter task priority (positive integer): "))
        except ValueError:
            print("Priority must be an integer.")
            return

        if priority <= 0:
            print("Priority must be greater than 0.")
            return

        response = requests.post(f"{BASE_URL}/tasks", json={"name": name, "priority": priority})
        self._handle_response(response)

    def list_tasks(self):
        """List all tasks by sending a GET request to the API."""
        response = requests.get(f"{BASE_URL}/tasks")
        if response.status_code == 200:
            tasks = response.json()
            if not tasks:
                print("No tasks.")
                return
            for task in tasks:
                print(f"(ID: {task['id']}) Task: {task['name']} | Priority: [{task['priority']}]")
        else:
            print("Error fetching tasks.")

    def delete_task(self):
        """Delete a task by its ID using a DELETE request."""
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Invalid ID.")
            return

        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        self._handle_response(response)

    def view_missing_priorities(self):
        """View missing priorities by sending a GET request to the API."""
        response = requests.get(f"{BASE_URL}/tasks/missing_priorities")
        if response.status_code == 200:
            missing = response.json().get("missing_priorities", [])
            if missing:
                print("Missing priorities:", missing)
            else:
                print("No missing priorities.")
        else:
            print("Error retrieving missing priorities.")

    def _handle_response(self, response):
        """Helper to print the API message or error from a response."""
        try:
            data = response.json()
            print(data.get("message") or data.get("error", "Unknown error"))
        except ValueError:
            print("Invalid response from server.")

    def run(self):
        """Run the CLI app loop."""
        while True:
            self.show_menu()
            choice = input("Choose an option (1-5): ").strip()
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.delete_task()
            elif choice == '4':
                self.view_missing_priorities()
            elif choice == '5':
                print("Thanks for using the API-based ToDo App!")
                break
            else:
                print("Invalid option.")


if __name__ == '__main__':
    TodoCLI().run()
