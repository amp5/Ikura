from model import connect_to_db, db, User, Card, Value



def user_cards(query):
	"""Loop over al cards user has entered and return a dictionary of dictionaries. 
	The outer dictionary key = user_id, values = cards
	The inner dictionary key = name of a card, values = min payments, min intr rates,
														min debt decrease, suggested payments,
														suggested intr rates, suggested debt decrease """


	# need to query database to get all cards where user_id is in session
	# object filled with cards
	# from object must need ot pull out all things we want

	#TODO: #
	# Make sure to take user_id from session once it's connected #
	# for now just manually entering in where user_id is 1. AKA the only user in the database

	print "This is the query pulled in from dashboard. User inputted.", query

	user_dict = {}
	
	for card in query:
		name = card.card_name 
		debt = card.card_debt
		apr = card.card_apr
		date = card.card_date
		min_payment = card.min_payment
		user_id = card.user_id

		print "Name", name
		print "Debt", debt
		print "APR", apr
		print "Date", date
		print "Min payment", min_payment
		print "User", user_id
		




		def min_payment_plan(name, date, debt, apr, user_id):
			"""Calculates min oayment plan for card and returns a dictionary 
				with diff calculations as values"""

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

			cards[name] = [new_debt_list, interest_to_pay_list, min_total_payment]
			# print '--'*20
			# print "This is dictionary cards", cards 
			# print cards
			return cards

		def suggested_plan(name, date, debt, apr, cards, user_id):
			"""Calculates suggested plan and returns an appended dictionary 
			from previous min_payment_plan functionw"""

			cards = cards
			# print "THIS IS MY CARDS FROM THE PAST FUNCTION!!!!!!!!!!!!!!!!!!!!!!!!", cards
			interest_per_month = apr/date
			monthly_payment_suggestion = float(debt) / float((date + 1))
			rounded_monthly_payment_siggestion = round(monthly_payment_suggestion, 2)

			# ----- # Suggested payment calculations # ----- # 

			new_debt_list=[debt]
			interest_to_pay_list = []
			monthly_payment_list = []

			while debt >0:

				interest_to_pay = debt * interest_per_month
				interest_to_pay_list.append(interest_to_pay)

				# monthly_payment = min_payment + interest_to_pay
				monthly_payment_list.append(monthly_payment_suggestion)

				new_debt = debt + interest_to_pay - monthly_payment_suggestion
				new_debt_list.append(new_debt)
				debt = new_debt

			# print "Suggested Debt decreasing:", new_debt_list
			# print "*"* 20 
			# print "Suggested Interest decreasing", interest_to_pay_list
			# print "*"* 20 
			# print "Suggested payments", monthly_payment_list

			cards[name].append([new_debt_list, interest_to_pay_list, monthly_payment_list])
			print '--'*20
			print "This is dictionary cards", cards
			return cards 

		def main():

			#  These values will be taken from user input. #
			# # Scenario 1
			# name = "Visa 145"
			# date = 12
			# debt = 1000
			# apr = 0.1


			# # Scenario 2
			# name = "Visa 14335"
			# date = 12
			# debt = 2000
			# apr = 0.2

			# # Scenario 3
			# name = "Visa 399
			# date = 12
			# debt = 5000
			# apr = 0.21

			# # Scenario 4
			# name = "Mastercard 1"
			# # make these into lists of things and we will iterate over them
			# date = 24
			# debt = 3000
			# apr = 0.2


			returned_dict = min_payment_plan(name, date, debt, apr)
			# print returned_dict
		# 	completed_card_dict = suggested_plan(name, date, debt, apr, returned_dict)

		# 	print "*" * 100
		# 	print "This should be the whole dict", completed_card_dict
		 
		### do I need to call main() or call each function.... ####

		returned_dict = min_payment_plan(name, date, debt, apr, user_id)
		completed_card_dict = suggested_plan(name, date, debt, apr, returned_dict, user_id)
		print "This should be the whole dict", completed_card_dict

		user_dict['user_id'] = [cards]



# user_cards()



# Tried doing this like in model and still getting 
# "application not registered on db instance and no application bound to current context" error
# if __name__ == "__main__":
#     # As a convenience, if we run this module interactively, it will leave
#     # you in a state of being able to work with the database directly.

#     from server import app
#     connect_to_db(app)
#     with app.app_context():
#     	print "Connected to DB."


 





# TODO: # 
# Additional values that need to be factored in: #
# - min payment plan #

# TODO: # 
# Add in docstring tests to make sure these calculations work all of the time 
# Or don't work when something bad is entered
# Or state assumptions so extra testing is unecessary 
#     such as not testing for negative numbers since html form does not allow
