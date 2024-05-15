from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


db = SQLAlchemy(app)


class Submission(db.Model): #USE THIS EVERYTHIME U GET AN INPUT SRIRAM MAKE SURE TO USE SAME NAMING
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    item_description = db.Column(db.Text, nullable=False)
    found_or_lost = db.Column(db.String, nullable=False)
    contact_info = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)  


@app.route('/')  #sriram create return home on each site/template
def home():
    return render_template('index.html')


@app.route('/submitfounditem', methods=['GET', 'POST'])
def found():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        found_or_lost = 'found'
        contact_info = request.form['contact_info']
        location = request.form['location']
        new_submission = Submission(item_name=item_name, item_description=item_description, found_or_lost=found_or_lost, contact_info=contact_info, location=location) 
        db.session.add(new_submission)
        db.session.commit()
        return 'Thanks for submitting the found item!'
    return render_template('found.html') #I renamed a couple of Files when doing the other files just lookout - Sriram


@app.route('/submitlostitem', methods=['GET', 'POST'])
def lost():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_description = request.form['item_description']
        found_or_lost = 'lost'
        contact_info = request.form['contact_info']  # Get contact info from form
        location = request.form['location']  # Get location from form
        new_submission = Submission(item_name=item_name, item_description=item_description, found_or_lost=found_or_lost,
                                    contact_info=contact_info, location=location)  # Pass contact info and location
        db.session.add(new_submission)
        db.session.commit()
        return 'Thanks for reporting the lost item!'
    return render_template('lost.html')


@app.route('/founditems')
def found_items():
    found_items = Submission.query.filter_by(found_or_lost='found').all()
    return render_template('found_items_list.html', items=found_items)


@app.route('/lostitems')
def lost_items():
    lost_items = Submission.query.filter_by(found_or_lost='lost').all()
    return render_template('lost_items_list.html', items=lost_items)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()




