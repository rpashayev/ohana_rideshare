from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import message

@app.route('/messages/send', methods=['POST'])
def send_msg():
    if not message.Message.validate_message(request.form):
        return redirect(f'/rides/view/{request.form["ride_id"]}')
    
    data = {
        'content': request.form['content'],
        'sender_id': session['id'],
        'ride_id': request.form['ride_id']
    }
    message.Message.send_message(data)
    
    return redirect(f'/rides/view/{request.form["ride_id"]}')
