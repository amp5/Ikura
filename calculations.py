"""This will be where I do the credit card debt calculations. """


# ***************************************************
# Round 1
# ***************************************************

def min_payment_plan(time_to_pay_off, debt, apr):

	# ----- # Base calculations # ----- #
	interest_per_month = apr/time_to_pay_off
	# print interest_per_month
	# 0.00833333333333

	min_payment = interest_per_month + (debt *0.01)
	# print min_payment
	# 10.0083333333

	monthly_payment_suggestion = float(debt) / float((time_to_pay_off + 1))
	# print monthly_payment_suggestion
	# 76.9230769231

	rounded_monthly_payment_siggestion = round(monthly_payment_suggestion, 2)
	# 76.92

	# ----- # Min payment calculations # ----- # 
	new_debt_list=[debt]
	interest_to_pay_list = []
	min_total_payment_list = []

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

	print "Min Debt decreasing:", new_debt_list
	print "*"* 20 
	print "Min Interest decreasing", interest_to_pay_list
	print "*"* 20 
	print "Min payments", min_total_payment_list

	print "*"* 40

def suggested_plan(time_to_pay_off, debt, apr):
	interest_per_month = apr/time_to_pay_off
	monthly_payment_suggestion = float(debt) / float((time_to_pay_off + 1))
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

	print "Suggested Debt decreasing:", new_debt_list
	print "*"* 20 
	print "Suggested Interest decreasing", interest_to_pay_list
	print "*"* 20 
	print "Suggested payments", monthly_payment_list


#  These values will be taken from user input. #
# # Scenario 1
# time_to_pay_off = 12
# debt = 1000
# apr = 0.1


# # Scenario 2
# time_to_pay_off = 12
# debt = 2000
# apr = 0.2

# # Scenario 3
# time_to_pay_off = 12
# debt = 5000
# apr = 0.21

# Scenario 4
time_to_pay_off = 24
debt = 3000
apr = 0.2

# TODO: # 
# Additional values that need to be factored in: #
# - min payment plan #


min_payment_plan(time_to_pay_off, debt, apr)
suggested_plan(time_to_pay_off, debt, apr)


# ***************************************************
# Round 2
# ***************************************************






# TODO: # 
# Add in docstring tests to make sure these calculations work all of the time 
# Or don't work when something bad is entered
# Or state assumptions so extra testing is unecessary 
#     such as not testing for negative numbers since html form does not allow
