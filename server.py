"""Ikura Server"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from model import connect_to_db, db, User, Card, Value
from organize_calcs import organization
import json
import csv

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "AcBbCa"
app.jinja_env.undefined = StrictUndefined


from calculations import user_cards

###############################################################
# View Routes #

@app.route('/')
def homepage():
	"""This will bring us to the homepage"""

	
	user_id = session.get("user_id")
	print "This is session's user_id:", user_id

	if user_id:
		user = User.query.get(user_id)
		print "This is the user_id from db:", user
	else:
		user = 0
		print "This is the user_id from db:", user
		flash("""Before you can get started, you'll
				need to login or create a new account.""")

	return render_template('homepage.html', user=user)


@app.route('/card_submission', methods=['GET', 'POST'])
def card_submission():
	"""Allows user to enter in credit card info and then sends 
	   user inuptted info to dashboard"""

	if request.method == 'POST':
		print "This is our request object", request.form
		names = request.form.getlist("card1_name[]")
		print "This is name", names
		print names[0]
		debts = request.form.getlist("card1_debt[]")
		aprs = request.form.getlist("card1_apr[]")
		dates = request.form.getlist("card1_date[]")
		# session.get
		user_id = session.get("user_id")
		min_payment = session.get("min_payment")

		print "Name", names
		print "Debt", debts
		print "APR", aprs
		print "Date", dates
		print "Min Payment", min_payment
		print "This is the session", session
		print "user id", user_id

		for i in range(len(names)):
			print "Name", names[i]
			print "Debt", debts[i]
			print "APR", aprs[i]
			print "Date", dates[i]
			print "Min Payment", min_payment
			print "This is the session", session
			print "user id", user_id


			card = Card.query.filter_by(user_id=user_id).all()

			if card == None:
				flash("In order to generate a payment plan for you we need some information on your current debts. ")
				
			else:
				new_card = Card(card_name = names[i],
							card_debt = debts[i],
							card_apr = aprs[i],
							card_date = dates[i],
							min_payment=min_payment,
							user_id = user_id)
				db.session.add(new_card)   
				db.session.commit()
				flash("Thank you for entering this information! We've calculated your payment plan:")
		return redirect(url_for('dashboard'))
		
	else:
		return render_template('card_submission.html')


@app.route('/dashboard')
def dashboard():
	"""Displays calculations and visualizations for credit cards"""

	
	user_id = session.get("user_id")

	results_of_query = Card.query.filter_by(user_id=user_id).all()
	user_card_dict_py = user_cards(results_of_query)


	all_totals = organization(user_card_dict_py)
	data_points = all_totals[2]
	d3_points_list_json = json.dumps(all_totals[2])



	return render_template('/dashboard.html', query_results=results_of_query, 
											 all_totals=all_totals, 
												 d3_data = d3_points_list_json)

@app.route('/update_dashboard', methods=['POST'])
def update_dashboard():


	user_id = session.get("user_id")
	results_of_query = Card.query.filter_by(user_id=user_id).all()

	print "This is our request object", request.form
	names = request.form.getlist("card1_name[]")
	print "This is name", names
	print names[0]
	debts = request.form.getlist("card1_debt[]")
	aprs = request.form.getlist("card1_apr[]")
	dates = request.form.getlist("card1_date[]")
	user_id = session.get("user_id")
	min_payment = session.get("min_payment")

	# print "Name", names
	# print "Debt", debts
	# print "APR", aprs
	# print "Date", dates
	# print "Min Payment", min_payment
	# print "This is the session", session
	# print "user id", user_id

	

	for index, card in enumerate(results_of_query):

			print "Name", names[index]
			print "Debt", debts[index]
			print "APR", aprs[index]
			print "Date", dates[index]
			print "Min Payment", min_payment
			print "This is the session", session
			print "user id", user_id

			card.card_name = names[index] 
			card.card_debt = debts[index]
			card.card_apr = aprs[index]
			card.card_date = dates[index]
			card.min_payment=min_payment
			card.user_id = user_id

			db.session.commit()
	flash("We've updated your payment plan!")
	

	return redirect('/dashboard')

@app.route('/dashboard_int')
def dashboard_int():
	"""Will calculate sugg payments with a weight on higher interests"""

	user_id = session.get("user_id")

	results_of_query = Card.query.filter_by(user_id=user_id).all()
# Add new function in calculations to replace user_cards
	user_card_dict_py = user_cards_int(results_of_query)

# See if you can still use organization function
	all_totals = organization(user_card_dict_py)
	data_points = all_totals[2]
	d3_points_list_json = json.dumps(all_totals[2])



	return render_template('/dashboard_int.html', query_results=results_of_query, 
											 all_totals=all_totals, 
												 d3_data = d3_points_list_json)
		


@app.route('/d3')
def d3():
 	"""practice for d3"""
 	return render_template('d3_study.html')



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
        return redirect('/login')
    
    del session['user_id']
    print "This is after", session
    flash("You have successfully logged out.")
    
    return redirect('/')

 # http://getbootstrap.com/javascript/#alerts


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

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
#TODO: #
# Make sure to take user_id from session #
# deactivate dashboard for users not logged in
# Need to add option to remove card from database!