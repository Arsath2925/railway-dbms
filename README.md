# Railway Database Management System (DBMS)

A web-based Railway Management System built with **Python (Flask)** and **SQL** implementing complete CRUD workflows, transactional integrity, dynamic seat allotment, and ticket cancellation logic.

## Key Features
- **SQL CRUD Actions:** Query real-time train status, insert new ticket reservations, update seat counters atomically, and remove bookings.
- **Transactional Consistency:** Validates seat inventory before confirming reservations.
- **Glassmorphic UI:** Styled with modern, high-contrast dark-mode dashboard.

## Setup & Run Locally
```bash
git clone https://github.com/Arsath2925/railway-dbms.git
cd railway-dbms
pip install -r requirements.txt
python app.py