card_name_1 = "Master"
card_debt_1 = 1000
card_apr_1 = .1
card_date_1 = 12


card_name_2 = "Visa"
card_debt_2 = 2000
card_apr_2 = .15
card_date_2 = 12


budget = float(500)

def sugg_payment(debt, date):
	sugg_payment = float(debt/(date + 1))
	return sugg_payment


def int_per_month(apr, date):
	int_per_month = float(apr / date)
	print int_per_month


def max_budget_for_card(budget, sugg_payment):
	max_budget_for_card = float(budget - sugg_payment)
	print max_budget_for_card

sugg_payment_1 = sugg_payment(card_debt_1, card_date_1)
sugg_payment_2 = sugg_payment(card_debt_2, card_date_2)

int_per_month(card_apr_1, card_date_1)
int_per_month(card_apr_2, card_date_2)

max_budget_for_card(budget, sugg_payment_1)
max_budget_for_card(budget, sugg_payment_2)

#  the max_budget_for_card should be a float with slightly different numbers....