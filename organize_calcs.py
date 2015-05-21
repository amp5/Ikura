from calculations import min_payment_plan, suggested_plan, user_cards
from model import connect_to_db, db, User, Card, Value

# Keeping this here for now so I can play with file to make sure organizaiton works.
# Will eventually send this stuff to server.py so that this stuff shows on dashboard.html
from server import app
connect_to_db(app)


results_of_query = Card.query.filter_by(user_id=1).all()

user_card_dict_py = user_cards(results_of_query)

print type(user_card_dict_py)
print "Values:", user_card_dict_py.values()

values = user_card_dict_py.values()
print "All of values", type(values)
print "First index within values", type(values[0])
print "First index within idex within values", type(values[0][0])

i = 0
# Fix names in for loop!!!
# When I typed "for i in values" received following error:
# TypeError: list indices must be integers, not tuple
for card in values[0]:
	print "*"*100
	print "This is i", i
	card = values[0][i]
	print "This is the dictionary of my card:", card

	card_values = card.values()
	print "These are the values of my card:", card_values

	# Minimum Payment Data #
	min_info = card_values[0][0]
	print "This is all of the info related to my card's minimum payment:", min_info

	min_debt = min_info[0]
	print "This is minimum debt on my card as it decreases:", min_debt

	min_int = min_info[1]
	print "This is the minimum interest accruing for each payment:", min_int

	min_payment = min_info[2]
	print "This is the minimum payments for card until debt is gone:", min_payment

	# Suggested Payment Data # 
	sugg_info = card_values[0][1]
	print "This is all of the info related to my card's suggested payment", sugg_info

	sugg_debt = sugg_info[0]
	print "This is suggested debt on my card as it decreases:", sugg_debt

	sugg_int = sugg_info[1]
	print "This is the suggested interest accruing for each payment:", sugg_int

	sugg_payment = sugg_info[2]
	print "This is the suggested payments for card until debt is gone:", sugg_payment
	i = i + 1
	print "This is new i", i 

# thing = values[0][1]
# print thing


