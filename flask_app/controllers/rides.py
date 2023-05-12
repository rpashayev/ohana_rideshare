from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import ride, user

@app.route('/rides')
def start_page():
    if 'id' not in session:
        return redirect('/logout')
    id = {
        'id': session['id']
    }
    
    return render_template('rides.html', booked_rides = ride.Ride.booked_rides(), requested_rides = ride.Ride.requested_rides(), one_user = user.User.get_one_user(id))

@app.route('/rides/create')
def show_create_page():
    if 'id' not in session:
        return redirect('/logout')
    return render_template('new_ride.html')

@app.route('/rides/save', methods=['POST'])
def create_ride():
    if not ride.Ride.validate_ride(request.form):
        return redirect('/rides/create')
    
    data = {
        'destination': request.form['destination'],
        'pickup': request.form['pickup'],
        'ride_date': request.form['ride_date'],
        'details': request.form['details'],
        'rider_id': session['id']
    }
    
    ride.Ride.save_ride(data)
    
    return redirect('/rides')

@app.route('/rides/edit/<int:ride_id>')
def show_edit_page(ride_id):
    if 'id' not in session:
        return redirect('/logout')    
    data = {
        'id': ride_id
    }
    return render_template('edit_ride.html', ride=ride.Ride.one_requested_ride(data))

@app.route('/rides/edit', methods=['POST'])
def edit_ride():
    if not ride.Ride.validate_ride_edit(request.form):
        return redirect(f'/rides/edit/{request.form["id"]}')
    data = {
        'pickup': request.form['pickup'],
        'details': request.form['details'],
        'id': request.form['id'] 
    }
    
    ride.Ride.edit_ride(data)
    
    return redirect('/rides')

@app.route('/rides/delete', methods=['POST'])
def delete_one_ride():
    
    ride.Ride.delete_ride(request.form)
    
    return redirect('/rides')

@app.route('/rides/view/<int:ride_id>')
def show_one_ride(ride_id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': ride_id
    }
    user_id = {
        'id': session['id']
    }
    return render_template('view_ride.html', ride=ride.Ride.one_booked_ride(data), user=user.User.get_one_user(user_id))

@app.route('/rides/add_driver/<int:ride_id>')
def add_driver(ride_id):
    if 'id' not in session:
        return redirect('/logout')    
    
    data = {
        'id': ride_id,
        'driver_id': session['id']
    }
    
    ride.Ride.add_driver_to_ride(data)
    
    return redirect('/rides')

@app.route('/rides/remove_driver/<int:ride_id>')
def remove_driver(ride_id):
    if 'id' not in session:
        return redirect('/logout')    
    
    data = {
        'id': ride_id,
        'driver_id': session['id']
    }
    
    ride.Ride.remove_driver_from_ride(data)
    
    return redirect('/rides')
