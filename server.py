"""Ikura Server"""

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from model import connect_to_db, db, User, Card, Value
from organize_calcs import organization, organization_int
from calculations import total_sugg_payments, total_sugg_int_amt_paid, total_min_int_paid
import json
import csv
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "AcBbCa"
app.jinja_env.undefined = StrictUndefined


from calculations import user_cards, user_cards_int

###############################################################
# View Routes #

# TODO: FIX BUDGET AND HAVE IT UPDATE ACCORDING TO USER'S SUGG PAY PLAN
BUDGET = 500

# print "what is budget? - global", BUDGET

@app.route('/')
def homepage():
    """This will bring us to the homepage"""

    
    user_id = session.get("user_id")
    # print "This is session's user_id:", user_id

    if user_id:
        user = User.query.get(user_id)
        # print "This is the user_id from db:", user
        user = User.query.filter_by(user_id=user_id).one()
        email = user.email
    else:
        user = 0
        email = "You are not logged in!"
        # print "This is the user_id from db:", user
        flash("""Before you can get started, you'll
                need to login or create a new account.""")

    return render_template('homepage.html', user=user, email=email)


@app.route('/card_submission', methods=['POST'])
def card_submission():
    """Allows user to enter in credit card info and then sends 
       user inuptted info to dashboard"""

    if request.method == 'POST':
        # print "This is our request object", request.form
        names = request.form.getlist("card1_name[]")
        # print "This is name", names
        # print names[0]
        debts = request.form.getlist("card1_debt[]")
        aprs = request.form.getlist("card1_apr[]")
        dates = request.form.getlist("card1_date[]")
        # session.get
        user_id = session.get("user_id")
        min_payment = session.get("min_payment")

        # print "Name", names
        # print "Debt", debts
        # print "APR", aprs
        # print "Date", dates
        # print "Min Payment", min_payment
        # print "This is the session", session
        # print "user id", user_id

        for i in range(len(names)):
            # print "Name", names[i]
            # print "Debt", debts[i]
            # print "APR", aprs[i]
            # print "Date", dates[i]
            # print "Min Payment", min_payment
            # print "This is the session", session
            # print "user id", user_id


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


@app.route('/dashboard')
def dashboard():
    """Displays calculations and visualizations for credit cards"""
    
    #  This checks to make sure user is logged in. If not they are redirected to login page
    if session == {}:
        flash("You are not logged in")
        return redirect('/login')
    else:
        global BUDGET

        BUDGET = BUDGET
        
        user_id = session.get("user_id")
        results_of_query = Card.query.filter_by(user_id=user_id).order_by(-Card.card_apr).all()
        
        
        # This checks to make sure user has entered in card data.
        if not results_of_query:
            flash("Looks like you don't have any cards yet! Start by clicking the 'Let's get Started' button.")
            return redirect('/')


        # If there is data, Ikura will calculate
        else:
            user_card_dict_py = user_cards(results_of_query)

            user = User.query.filter_by(user_id=user_id).one()
            email = user.email
         
            amt_of_cards = len(user_card_dict_py.values()[0])
            list_of_total_sugg_int_amt_paid = []
            
            for item in range(amt_of_cards):
                card = user_card_dict_py.values()[0][item]
                # print "what is card", card
                interest = card.values()[0].values()[0][1]
                print "what is interest", interest
                all_interest_sugg = total_sugg_int_amt_paid(interest)
                print "what is all_interest", all_interest_sugg
                # list_of_total_sugg_int_amt_paid.append(all_interest_sugg)
                
            # print "indiv nums in list", list_of_total_sugg_int_amt_paid
            # list_of_total_sugg_int_amt_paid_sum = sum(list_of_total_sugg_int_amt_paid)
            # print "sugg sum should be smaller", list_of_total_sugg_int_amt_paid_sum


            cards_payment_list = []
            for item in range(amt_of_cards):
                card = user_card_dict_py.values()[0][item]
                payment = card.values()[0].values()[0][2]
                payment = (sum(payment))/(len(payment))
                cards_payment_list.append(payment)            
            total_per_month = sum(cards_payment_list)





        # for calulating my summed int rates....# <- MIN
            # the second index is where the cards are.... [0] is visa
            list_of_total_min_int_amt_paid = []
            for item in range(amt_of_cards):
                card_thing = user_card_dict_py.values()[0][item]

                interest_thing = card_thing.values()[0].values()[1][1]
                all_interest_min = total_min_int_paid(interest_thing)
                # list_of_total_min_int_amt_paid.append(all_interest_thing)

            # list_of_total_min_int_amt_paid_sum = sum(list_of_total_min_int_amt_paid)

            # print "min sum should be larger",  list_of_total_min_int_amt_paid_sum


            print "all_interest_min", all_interest_min
            all_totals = organization(user_card_dict_py)
            

            highcharts_dates = all_totals[3]
            highcharts_dates_str = []
            for date in highcharts_dates:
                date_conv = datetime.strptime(date, "%Y/%m/%d" )
                date_conv = date_conv.strftime("%b-%y")
                highcharts_dates_str.append(date_conv)

            # print "list?", highcharts_dates_str
            # print type(highcharts_dates_str[0])
            # highcharts_dates_json = json.dumps(highcharts_dates)
            # print "JSON", highcharts_dates_json


            highcharts_points = all_totals[4]
            data_points = all_totals[2]
            d3_points_list_json = json.dumps(all_totals[2])
            # print "JSON format!", d3_points_list_json

            
            # print "list of point?", highcharts_points_int_sugg


          
            user_card_dict_py_int = user_cards_int(results_of_query, BUDGET)
            all_totals_int = organization_int(user_card_dict_py_int)
            total_sugg_payment_amt = round(total_sugg_payments(results_of_query), 2)


            highcharts_points_int_sugg = all_totals[5]
            highcharts_points_int_budget = user_card_dict_py_int[2]
            highcharts_points_int_total = []
            highcharts_points_int_total.append(highcharts_points_int_sugg)
            highcharts_points_int_total.append(highcharts_points_int_budget)

            # BUDGET = total_sugg_payment_amt

       
        return render_template('/dashboard.html', query_results=results_of_query, 
                                                all_totals=all_totals, 
                                                d3_data = d3_points_list_json, 
                                                all_totals_int = all_totals_int, 
                                                total_sugg_payment_amt =total_sugg_payment_amt,
                                                list_of_total_sugg_int_amt_paid_sum=all_interest_sugg, 
                                                list_of_total_min_int_amt_paid_sum=all_interest_min, 
                                                email = email, 
                                                cards_payment_list=cards_payment_list, 
                                                total_per_month=total_per_month, 
                                                highcharts_points=highcharts_points, 
                                                highcharts_dates_str=highcharts_dates_str,
                                                highcharts_points_int_total=highcharts_points_int_total, 
                                                BUDGET=BUDGET)
    

