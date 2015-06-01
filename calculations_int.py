class Card(object):
	name = None
	debt = None
	apr = None
	date = None

	def __init__(self, name, debt, apr, date):
		"""initalizing every instance so all cards have a name, debt, 
			apr and time alottment to pay off debt attributes"""
		self.name = name
		self.debt = debt
		self.apr = apr
		self.date = date

	def int_per_month(self):
		"""interest rate divided by the number of months user entered 
		in until they want to be debt free"""
		return self.apr / self.date

	def sugg_payment(self):
		"""calculates suggested payment for user so that they can be 
		debt free by the date they inputted (# of months) """
		return self.debt / (self.date + 1)


card1 = Card("Mastercard", 1000, .10, 12)
card2 = Card("Visa", 2000, .15, 12)
# card3 = Card("Discover", 10, 0, 12)

#  need to figure out how to make this scalable and have multiple card current debt amounts...

num_of_cards = [card1, card2]
# make sure in html. budget is over {{total amount of sugg payments}}
budget = 500
payment_info_list = []


# how to do this part?
# for each month:
# have a poblem in my calcs where it will get 
	#funky if all the dates aren't averaged

date_list = []
for card in num_of_cards:
	date_list.append(card.date)

avg_num_of_months = sum(date_list) / len(date_list)
print "is this avg?", avg_num_of_months


# This should calculate the monthly payments for each card. 
# Will also add in the extra budget amount too for 
	# higest int card until paid off
for month in range(avg_num_of_months):
	print "#" * 60
	sugg_payment_total = []
	

	# calculating extra budget 
	for card in num_of_cards:       	
		sugg_payment = card.sugg_payment()
		sugg_payment_total.append(sugg_payment)
	
	
	sugg_payment_total = sum(sugg_payment_total)
	extra_budget =  budget - sugg_payment_total
	print "what is extra budget:",  extra_budget
	print "*"* 60

	#focused on the number of cards user has entered and making sugg payments
	for card in num_of_cards:
		print "Month:", month
		print "I am card", card.name   				
		print "before", card.debt  
		print "suggested payment", card.sugg_payment()  
		if (card.debt - card.sugg_payment()) <= 0:
		  		card.debt = 0
		elif (card.debt - card.sugg_payment()) > 0:
			card.debt = card.debt - card.sugg_payment()
			print "after", card.debt
		else:
			print "This shouldn't be here!"
		card.debt = card.debt
		print "what are we now???????", card.debt
	
		print "*"* 30


	# focused on the amount of money left in extra budget
	# Rught now this is wrong. 
	# I want it to only grab the highest int rate card
	for card in num_of_cards:
		print "Month:", month
		print "I am card", card.name 
		# if card.apr = highest:  
		if card.debt > 0:
			# if apr rate is the highest then:
			if card.debt - extra_budget < 0:
				card.debt = 0
				print "after decreasing card debt is neg or zero", card.debt
			elif card.debt <=0:
				print "after decreasing from extra budget - 000000:", card.debt
			else:	
				card.debt = card.debt - extra_budget
				print "after decreasing from extra budget", card.debt
		# else:  ## aka: this card doesn't have the higest rate
		# 	pass

		# look for highest int rate





















# for pet in [
#     Pet("Santa's Little Helper", "dog"),
#     Cat("Snowball II")
# ]:

#      pet.speak()