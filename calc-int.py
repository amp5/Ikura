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
card_list = [[card_name_1, card_debt_1, card_apr_1, card_date_1], [card_name_2, card_debt_2, card_apr_2, card_date_2]]
print "card list", card_list


card_sugg_payments = []
for card in card_list:
	sugg_payment = card[1] / (card[3] + 1)
	card_sugg_payments.append(sugg_payment)
# print "list of all minimum sugg payments", card_sugg_payments
sugg_payment_for_all_cards = sum(card_sugg_payments)


print "allocated for paying sugg payments", sugg_payment_for_all_cards


extra_per_month = budget - sugg_payment_for_all_cards
print "extra to be used for highest card", extra_per_month







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









