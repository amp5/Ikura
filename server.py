"""Ikura Server"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from model import connect_to_db, db, User, Card, Value

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "AcBbCa"
app.jinja_env.undefined = StrictUndefined


###############################################################
# View Routes #

@app.route('/')
def homepage():
	"""This will bring us to the homepage"""

	return render_template('homepage.html')


@app.route('/card_submission')
def card_submission():
	"""Allows user to enter in credit card info"""

	return render_template('card_submission.html')



# ******************************
# Help. Method not allowed? It worked yesterday. What am I not seeing?
# ******************************



@app.route('/card_submission_sent', methods=['POST'])
def card_submission_sent():
	"""Sends user inputted information to calculations"""

	name_1 = request.form["card1_name"]
	debt_1 = request.form["card1_debt"]
	apr_1 = request.form["card1_apr"]
	date_1 = request.form["card1_date"]
	user_id = session.get("user_id")

	print "Name", name_1
	print "Debt", debt_1
	print "APR", apr_1
	print "Date", date_1
	print "This is the session", session
	print "user id", user_id

	card = Card.query.filter_by(user_id=user_id).all()

	if card == None:
		flash("In order to generate a payment plan for you we need some information on your current debts. ")
		
	else:
		new_card = Card(card_name = name_1,
					card_debt = debt_1,
					card_apr = apr_1,
					card_date = date_1, 
					user_id = user_id)
		db.session.add(new_card)   
		db.session.commit()
		flash("Thank you for entering this information! We've calculated your payment plan:")

	return render_template('dashboard.html', 
							card_name=name_1, 
							card_debt=debt_1,
							card_apr=apr_1,
							card_date=date_1)


@app.route('/dashboard')
def dashboard():
	"""Displays calculations and visualizations for credit cards"""

	return render_template('dashboard.html')



###############################################################
# Signup & Login #

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	"""Route should direct user to sign up page first. Then route should take inputs
	and add user into database"""
	
	if request.method == 'POST':
		email = request.form["email_input"]
		password = request.form["password_input"]
		user = User.query.filter_by(email=email).first()

		print "Email:", email
		print "Password:", password
		print "User:", user

		if user != None:
			flash("Sorry, that email is taken. Did you mean to log in instead?")

		else:
			new_user = User(email = email, password = password)
			db.session.add(new_user)   
			db.session.commit()
			flash("Thank you for signing up for Ikura!")

		return render_template('login.html', email= email, password=password)
	else: 
		return render_template('subscribe.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Takes user to login in page and logs a user into the website"""


	if request.method == 'POST':
		email = request.form["email_input"]
		password = request.form["password_input"]
		user = User.query.filter_by(email=email, password=password).first()
		
		print "Email:", email
		print "Password:", password
		print "User:", user
		print "Session:", session

		if user == None:
			flash( """Hey there! That email and/or password is not in our database. 
			Try again? Or signup!""")
			return redirect('/login')

		if 'user_id' in session:
			print "This is before login", session
			del session['user_id']
			print "This is after del", session

			session['user_id'] = user.user_id
			print "This is after login", session
			flash("You are already logged in!") 
		else:
			session['user_id'] = user.user_id
			flash("You have successfully logged in!")
			print "Session:", session

		print "*"*30
		print "This is our current session", session

		return redirect('/')
	else:
		return render_template('login.html')


@app.route('/logout')
def logout():
    """Logs a user out of the site."""
    
    print "This is before logout", session
    if session == {}:
        flash("You are not logged in")
        return redirect('/to_login')
    
    del session['user_id']
    print "This is after", session
    flash("You have successfully logged out.")
    
    return redirect('/')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()


#***************** # Notes # ***********************

# interactive debugger for Flask must never be used on production machines!!

# TODO:
# Need to combine subscribe and login to same @app.route. Should be able to
# have jinja display different messages on same page.
# Want to make this more succinct.