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

    # print "date right?", date
    interest_per_month = apr/date
    # print "int rate", interest_per_month
    monthly_payment_suggestion = float(debt) / float((date + 1))
    # print "This should be the right number!", monthly_payment_suggestion
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


def calculations_int(query_results, budget):

    # make sure in html. budget is over {{total amount of sugg payments}}
    # budget = 500  # USER MUST ENTER THIS IN!
    payment_info_list = []
    num_of_cards_orig = []


    for card in query_results:
        name = card.card_name
        card.current_debt = -1
        # want to update highest_apr to true for the first card (aka the highest int rate). How do?
        card.highest_apr = True
        apr = card.card_apr
        #This will turn user inputted apr into percentage
        apr = apr/100
        date = card.card_date
        min_payment = card.min_payment
        user_id = card.user_id
        sugg_payment = card.card_sugg
        card.card_sugg = card.card_debt / (date + 1)
        sugg_payment = card.card_sugg
        num_of_cards_orig.append(card)

    for card in query_results[1:]:
        card.highest_apr = False

    num_of_cards = num_of_cards_orig
    date_list = []
    
    for card in num_of_cards:
        date_list.append(card.card_date)

    avg_num_of_months = sum(date_list) / len(date_list)


    # calculating extra budget 
    sugg_payment_total = []
    for card in num_of_cards: 
        sugg_payment = card.card_sugg
        sugg_payment_total.append(sugg_payment)
    sugg_payment_total = sum(sugg_payment_total)
    extra_budget =  budget - sugg_payment_total


    card_info = {}
    decr_debt = []
    total_decr_debt = []
    payments = []
    total_payments = []

    # This should calculate the monthly payments for each card. 
    # Will also add in the extra budget amount too for 
    # higest int card until paid off
    i = 0

    for month in range(avg_num_of_months + 1):
        extra_budget = extra_budget
        for card in  num_of_cards:
            if card.current_debt > 0:
                if card.highest_apr == True:
                    payment_result = card.current_debt - card.card_sugg - extra_budget
                    if payment_result <= 0:
                        decr_debt.append(card.current_debt)
                        payments.append(card.card_sugg + extra_budget)
                        card.current_debt = 0
                    else:
                        decr_debt.append(card.current_debt)
                        payments.append(card.card_sugg + extra_budget)
                        card.current_debt = payment_result
                else:
                    payment_result = card.current_debt - card.card_sugg
                    if payment_result <= 0:
                        decr_debt.append(card.current_debt)
                        payments.append(card.card_sugg)
                        card.current_debt = 0
                    else:
                        decr_debt.append(card.current_debt)
                        payments.append(card.card_sugg)
                        card.current_debt = payment_result
                
            elif card.current_debt == 0:
                decr_debt.append(card.current_debt)
                payments.append(0)
                card.current_debt = 0
                if card.highest_apr == True:
                    i = num_of_cards.index(card)
                    num_of_cards[i].highest_apr = False
                    i += 1
                    if i < len(num_of_cards):
                        num_of_cards[i].highest_apr = True
                        print "next card?", num_of_cards[i]
                    else:
                        print "you outta line!"
                else:
                    sugg_payment_total = sugg_payment_total - card.card_sugg
                    extra_budget =  budget - sugg_payment_total
                    # i = num_of_cards.index(card)
                    # num_of_cards[i].highest_apr == False
                    # i += 1
                    # num_of_cards[i].highest_apr == True
                    # print "next card?", num_of_cards[i]

            elif card.card_debt > 0:
                if card.highest_apr == True:
                    payment_result = card.card_debt - card.card_sugg - extra_budget
                    if payment_result <= 0:
                        card.current_debt = 0
                        decr_debt.append(card.card_debt)
                        payments.append(card.card_sugg + extra_budget)
                    else:
                        card.current_debt = payment_result
                        decr_debt.append(card.card_debt)
                        payments.append(card.card_sugg + extra_budget)
                else: 
                    payment_result = card.card_debt - card.card_sugg
                    if payment_result <= 0:
                        card.current_debt = 0
                        decr_debt.append(card.card_debt)
                        payments.append(card.card_sugg)
                    else:
                        card.current_debt = payment_result
                        decr_debt.append(card.card_debt)
                        payments.append(card.card_sugg)   
        # print "is this one each month?", decr_debt
        total_decr_debt.append(decr_debt)
        total_payments.append(payments)
        decr_debt = []
        payments =[]

    # ********************************************************************
    # *************************************
    # QUESTION : how to make this scalable
    # and not specify right now how to unpack this
    # *************************************

    card1d, card2d, card3d = zip(*total_decr_debt)
    card1p, card2p, card3p = zip(*total_payments)

    # print "list1", card1d
    # print "lsit 1 for payments", card1p
    # print "list2", card2
    # print "list3", card3

    card_listd = [card1d, card2d, card3d]
    card_listp = [card1p, card2p, card3p]

    # ********************************************************************

    int_rate_dict = {}
    int_info_dict = {}
    int_info_list = []
    counter = 0

    for card in query_results:
        list_for_card_d = card_listd[counter]
        list_for_card_p = card_listp[counter]
        int_info_dict["Decreasing_Debt"] = list_for_card_d
        # print "Dict", decr_debt_dict
        int_info_dict["Payments"] = list_for_card_p
        # print "Dict", payments_dict
        info = list_for_card_d, list_for_card_p
        int_info_list.append(info)



        # int_info = [decr_debt_dict, payments_dict]
        int_rate_dict[card.card_name] = int_info_dict
        counter += 1

    points_for_cards = []
    for num in range(len(int_info_list)):
        card_all = int_info_list[num]
        debt_pay_point = zip(*card_all)
        num += 1
        points_for_cards.append(debt_pay_point)
    # print "final (debt, payment) points for card", points_for_cards
    # print "what is this", points_for_cards[0]
    # print "dict:", int_rate_dict

    passed_data = [int_rate_dict, points_for_cards]

    return passed_data
# TODO: calculate interest rate and payments

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


def user_cards_int(results_of_query, budget):
    """Loop over all cards user has entered and return a dictionary of dictionaries.
    The outer dictionary key = user_id, values = cards
    The inner dictionary key = name of a card, values = min payments, min intr rates,
                                                        min debt decrease, suggested payments,
                                                        suggested intr rates, suggested debt decrease """
    user_dict = {}
    card_dict_int_list = []
    for card in results_of_query:
        user_id = card.user_id

    # budget = 500

    int_calcs = calculations_int(results_of_query, budget)
    # user_dict_int = {user_id : [int_calcs]}


    return int_calcs

def total_sugg_payments(results_of_query):
    """Calculates the suggested payments for all cards that one need to pay per month"""

    sugg_payment_total = []

    for card in results_of_query:
        sugg_payment = card.card_sugg
        sugg_payment_total.append(sugg_payment)


    sugg_payment_total = sum(sugg_payment_total)

    return sugg_payment_total

def total_sugg_int_paid():
    pass

def total_min_int_paid():
    pass



# TODO: #
# Add in docstring tests to make sure these calculations work all of the time
# Or don't work when something bad is entered
# Or state assumptions so extra testing is unecessary
#     such as not testing for negative numbers since html form does not allow