@app.route('/update_dashboard', methods=['POST'])
def update_dashboard():
    """This allows users to update the credit card debt info on dashboard page"""

    user_id = session.get("user_id")
    results_of_query = Card.query.filter_by(user_id=user_id).all()

    names = request.form.getlist("card1_name[]")
    debts = request.form.getlist("card1_debt[]")
    aprs = request.form.getlist("card1_apr[]")
    dates = request.form.getlist("card1_date[]")
    user_id = session.get("user_id")
    min_payment = session.get("min_payment")

    for index, card in enumerate(results_of_query):
            # print "what is this index?", index
            # print "names", names

            # print "Name", names[index]
            # print "Debt", debts[index]
            # print "APR", aprs[index]
            # print "Date", dates[index]
            # print "Min Payment", min_payment
            # print "This is the session", session
            # print "user id", user_id

            card.card_name = names[index] 
            card.card_debt = debts[index]
            card.card_apr = aprs[index]
            card.card_date = dates[index]
            card.min_payment=min_payment
            card.user_id = user_id

            db.session.commit()
    flash("We've updated your payment plan!")
    return redirect('/dashboard')


@app.route('/remove_card', methods=['POST'])
def remove_card():
 

    card_id = request.form["remove_card"]
    results_of_query = Card.query.filter_by(card_id=card_id).one()
    results_of_query.user_id = 3
    db.session.commit()


    flash("We've updated your payment plan!")
    return redirect('/dashboard')




@app.route('/update_dashboard_int', methods=['POST'])
def update_dashboard_int():
    """This allows users to update the credit card debt info on dashboard page"""
    
    global BUDGET 
    BUDGET = request.form["budget"]
    BUDGET = int(BUDGET)
    
    return redirect('/dashboard')





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

        # print "Email:", email
        # print "Password:", password
        # print "User:", user

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
        
        # print "Email:", email
        # print "Password:", password
        # print "User:", user
        # print "Session:", session

        if user == None:
            flash( """Hey there! That email and/or password is not in our database. 
            Try again? Or signup!""")
            return redirect('/login')

        if 'user_id' in session:
            print "This is before login", session
            del session['user_id']
            # print "This is after del", session

            session['user_id'] = user.user_id
            # print "This is after login", session
            flash("You are already logged in!") 
        else:
            session['user_id'] = user.user_id
            flash("You have successfully logged in!")
            # print "Session:", session

        # print "*"*30
        # print "This is our current session", session

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


@app.route("/error")
def error():
    raise Exception("Error!")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    PORT = int(os.environ.get("PORT", 5000))

    DEBUG = "NO_DEBUG" not in os.environ
    # DEBUG = True


    
    # app.debug = False
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    # app.run()
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)


    # app.run(debug=DEBUG)


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