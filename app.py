from flask import Flask, render_template, request, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = "railway_secret_key"

database.init_db()

@app.route('/')
def index():
    conn = database.get_connection()
    trains = conn.execute('SELECT * FROM trains').fetchall()
    bookings = conn.execute('''
        SELECT b.booking_id, b.passenger_name, b.seat_number, b.status, t.train_name, t.train_number
        FROM bookings b
        JOIN trains t ON b.train_number = t.train_number
        ORDER BY b.booking_id DESC
    ''').fetchall()
    conn.close()
    return render_template('index.html', trains=trains, bookings=bookings)

@app.route('/book', methods=['POST'])
def book_ticket():
    passenger_name = request.form.get('passenger_name').strip()
    train_number = request.form.get('train_number')

    if not passenger_name or not train_number:
        flash("All fields are required!", "error")
        return redirect(url_for('index'))

    conn = database.get_connection()
    train = conn.execute('SELECT * FROM trains WHERE train_number = ?', (train_number,)).fetchone()

    if train and train['seats_available'] > 0:
        assigned_seat = (train['seats_available'] % 100) + 1
        
        # Insert booking
        conn.execute('''
            INSERT INTO bookings (passenger_name, train_number, seat_number, status)
            VALUES (?, ?, ?, ?)
        ''', (passenger_name, train_number, assigned_seat, "CONFIRMED"))

        # Decrement seat count
        conn.execute('''
            UPDATE trains SET seats_available = seats_available - 1
            WHERE train_number = ?
        ''', (train_number,))

        conn.commit()
        conn.close()
        flash(f"Ticket booked successfully for {passenger_name}! Seat #{assigned_seat}", "success")
    else:
        conn.close()
        flash("No seats available on selected train!", "error")

    return redirect(url_for('index'))

@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_ticket(booking_id):
    conn = database.get_connection()
    booking = conn.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,)).fetchone()

    if booking:
        # Increment available seats back
        conn.execute('UPDATE trains SET seats_available = seats_available + 1 WHERE train_number = ?', (booking['train_number'],))
        # Delete booking record
        conn.execute('DELETE FROM bookings WHERE booking_id = ?', (booking_id,))
        conn.commit()
        flash("Ticket reservation cancelled and seat refunded.", "info")
    
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)