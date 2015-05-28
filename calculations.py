from model import connect_to_db, db, User, Card, Value



def min_payment_plan(name, date, debt, apr, user_id):
	"""Calculates min payment plan for card and returns a dictionary 
		with diff calculations as values

		{Name: [new_debt_list, interest_to_pay_list, min_total_payment_list]} """


	# ----- # Base calculations # ----- #
	interest_per_month = apr/date
	min_payment = interest_per_month + (debt *0.01)
	monthly_payment_suggestion = float(debt) / float((date + 1))
	rounded_monthly_payment_siggestion = round(monthly_payment_suggestion, 2)

	# ----- # Min payment calculations # ----- # 
	new_debt_list=[debt]
	interest_to_pay_list = []
	min_total_payment_list = []
	card = {}

	while debt >0:

		interest_to_pay = round((debt * interest_per_month), 2)
		interest_to_pay_list.append(interest_to_pay)

		min_total_payment = round((min_payment + interest_to_pay) ,2)
		min_total_payment_list.append(min_total_payment)

		new_debt = round((debt + interest_to_pay - min_total_payment), 2)
		new_debt_list.append(new_debt)
		debt = new_debt

	print "*"* 40

	

	minimum = {"Minimum":[new_debt_list, interest_to_pay_list, min_total_payment_list]}
	card[name] = minimum

	return card


def suggested_plan(name, date, debt, apr, card, user_id):
	"""Calculates suggested plan and returns an appended dictionary 
	from previous min_payment_plan function

	{Name: [new_debt_list(min), interest_to_pay_list(min), min_total_payment_list, 
			new_debt_list(suggested), interest_to_pay_list(suggested), monthly_payment_list])}
	"""

	interest_per_month = apr/date
	monthly_payment_suggestion = round(float(debt) / float((date + 1)), 2)
	rounded_monthly_payment_suggestion = round(monthly_payment_suggestion, 2)


	# ----- # Suggested payment calculations # ----- # 

	new_debt_list=[debt]
	interest_to_pay_list = []
	monthly_payment_list = []

	while debt >0:
		interest_to_pay = round((debt * interest_per_month), 2)
		interest_to_pay_list.append(interest_to_pay)

		monthly_payment_list.append(rounded_monthly_payment_suggestion)

		new_debt = round((debt + interest_to_pay - rounded_monthly_payment_suggestion), 2)
		new_debt_list.append(new_debt)
		debt = new_debt


	minimum = card[name].values()
	minimum = minimum[0]

	card[name] = {"Suggested": [new_debt_list, interest_to_pay_list, monthly_payment_list], "Minimum" : minimum}


	dict_within_user = card.values()[0]
	sugg_value_from_dict = dict_within_user["Suggested"]
	min_value_from_dict = dict_within_user["Minimum"]


	return card 


def user_cards(query_results):
	"""Loop over all cards user has entered and return a dictionary of dictionaries. 
	The outer dictionary key = user_id, values = cards
	The inner dictionary key = name of a card, values = min payments, min intr rates,
														min debt decrease, suggested payments,
														suggested intr rates, suggested debt decrease """
	
	user_dict = {}
	card_dict_list = []

	for card in query_results:
		name = card.card_name 
		debt = card.card_debt
		apr = card.card_apr
		#This will turn user inputted apr into percentage
		apr = apr/100
		date = card.card_date
		min_payment = card.min_payment
		user_id = card.user_id
		

		print "Name", name
		print "Debt", debt
		print "APR", apr
		print "Date", date
		print "Min payment", min_payment
		print "User", user_id

		returned_dict = min_payment_plan(name, date, debt, apr, user_id)
		completed_card_dict = suggested_plan(name, date, debt, apr, returned_dict, user_id)
		card_dict_list.append(completed_card_dict)



	user_dict = {user_id : {}}
	
	for card_dict in card_dict_list:
		if user_dict[user_id]:
			user_dict[user_id].append(card_dict)
		else:
			user_dict[user_id] = [card_dict]
	# print "Complete User Dictionary:", user_dict

	return user_dict




#TODO: #
# Make sure to take user_id from session once it's connected #
# for now just manually entering in where user_id is 1. AKA the only user in the database


# TODO: # 
# Additional values that need to be factored in: #
# - min payment plan #

# TODO: # 
# Add in docstring tests to make sure these calculations work all of the time 
# Or don't work when something bad is entered
# Or state assumptions so extra testing is unecessary 
#     such as not testing for negative numbers since html form does not allow
# change the user_id in here and have it pull from session. Might have to do that in server.py


# NOT SURE CALCULATIONS ARE UPDATING PAST TWO CARDS... LOOK INTO THIS....