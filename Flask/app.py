from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):
    SNO = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False, unique=True)
    Subject = db.Column(db.String(200), nullable=False)
    Message = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Name}"

if not os.path.exists('contact.db'):
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Validate the form data
        if not name or not email or not subject or not message:
            return jsonify({"error": "Please fill all the fields"}), 400

        # Create a new Contact entry
        new_contact = Contact(Name=name, Email=email, Subject=subject, Message=message)

        # Add to the database
        try:
            db.session.add(new_contact)
            db.session.commit()
            return jsonify({"success": "Message successfully sent!"}), 200
        except Exception as e:
            return jsonify({"error": "There was an issue adding your message. Same message cannot be sent."}), 500

if __name__ == '__main__':
    app.run(debug=True)
