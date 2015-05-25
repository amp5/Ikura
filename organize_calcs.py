from model import connect_to_db, db, User, Card, Value
from pandas import Series, DataFrame
import pandas as pd
from datetime import datetime
# import json

# Keeping this here for now so I can play with file to make sure organizaiton works.
# Will eventually send this stuff to server.py so that this stuff shows on dashboard.html
# from server import app
# connect_to_db(app)

def organization(dictionary):

	# print type(user_card_dict_py)
	# print "Values:", user_card_dict_py.values()
	# results_of_query = Card.query.filter_by(user_id=1).all()
	# user_card_dict_py = user_cards(results_of_query)

	# This converts my Python dictionary or dictionaries into JSON. 
	# Will be used to pass onto D3
	# user_card_dict = json.dumps(user_card_dict_py)
	# print type(user_card_dict)


	user_card_dict_py = dictionary
	values = user_card_dict_py.values()
	# print "All of values", type(values)
	# print "First index within values", type(values[0])
	# print "First index within idex within values", type(values[0][0])

	total_min_debt = []
	total_min_int = []
	total_min_payment = []

	total_sugg_debt = []
	total_sugg_int = []
	total_sugg_payment = []

	for i in range(len(values[0])):
		print "*" * 100
		card = values[0][i]
		# print "This is the dictionary of my card:", card

		card_values = card.values()
		# print "These are the values of my card:", card_values


	# *************************************
		# Minimum Payment Data #
	# *************************************

		min_info = card_values[0][0]
		# print "This is all of the info related to my card's minimum payment:", min_info

		min_debt = min_info[0]
		# print "This is minimum debt on my card as it decreases:", min_debt
		total_min_debt.append(min_debt)
		# Should be a list of lists... YES
		# print "This is my total minimum debt decreasing.", total_min_debt
		# print "Type", type(total_min_debt)

		min_int = min_info[1]
		# print "This is the minimum interest accruing for each payment:", min_int
		total_min_int.append(min_int)
		# print "This is my total minimum interest", total_min_int
		# print "Type", type(total_min_int)

		min_payment = min_info[2]
		# print "This is the minimum payments for card until debt is gone:", min_payment
		total_min_payment.append(min_payment)
		# print "Total min payment", total_min_payment

	# *************************************
		# Suggested Payment Data # 
	# *************************************
		sugg_info = card_values[0][1]
		# print "This is all of the info related to my card's suggested payment", sugg_info

		sugg_debt = sugg_info[0]
		# print "This is suggested debt on my card as it decreases:", sugg_debt
		total_sugg_debt.append(sugg_debt)
		# print "Total suggested debt decreasing", total_sugg_debt

		sugg_int = sugg_info[1]
		# print "This is the suggested interest accruing for each payment:", sugg_int
		total_sugg_int.append(sugg_int)
		# print "sugg int", total_sugg_int

		sugg_payment = sugg_info[2]
		# print "This is the suggested payments for card until debt is gone:", sugg_payment
		total_sugg_payment.append(sugg_payment)
		# print "sugg payment", total_sugg_payment

	total_min_debt = [x + y for x, y in zip(total_min_debt[0], total_min_debt[1])]
	rounded_total_min_debt = [round(x, 2) for x in total_min_debt]

	
	total_min_int = [x + y for x, y in zip(total_min_int[0], total_min_int[1])]
	rounded_total_min_int = [round(x, 2) for x in total_min_int]

	
	total_min_payment = [x + y for x, y in zip(total_min_payment[0], total_min_payment[1])]
	rounded_total_min_payment = [round(x, 2) for x in total_min_payment]

	
	total_sugg_debt = [x + y for x, y in zip(total_sugg_debt[0], total_sugg_debt[1])]
	rounded_total_sugg_debt = [round(x, 2) for x in total_sugg_debt]

	
	total_sugg_int = [x + y for x, y in zip(total_sugg_int[0], total_sugg_int[1])]
	rounded_total_sugg_int = [round(x, 2) for x in total_sugg_int]

	
	total_sugg_payment = [x + y for x, y in zip(total_sugg_payment[0], total_sugg_payment[1])]
	rounded_total_sugg_payment = [round(x, 2) for x in total_sugg_payment]


	# rounded_all_totals = [float(int(x)) for x in all_totals]
	# print "total sugg payment", total_sugg_payment

	# print "total min debt:", total_min_debt
	# print '*' * 30
	# print "total min int:",  total_min_int
	# print '*' * 30
	# print "total min payment", total_min_payment
	# print '*' * 30
	# print "total sugg debt:", total_sugg_debt
	# print '*' * 30
	# print "total sugg int", total_sugg_int
	# print '*' * 30
	# print "total sugg payment", total_sugg_payment


	now = datetime.now()
	dt_min_month = pd.date_range(datetime.strftime(now, '%Y-%m-%d'), periods=len(rounded_total_min_debt), freq='M')
	dt_sugg_month = pd.date_range(datetime.strftime(now, '%Y-%m-%d'), periods=len(rounded_total_sugg_debt), freq='M')

	# How to get month and year to display on table?
	total_min = zip(*[dt_min_month, rounded_total_min_debt, rounded_total_min_int, rounded_total_min_payment])
	total_sugg = zip(*[dt_sugg_month, rounded_total_sugg_debt, rounded_total_sugg_int, rounded_total_sugg_payment])


	# all_totals = [total_min, total_sugg]
	
	df_min = pd.DataFrame(data = total_min, columns=['Month', 'Debt', 'Interest', 'Payments'])
	df_sugg = pd.DataFrame(data = total_sugg, columns=['Month', 'Debt', 'Interest', 'Payments'])

	#**************# A debugger tool from Rachael: #**************#
	# import pdb; pdb.set_trace()

	# print "This is my sugg data frame", df_sugg


	# ****************** D3 ********************************************
	# For D3 graph I want points for (debt_decr, time)
	# min_d3_points = []
	min_point = zip(*[dt_min_month.date, rounded_total_min_debt])
	# print "This is zipped point", min_point

	data_point_list = []

	# min_point_list = []
	for i in range(len(min_point)):
		point_dict = {"type":"Minimum Payment", "date":str(min_point[i][0]), "amount":min_point[i][1]}
		# min_point_list.append(point_dict)
		data_point_list.append(point_dict)

	# min_point_dict = {"Minimum Payment": min_point_list}
	# print "dict", min_point_dict




	sugg_point = zip(*[dt_sugg_month.date, rounded_total_sugg_debt])
	# sugg_point_list = []
	for i in range(len(sugg_point)):
		point_dict = {"type":"Suggested Payment", "date":str(sugg_point[i][0]), "amount": sugg_point[i][1]}
		# point = [str(sugg_point[i][0]), sugg_point[i][1]]
		# sugg_point_list.append(point_dict)
		data_point_list.append(point_dict)

	# print "This is mini dictionary of points for each one", point_dict

	# sugg_point_dict = {"Suggested Payment": sugg_point_list}
	# print "dict of sugg", sugg_point_dict

	data_point_dict = {"User Points": data_point_list}
	# print "This is my dictoinary of all of my data points", data_point_dict





	# d3_points_list = []
	# print "list of dicts", d3_points_list
	



	# min_d3_points_json = df_min_point.to_json()
	# print min_d3_points_json


	# min_d3_points.append(point)
	# print "These are my points for min_d3_points", min_d3_points

	# min_d3_points_json = min_d3_points.to_json()
	# print min_d3_points_json

	# sugg_d3_points = []
	# point = zip(*[dt_sugg_month, rounded_total_sugg_debt])
	# sugg_d3_points.append(point)
	# print "These are my points for sugg_d3_points", sugg_d3_points

	# total_d3_points = [min_d3_points, sugg_d3_points]








	# d3_points = all_totals[2]
	# json_d3_points = d3_points.to_json()
	# print "JSON:", json_d3_points
	# print type(json_d3_points)

	# # These lines return a JSON of my data frames.
	# df_sugg_json = df_sugg.to_json()
	# print df_sugg_json
	# print type(df_sugg_json)






# TODO:
# create points for use in multiple d3 graphs? use toggle feature?: 
# 	(debt_decr, time)
# 	(intr_decr, time)
# 	(payment_decr, time)		



	df_total = [df_min, df_sugg, data_point_dict]
	# print '*'* 100
	# print "These are points I want to use for D3", df_total[2]
	# print '*'* 100



	return df_total
	# return all_totals

# organization()



