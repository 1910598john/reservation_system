🏨 Hotel Reservation System
A simple desktop-based reservation system designed to help front desk staff manage hotel guest bookings with ease. Built using Python (Tkinter) for the GUI and MySQL for the backend database.

✨ Features
📌 Book Room – Register a new guest and assign a room

❌ Cancel Booking – Remove an existing reservation

✅ Check-In – Mark a guest as checked-in

🧾 Check-Out – Finalize stay and free up the room

📋 View Available Rooms – Check which rooms are currently unoccupied

👤 View Guest Records – Access information on all guests, past and present

🛠 Technologies Used
Frontend: Python + Tkinter

Backend: MySQL

Database Connectivity: MySQL Connector for Python

⚙️ Setup Instructions
Clone this repository

bash
Copy
Edit
git clone https://github.com/1910598john/reservation_system.git
cd reservation_system
Set up MySQL database

Create a database (e.g. hotel_db)

Run the SQL schema file (if provided) or create the tables manually as needed.

Install Python dependencies

bash
Copy
Edit
pip install mysql-connector-python
Configure database settings

Update your MySQL connection settings in the Python script (host, username, password, database name)

Run the application

bash
Copy
Edit
python main.py

