"""Models and database functions for Ikura project"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """Ikura users"""


    __tablename__ = "Users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
  
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

class Card(db.Model):
    """Holds information about a user's credit cards"""

    __tablename__ = "Cards"

    card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    card_name = db.Column(db.String(64), nullable=False)
    card_debt = db.Column(db.Integer, nullable=False)
    card_apr = db.Column(db.Integer, nullable=False)
    card_date = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))


    def __repr__(self):
        """Provide helpful card representation when printed."""

        return "<Card card_id=%s card_name=%s>" % (self.card_id, self.card_name)

# *************************************************
# ASK 

# How to best structure this data?

# *************************************************


class Value(db.Model):
    """Stores user answers for value question: money, time, sanity"""

    __tablename__ = "Values"

    # TODO: Make sure you can have boolean values? Ask if this is the best strategy for this.

    value_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    money_high = db.Column()
    money_low = db.Column()
    time_1 = db.Column()
    time_2 = db.Column()
    time_3 = db.Column()
    money_low = db.Column()
    money_low = db.Column()
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))


    def __repr__(self):
        """Provide helpful card representation when printed."""

        return "<Card card_id=%s card_name=%s>" % (self.card_id, self.card_name)

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ikura.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."



