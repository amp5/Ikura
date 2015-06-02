from model import connect_to_db, db, User, Card, Value


def min_payment_plan(name, date, debt, apr, user_id):
	"""Calculates min payment plan for card and returns a dictionary 
		with diff calculations as values

		{Name: [new_debt_list, interest_to_pay_list, min_total_payment_list]} """

	# ----- # Base calculations # ----- #
	interest_per_month = apr/date
	min_payment = interest_per_month + (debt *0.01)

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

	print "date right?", date
	interest_per_month = apr/date
	print "int rate", interest_per_month
	monthly_payment_suggestion = float(debt) / float((date + 1))
	print "This should be the right number!", monthly_payment_suggestion
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

	# print "this is my card!", card

	return card 

# *************************************
# Attemptng to fix this problem.
# 1. figure out in excel what numbers you need to see
# 2. Get your function to print those numbers
# 3. save it in a list
# 4. save it in a dictionary
# *************************************


def calculations_int(query_results):

	# make sure in html. budget is over {{total amount of sugg payments}}
	budget = 500  # USER MUST ENTER THIS IN!
	payment_info_list = []

	num_of_cards = []
	for card in query_results:
		name = card.card_name 
		debt = card.card_debt
		apr = card.card_apr
		#This will turn user inputted apr into percentage
		apr = apr/100
		date = card.card_date
		min_payment = card.min_payment
		user_id = card.user_id
		sugg_payment = card.card_sugg
		card.card_sugg = debt / (date + 1)
		sugg_payment = card.card_sugg
		num_of_cards.append(card)

	
		# KNOWN BUG - if the card dates are not the same, the calculations will not factor this in
		# Thus I'm getting the average of the months for now. 
		# TODO: fix this

	# print "this is num of cards", num_of_cards

	date_list = []
	for card in num_of_cards:
		date_list.append(card.card_date)

	avg_num_of_months = sum(date_list) / len(date_list)
	

	# This should calculate the monthly payments for each card. 
	# Will also add in the extra budget amount too for 
		# higest int card until paid off
	num_of_cards_copy = list(num_of_cards)
	highest_apr = num_of_cards_copy.pop(0)

	card_info = {}
	decr_debt = []
	payment_per_month = []

	for month in range(avg_num_of_months):
		# print "#" * 60
		sugg_payment_total = []
		
		# calculating extra budget 
		for card in num_of_cards:       	
			sugg_payment = card.card_sugg
			sugg_payment_total.append(sugg_payment)
			card_info[card.card_name] = {}
		sugg_payment_total = sum(sugg_payment_total)
		extra_budget =  budget - sugg_payment_total

		print "extra budget - I should change after month 7", extra_budget # but I'm not....
		# KNOWN BUG: problem after going through the first high int rate card, not redoing the extra budget part

		#focused on the number of cards user has entered and making sugg payments
		# print "Month:", month
		for card in  num_of_cards_copy:
			if card == highest_apr:
				# print "extra budget", extra_budget, " for ", card.card_name, " with debt ", card.card_debt
				if card.card_debt > 0:
					if card.card_debt - extra_budget <= 0:
						card.card_debt = 0
						decr_debt.append(card.card_debt)
						payment_per_month.append(extra_budget)
						# extra_budget = extra_budget + card.card_sugg
						if num_of_cards_copy:
							highest_apr = num_of_cards_copy.pop(0)
						# print "zero debt", card.card_debt
					else:	
						card.card_debt = card.card_debt - extra_budget
						# print "decreasing debt", card.card_debt
						decr_debt.append(card.card_debt)
						payment_per_month.append(extra_budget)
				else: 
					# some cards are giving me this print statement. why...?
					payment_per_month.append(0)
					# print "Error!"
			else:
				# print "Non highest apr card", card.card_name, " debt ", card.card_debt, " with sugg payment: ",  card.card_sugg 
				payment_result = card.card_debt - card.card_sugg
				if card.card_debt > 0:
					if payment_result <= 0:
					  	card.card_debt = 0
					  	decr_debt.append(card.card_debt)
					  	payment_per_month.append(card.card_sugg)	
					else:
						card.card_debt = card.card_debt - card.card_sugg
						decr_debt.append(card.card_debt)
						payment_per_month.append(card.card_sugg)
						# print "after", card.card_debt
				# else:
				# 	payment_per_month.append(0)	
				# 	print "This shouldn't be here!"
				
				# print "what are we now???????", card.card_debt

	print "This is my list of decr debt", decr_debt
	print len(decr_debt)
	print "This is my sugg payments/extrabudget amount", payment_per_month
	print len(payment_per_month)

	# TODO:
	# NEED TO CREATE A LIST FOR EVERY MONTH THE DEBT DECREASING, PAYMENT AMOUNT
		# - either do by month... <- a set of points and the index them and transfer them into keys below...
		# or by card....

	# print "This is my card dict", card_info
		# here I will assign the lists of info as the value to the 
		# associated key written above on line 142



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
		sugg_payment = card.card_sugg
		

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


def user_cards_int(results_of_query):
	"""Loop over all cards user has entered and return a dictionary of dictionaries. 
	The outer dictionary key = user_id, values = cards
	The inner dictionary key = name of a card, values = min payments, min intr rates,
														min debt decrease, suggested payments,
														suggested intr rates, suggested debt decrease """
	

	user_dict = {}
	card_dict_list = []

	# calculating cards based on highest interest rate
	int_calcs = calculations_int(results_of_query)

	return "stuff"

	# user_dict = {user_id : {}}
	# for card_dict in card_dict_list:
	# 	if user_dict[user_id]:
	# 		user_dict[user_id].append(card_dict)
	# 	else:
	# 		user_dict[user_id] = [card_dict]
	# # print "Complete User Dictionary:", user_dict
	# return user_dict



# TODO: # 
# Add in docstring tests to make sure these calculations work all of the time 
# Or don't work when something bad is entered
# Or state assumptions so extra testing is unecessary 
#     such as not testing for negative numbers since html form does not allow
# change the user_id in here and have it pull from session. Might have to do that in server.py

