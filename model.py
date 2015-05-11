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

# TODO: create this class below and create a table in db for this as well. 
 # class Card(db.Model):
# """Holds information about a user's credit cards"""

    # __tablename__ = "cards"

    # card_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # name = db.Column(db.String(64), nullable=False)
    # debt = db.Column(db.Integer, nullable=False)
    # apr = db.Column(db.Integer, nullable=False)
    # date = db.Column(db.Integer, nullable=True)

    #     def __repr__(self):
    #     """Provide helpful card representation when printed."""

    #     return "<Card card_id=%s name=%s>" % (self.card_id, self.name)

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