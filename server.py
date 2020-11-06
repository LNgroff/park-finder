"""Server for park finder app."""

from flask import (Flask, render_template, request, flash, session,
                    redirect)
from model import connect_to_db
import crud
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def get_homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/parks')
def show_all_parks():
    """View all parks."""

    parks = crud.return_all_parks()

    return render_template('all_parks.html', parks=parks)

@app.route('/parks/<park_id>')
def park_details(park_id):
    """Show details on specific parks"""

    park = crud.get_park_by_id(park_id)

    return render_template('park_details.html', park=park)

@app.route('/all-users')
def show_all_users():
    """View all users."""

    users = crud.return_all_users()

    return render_template('all_users.html', users=users)

@app.route('/all-users/<user_id>')
def user_details(user_id):
    """Show details on specific user"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

@app.route('/users', methods = ['POST'] )
def register_user():
    """Get inputs from form"""

    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    user = crud.get_user_by_email(email)


    if user == None:
        crud.create_user(email, password)
        flash('Account created! You can now log in.')
    else:    
        flash('Email already exists. Try again.')

    return redirect('/')

@app.route('/login', methods = ['POST'])
def log_in():
    """Gets input from log-in and checks to see if emails and passwords
    match."""

    # fix so the user can enter username OR email
    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if email == user.email and password == user.password:
        session['user'] = user.user_id
        flash('Logged in!')
    else:
        flash('Email and password do not match.')
    
    return redirect('/')
    


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)


"""
TODO:
- fix log-in so user can enter usernmae OR email. (retcon on homepage.html)
- Add server route for parks by state


"""