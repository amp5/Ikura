from model import connect_to_db, db, User, Card, Value



def min_payment_plan(name, date, debt, apr, user_id):
	"""Calculates min payment plan for card and returns a dictionary 
		with diff calculations as values

		{Name: [new_debt_list, interest_to_pay_list, min_total_payment_list]} """


	# ----- # Base calculations # ----- #
	interest_per_month = apr/date
	# print interest_per_month
	# 0.00833333333333

	min_payment = interest_per_month + (debt *0.01)
	# print min_payment
	# 10.0083333333

	monthly_payment_suggestion = float(debt) / float((date + 1))
	# print monthly_payment_suggestion
	# 76.9230769231

	rounded_monthly_payment_siggestion = round(monthly_payment_suggestion, 2)
	# 76.92

	# ----- # Min payment calculations # ----- # 
	new_debt_list=[debt]
	interest_to_pay_list = []
	min_total_payment_list = []
	cards = {}

	# interest_to_pay = debt * interest_per_month
	# print interest_to_pay
	# 8.33333333333

	# min_total_payment = min_payment + interest_to_pay
	# print min_total_payment
	# 18.3416666667
	 
	# new_debt = debt + interest_to_pay - min_total_payment
	# print new_debt
	# 989.991666667

	while debt >0:

		interest_to_pay = debt * interest_per_month
		interest_to_pay_list.append(interest_to_pay)

		min_total_payment = min_payment + interest_to_pay
		min_total_payment_list.append(min_total_payment)

		new_debt = debt + interest_to_pay - min_total_payment
		new_debt_list.append(new_debt)
		debt = new_debt

	# print "Min Debt decreasing:", new_debt_list
	# print "*"* 20 
	# print "Min Interest decreasing", interest_to_pay_list
	# print "*"* 20 
	# print "Min payments", min_total_payment_list

	# print "*"* 40

	cards[name] = [[new_debt_list, interest_to_pay_list, min_total_payment_list]]

	# print "This is how long debt list is", len(new_debt_list)
	# print '--'*20
	# print "This is dictionary cards", cards 
	return cards


def suggested_plan(name, date, debt, apr, card, user_id):
	"""Calculates suggested plan and returns an appended dictionary 
	from previous min_payment_plan function

	{Name: [new_debt_list(min), interest_to_pay_list(min), min_total_payment_list, 
			new_debt_list(suggested), interest_to_pay_list(suggested), monthly_payment_list])}
	"""
	# print "These are my card", card


	# print "How many card are there", len(card)
	# print "THIS IS MY card FROM THE PAST FUNCTION!!!!!!!!!!!!!!!!!!!!!!!!", card
	interest_per_month = apr/date
	# print "interest per month:", interest_per_month
	monthly_payment_suggestion = float(debt) / float((date + 1))
	rounded_monthly_payment_suggestion = round(monthly_payment_suggestion, 2)
	# print "rounded suggestion:", rounded_monthly_payment_suggestion
	

	# ----- # Suggested payment calculations # ----- # 

	new_debt_list=[debt]
	interest_to_pay_list = []
	monthly_payment_list = []

	while debt >0:
		interest_to_pay = debt * interest_per_month
		interest_to_pay_list.append(interest_to_pay)
		# print "interest list:", interest_to_pay_list

		# monthly_payment = min_payment + interest_to_pay
		monthly_payment_list.append(rounded_monthly_payment_suggestion)
		# print "monthly payment list:", monthly_payment_list

		new_debt = debt + interest_to_pay - rounded_monthly_payment_suggestion
		new_debt_list.append(new_debt)
		debt = new_debt

	# print "What is in here", monthly_payment_list

	# print "Suggested Debt decreasing:", new_debt_list
	# print "*"* 20 
	# print "Suggested Interest decreasing", interest_to_pay_list
	# print "*"* 20 
	# print "Suggested payments", monthly_payment_list



	# print "Taking this from card - min len ", data_points_len

	card[name].append([new_debt_list, interest_to_pay_list, monthly_payment_list])
	# print '--'*20
	# print "This is dictionary card", card

	return card 


def user_cards(query_results):
	"""Loop over all cards user has entered and return a dictionary of dictionaries. 
	The outer dictionary key = user_id, values = cards
	The inner dictionary key = name of a card, values = min payments, min intr rates,
														min debt decrease, suggested payments,
														suggested intr rates, suggested debt decrease """



	#TODO: #
	# Make sure to take user_id from session once it's connected #
	# for now just manually entering in where user_id is 1. AKA the only user in the database

	
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

	print "This is card list", card_dict_list

	user_dict = {user_id : {}}
	
	for card_dict in card_dict_list:
		if user_dict[user_id]:
			user_dict[user_id].append(card_dict)
		else:
			user_dict[user_id] = [card_dict]
	# print "Complete User Dictionary:", user_dict

	return user_dict


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