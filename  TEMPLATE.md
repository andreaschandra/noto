Below is a comprehensive and detailed prompt that describes how to build a simple “To-Do List” web application, covering the homepage, sign-in, sign-up, to-do list page, and profile page. It outlines the tech stack choices (Flask for the backend, SQLite for the database, JavaScript for client-side functionality, and Bootstrap for styling). You can use this prompt as a blueprint for planning or generating code with your chosen AI or reference it as a project guide.

──────────────────────────────────────────────────────────────
PROMPT TO BUILD A TO-DO LIST WEB APPLICATION
──────────────────────────────────────────────────────────────

Project Overview and Requirements:
- Build a To-Do List web app with the following pages:
– Homepage (landing page)
– User sign-in page
– User sign-up page
– Main to-do page (accessible after authentication)
– Profile page
• The application should allow users to:
– Register for an account
– Log in using their username/email and password
– Create, read, update, and delete to-do items
– Update their profile details (e.g., name, email, password)
– Log out securely

Technology Stack:
• Backend: Flask (Python)
– Use Flask to handle routes, process user requests, and communicate with the database.
– Use Flask’s session management to handle user authentication (or a library like Flask-Login).
• Database: SQLite
– Store user records (id, username, email, password (hashed), profile info).
– Store to-do items (id, user_id, description, created_at, is_complete).
– All data is stored in a single SQLite file (for example, “database.db”).
• Frontend: HTML, Bootstrap, JavaScript
– HTML for base structure and semantic markup.
– Bootstrap for responsive layout, components (forms, buttons, alerts), and styling.
– JavaScript for client-side logic (such as toggling UI elements, updating tasks asynchronously if desired).

Project Structure (suggested):
• project/
├─ app.py (main Flask application file)
├─ requirements.txt (list of dependencies, e.g., Flask)
├─ static/
│   ├─ css/
│   │   └─ custom.css (optional custom CSS overrides)
│   ├─ js/
│   │   └─ main.js (your main JavaScript file)
│   └─ images/ (logo or profile images if any)
├─ templates/
│   ├─ base.html (shared layout for all pages)
│   ├─ index.html (homepage)
│   ├─ login.html (sign in)
│   ├─ signup.html (sign up)
│   ├─ todo.html (to-do page)
│   └─ profile.html (user profile page)
└─ database.db (SQLite database file)

Detailed Features:

A. Homepage (index.html)
– Greeting or a short description of the app with a “Get Started” or “Sign In/Sign Up” button.
– Brief marketing-style information: how the app helps with productivity, data security, etc.
– Navigation links (if logged out: “Sign In” and “Register”; if logged in, direct them to “My Todo List”)

B. Sign-Up Page (signup.html)
– A Bootstrap form for username, email, and password.
– Include password confirmation field.
– On submit:
1. Validate that the username/email is not already taken.
2. Hash the password using a secure library (like werkzeug.security in Flask).
3. Insert the user data into the SQLite database.
4. Redirect to the sign-in page or automatically log in the newly registered user.
– Display error messages if validation fails (e.g., “Email already used,” “Passwords do not match,” etc.).

C. Sign-In Page (login.html)
– A Bootstrap form requesting email (or username) and password.
– On submit:
1. Validate that the email/password combination exists in the database.
2. If valid, set a session token to keep the user logged in.
3. Redirect the user to their to-do list page.
4. Display error messages if credentials are invalid.

D. To-Do Page (todo.html)
– Only accessible by authenticated users. If a user is not logged in, redirect them to the sign-in page.
– At the top, a text input to add a new task and a button labeled “Add Task.”
– List of existing tasks displayed in a Bootstrap card or list group:
▸ Each task item includes:
- Description text
- A button or checkbox to mark it as complete or incomplete
- A delete (trash/bin icon) button to remove it
- Possibly an edit button or an inline editing option for the task description
– Include dynamic features using JavaScript to update tasks without reloading the page (optional, could be done with simple form submission too).
– Provide a logout link/button in the header or navbar.

E. Profile Page (profile.html)
– Display current user information (username, email, joined date, etc.).
– Provide a form to update profile info (username, email, maybe password).
– Save updated information to the SQLite database.
– Optionally, provide an option to upload or change a profile image.

Backend (Flask) Guidelines:
• app.py setup:
– Import Flask, request, session, redirect, url_for, render_template, etc.
– Initialize Flask app.
– Configure a secret key for session encryption (app.secret_key = "some_secret_string").
• Database initialization:
– Create a database connection function that connects to SQLite (using sqlite3 in Python).
– Create tables if they do not exist:
1. users table with (id, username, email, password_hashed, created_at, etc.)
2. todos table with (id, user_id, description, is_complete, created_at, etc.)
• Routes:
– “/” (GET): Render the homepage (index.html).
– “/signup” (GET/POST): Render the sign-up form and handle new user registration.
– “/login” (GET/POST): Render the sign-in form, authenticate the user, set sessions.
– “/logout” (GET): Clear the session, redirect to homepage.
– “/todo” (GET/POST): Display the user’s tasks, handle new task creation.
▸ If using AJAX for creation/updating, create separate endpoints “/create_task” or “/update_task”.
– “/delete_task/int:task_id” (POST or GET): Delete the selected task.
– “/complete_task/int:task_id” or “/toggle_task/int:task_id”: Toggle task’s completion status.
– “/profile” (GET/POST): Retrieve user info, allow updates.

JavaScript Enhancements:
• Use main.js (in static/js/) to handle any dynamic or AJAX-based operations:
– Submitting a new task without page reload.
– Marking tasks as complete/incomplete with a toggle.
– Deleting tasks using a confirmation prompt.
• If not comfortable with AJAX or want simplicity, use standard form submissions and re-render pages through Flask.

Security and Best Practices:
• Always hash passwords using a library like bcrypt or werkzeug.security.generate_password_hash.
• Check user session on protected routes (like “/todo”, “/profile”).
• Use Flask’s “flash” method for error and success messages displayed in Bootstrap alert components.
• Validate form inputs on both client side (JavaScript or HTML5 validations) and server side.

Building & Deploying:
• Use a virtual environment for Python (optional but recommended).
• Install dependencies in requirements.txt (Flask, any other libraries).
• For deployment, you can host on platforms like Heroku, PythonAnywhere, or your own server:
– Make sure to configure environment variables (if needed) and set up the database properly.

Additional Notes:
• Include a “Remember Me” checkbox on the login page if you prefer longer sessions.
• Implement user-specific data by linking tasks to the user’s ID.
• Consider including pagination if users might have many tasks.
• Customize styles by overriding or extending Bootstrap classes in custom.css.