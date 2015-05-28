"""Models and database functions for Ikura project"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """Ikura users"""


    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
  
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s ........>" % (self.user_id, self.email)

class Card(db.Model):
    """Holds information about a user's credit cards"""

    __tablename__ = "cards"

    card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_name = db.Column(db.String(64), nullable=False)
    card_debt = db.Column(db.Float, nullable=False)
    card_apr = db.Column(db.Float, nullable=False)
    # need to change all the names of this. date is not right. It's months to pay off....
    # change here and in server, calculations and html
    card_date = db.Column(db.Integer, nullable=True)
    min_payment = db.Column(db.String(64), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship("User", backref="Card")

    #  if i need to change just one table in db I can drop that
    # one table and then do db.create_all() in -i model.py and it'll add that new table....

    def updated_card(card_name, card_debt, card_apr, card_date, min_payment, user_id):
        Card.update().where(Card.card_id = card_id).values(card_name = card_name, 
                                                            card_debt = card_debt, 
                                                            card_apr = card_apr, 
                                                            card_date = card_date, 
                                                            min_payment = min_payment, 
                                                            user_id = user_id)

# table.update().returning(table.c.col1, table.c.col2).\
#     where(table.c.name=='foo').values(name='bar')


    def __repr__(self):
        """Provide helpful card representation when printed."""

        return "<Card card_id=%s card_name=%s ........>" % (self.card_id, self.card_name)


class Value(db.Model):
    """Stores user answers for value question: money, time, sanity"""

    
    __tablename__ = "values"


    value_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    money_spent_high = db.Column(db.BOOLEAN)
    money_spent_low = db.Column(db.BOOLEAN)
    time_1 = db.Column(db.BOOLEAN)
    time_2 = db.Column(db.BOOLEAN)
    time_3 = db.Column(db.BOOLEAN)
    money_amnt_low = db.Column(db.BOOLEAN)
    money_amnt_high = db.Column(db.BOOLEAN)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    def __repr__(self):
        """Provide helpful card representation when printed."""

        return "<Card card_id=%s card_name=%s ........>" % (self.card_id, self.card_name)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configuring PostgreSQL 
    # Will this link to localhost change once I have this deployed? <- yes
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/ikura'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    # we want to connect to the db after lines 3-5 run.

    from server import app
    connect_to_db(app)
    print "Connected to DB."



