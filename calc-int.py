from operator import itemgetter


card_name_1 = "Master"
card_debt_1 = float(1000)
card_apr_1 = float(.1)
card_date_1 = float(12)

card_name_2 = "Visa"
card_debt_2 = float(2000)
card_apr_2 = float(.15)
card_date_2 = float(12)

budget = float(500)

# TODO: need to figure out how to sort a list...... right now this ex is sorted....
# should try sorting by list and by dictionary value. Not sure yet what'll be the best format to have info from DB
card_list = [[card_name_2, card_debt_2, card_apr_2, card_date_2], [card_name_1, card_debt_1, card_apr_1, card_date_1]]
card_list_sorted = sorted(card_list, key=itemgetter(2))
print card_list_sorted


card_sugg_payments = []
card_total_debt = []
for card in card_list:
	sugg_payment = card[1] / (card[3] + 1)
	card_sugg_payments.append(sugg_payment)
	card_debt = card[1]
	card_total_debt.append(card_debt)
# print "list of all minimum sugg payments", card_sugg_payments


sugg_payment_for_all_cards = sum(card_sugg_payments)
# print "allocated for paying sugg payments", sugg_payment_for_all_cards


total_debt = sum(card_total_debt)
# print "This is the total debt", total_debt




# # *******************************
#  # ATTEMPT 3 
# # *******************************

print '*' * 60

while total_debt > 0:
	extra_per_month = budget - sugg_payment_for_all_cards
	print "extra to be used for highest card", extra_per_month

	print '*' * 50
	if card_list_sorted[-1] > 0:
		last_card = card_list_sorted[-1]
		print "What am i", last_card
		debt = last_card[1]
		int_per_month = last_card[2] / last_card[3]
		sugg_payment =last_card[1]/(last_card[3] + 1)
		interest_to_pay_list = []
		card_payment_completed = []

		# while debt >0:
		interest_to_pay = debt * int_per_month
		interest_to_pay_list.append(interest_to_pay)
		new_debt = round((debt + interest_to_pay - sugg_payment - extra_per_month), 2)
		debt = new_debt
		print "debt", debt
		card_payment_completed.append(debt)
		sum_card_payment_completed = sum(card_payment_completed)
		to_be_added = -sum_card_payment_completed
		print "are you negative?", to_be_added
		total_debt = total_debt + to_be_added
		print "Should be decreasing", total_debt

	if card_list_sorted[-2] > 0:
		next_card = card_list_sorted[-1]
		print "What am i", next_card
		debt = next_card[1]
		int_per_month = next_card[2] / next_card[3]
		sugg_payment =next_card[1]/(next_card[3] + 1)
		interest_to_pay_list = []
		card_payment_completed = []

		# while debt >0:
		interest_to_pay = debt * int_per_month
		interest_to_pay_list.append(interest_to_pay)
		new_debt = round((debt + interest_to_pay - sugg_payment - extra_per_month), 2)
		debt = new_debt
		print "debt", debt
		card_payment_completed.append(debt)
		sum_card_payment_completed = sum(card_payment_completed)
		to_be_added = -sum_card_payment_completed
		print "are you negative?", to_be_added
		total_debt = total_debt + to_be_added
		print "Should be decreasing", total_debt










# # *******************************
#  # ATTEMPT 2
# # *******************************


# total_card_payment_completed = []

# while card_list_sorted:
# 	# for card in card_list_sorted:
# 	last_card = card_list_sorted[-1]
# 	print "What am i", last_card
# 	debt = last_card[1]
# 	int_per_month = last_card[2] / last_card[3]
# 	sugg_payment =last_card[1]/(last_card[3] + 1)
# 	interest_to_pay_list = []
# 	card_payment_completed = []

# 	while debt >0:
# 		interest_to_pay = debt * int_per_month
# 		interest_to_pay_list.append(interest_to_pay)
# 		new_debt = round((debt + interest_to_pay - sugg_payment - extra_per_month), 2)
# 		debt = new_debt
# 		print "debt", debt
# 		card_payment_completed.append(debt)



# 	card_list_sorted.pop(-1)


# 	print "watch me decrease", card_list_sorted
# 	print "how is this formatted", card_payment_completed
# 	total_card_payment_completed.append(card_payment_completed)


# 	for card in card_list_sorted:
# 		print "How does this all work?",  card
# 		debt = card[1]
# 		int_per_month = card[2] / card[3]
# 		sugg_payment =card[1]/(card[3] + 1)
# 		print "sugg pay", sugg_payment
# 		interest_to_pay_list = []
# 		card_payment_completed = []
# 		print "how long?", len(total_card_payment_completed[0])

		
# 		while debt >0:
# 			interest_to_pay = debt * int_per_month
# 			interest_to_pay_list.append(interest_to_pay)
# 			for i in range(len(total_card_payment_completed[0])):
# 				new_debt = round((debt + interest_to_pay - sugg_payment), 2)
# 				debt = new_debt
# 				print "debt", debt
# 			new_debt = round((debt + interest_to_pay - sugg_payment - extra_per_month), 2)
# 			debt = new_debt
# 			print "new debt", debt



# print "List of lists for all card payments", total_card_payment_completed










# MUST WORK ON GETTING THIS INTO THE RIGHT FORMAT TO PASS ONTO ORGs?


# *******************************
 # ATTEMPT 1
# *******************************


# highest_int = 0
# for card in card_list:
# 	apr = card[2]
# 	while apr > highest_int:
# 		highest_int = apr


# other_sugg_payments = 0
# for card in card_list:
# 	interest_to_pay_list = []
# 	monthly_payment_list = []
# 	thing = []

# 	if card[2] != highest_int:
# 		print "this is card", card
# 		debt = card[1]
# 		int_per_month = card[2] / card[3]
# 		sugg_payment =card[1]/ (card[3] + 1)
# 		other_sugg_payments += sugg_payment
# 		while debt >0:
# 			interest_to_pay = debt * int_per_month
# 			interest_to_pay_list.append(interest_to_pay)
# 			new_debt = round((debt + interest_to_pay - sugg_payment), 2)
# 			debt = new_debt
# 			print "debt", debt
# 			info = [debt, interest_to_pay, sugg_payment]
# 			thing.append(info)
# 		print "this should be a list of all debt, int and payments for this card",  thing

# 		print "other_sugg_payments now", other_sugg_payments	


# 	if card[2] == highest_int:
# 		print "this is card", card
# 		max_budget = budget - card[1]/(card[3] + 1)
# 		debt = card[1]
# 		int_per_month = card[2] / card[3]
# 		sugg_payment =card[1]/(card[3] + 1)


# 		while debt >0:
# 			interest_to_pay = debt * int_per_month
# 			interest_to_pay_list.append(interest_to_pay)
# 			print "new payment w/ max budget addition", sugg_payment + max_budget - other_sugg_payments
# 			new_debt = round((debt + interest_to_pay - sugg_payment - max_budget + other_sugg_payments), 2)
# 			debt = new_debt
# 			print "debt", debt




	# card[name] = {"Suggested": [new_debt_list, interest_to_pay_list, monthly_payment_list], "Minimum" : minimum}


	# dict_within_user = card.values()[0]
	# sugg_value_from_dict = dict_within_user["Suggested"]
	# min_value_from_dict = dict_within_user["Minimum"]







# ***************************
# Becca's solution/suggestion:
# **************************

# max before for loop. 
# calc
# then allocate remainder to max during all card calculations









