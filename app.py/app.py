from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin requests for frontend communication

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    date = db.Column(db.String(20))

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    result = []
    for expense in expenses:
        result.append({
            'id': expense.id,
            'description': expense.description,
            'category': expense.category,
            'amount': expense.amount,
            'date': expense.date
        })
    return jsonify(result)

@app.route('/api/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        description=data['description'],
        category=data['category'],
        amount=data['amount'],
        date=data['date']
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'})

@app.route('/api/expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'})
    return jsonify({'message': 'Expense not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
