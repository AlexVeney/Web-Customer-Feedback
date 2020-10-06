from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Initialize app
app = Flask(__name__)

# Environment
ENV = 'dev'

# Development mode settings
if ENV == 'dev':
    # When in development debug is turned on
    app.debug = True
    # When in development postgresql database is used
    string = "t_#333gSE'9Z664_"
    mod_string = 'postgresql://postgres:'+string+'@localhost/lexus'
    app.config['SQLALCHEMY_DATABASE_URI'] = mod_string
else:
    # Production mode settings
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

# added to stop warning message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database object
db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__='feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    # Initializer/constructor
    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

    """
    python command used to look at model, database and creates feedback table
    python
    from app import db
    db.create_all()
    """

# Main/default page loaded (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Submit page rendered when submit action post is called by form
@app.route('/submit', methods=['POST'])
def submit():
    # Checks that the submit is a POST method and not a GET
    if request.method == 'POST':
        # Gets information from the form variables
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        
        # Checks if customer and dealer are empty
        if customer == '' or dealer == '':
            # if fields are empty, index/html is rendered and message is output to user
            return render_template('index.html', message='Please enter required fields')
        
        # Checks if customer doesnt already exist
        # Commits feedback to db, renders success page after form submission
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
        
            return render_template('success.html')
        
        # If customer is duplicated, index rendered and message output to user
        return render_template('/index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()