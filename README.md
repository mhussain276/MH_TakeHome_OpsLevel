📝 ToDo CLI App
A simple command-line ToDo list manager built in Python, powered by a Flask-based REST API. This application allows users to create, list, delete, and analyze tasks based on priority — all in memory, with no external database or persistence.

✨ Features
✅ Add tasks with a custom priority (lower number = higher priority)

📋 List all tasks sorted by priority

🗑️ Delete tasks using their unique task ID

📉 View all missing priorities between 1 and the current maximum

🧠 Fully in-memory (no file/database storage required)

🌐 Powered by a lightweight Flask API backend

🖥️ Why I Chose a CLI + API Approach
The prompt emphasized building a simple, interactive, in-memory application — no persistence or complex infrastructure required.

By combining a Flask API backend with a CLI frontend, I was able to:

🚀 Separate core logic (API) from the interface (CLI)

💡 Focus on clean architecture and modularity

🧪 Keep the solution lightweight, testable, and extensible

This approach ensures:

🧱 Maintainable and scalable design

🔧 Easy extension in future phases (e.g., web UI, authentication, persistence)

♻️ Reusability of API across multiple interfaces

🔧 Next Steps / How I’d Extend This
If building for production or team collaboration, I'd consider:

📁 Persistence
Enable saving/loading tasks using:

JSON or CSV files

SQLite or a relational database (e.g., PostgreSQL)

🖼️ Web UI Layer
Build a frontend using:

HTML/CSS/JavaScript

Or React for a more dynamic experience

🧪 Testing
Add test coverage with:

unittest or pytest for API and CLI functionality

📦 Deployment
Dockerize the app

Deploy the API to a cloud service (e.g., Heroku or Render)