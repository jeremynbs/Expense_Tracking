from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database setup

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Dashboard route

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/dashboard-summary')
def dashboard_summary():
    conn = get_db()
    cur = conn.cursor()
    current_month = datetime.now().strftime('%Y-%m')
    cur.execute('''
        SELECT SUM(amount) as total, category
        FROM expenses
        WHERE strftime('%Y-%m', date) = ?
        GROUP BY category
    ''', (current_month,))
    rows = cur.fetchall()
    data = [{'category': row['category'], 'total': row['total']} for row in rows]
    return jsonify(data)

# Expense routes

@app.route('/expenses')
def expenses_page():
    return render_template('expenses.html')

@app.route('/api/expenses', methods=['GET', 'POST'])
def manage_expenses():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'GET':
        category = request.args.get('category')
        date = request.args.get('date')
        query = 'SELECT * FROM expenses WHERE 1=1'
        params = []

        if category:
            query += ' AND category = ?'
            params.append(category)
        if date:
            query += ' AND date = ?'
            params.append(date)

        cur.execute(query, params)
        rows = cur.fetchall()
        return jsonify([dict(row) for row in rows])

    if request.method == 'POST':
        data = request.json
        cur.execute('INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)',
                    (data['amount'], data['category'], data['date'], data.get('note')))
        conn.commit()
        return jsonify({'status': 'success'})

@app.route('/api/expenses/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_expense(id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'PUT':
        data = request.json
        cur.execute('UPDATE expenses SET amount=?, category=?, date=?, note=? WHERE id=?',
                    (data['amount'], data['category'], data['date'], data.get('note'), id))
        conn.commit()
        return jsonify({'status': 'updated'})

    if request.method == 'DELETE':
        cur.execute('DELETE FROM expenses WHERE id=?', (id,))
        conn.commit()
        return jsonify({'status': 'deleted'})
    

# Income routes

@app.route('/income')
def income_page():
    return render_template('income.html')

@app.route('/api/income', methods=['GET', 'POST'])
def handle_income():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'GET':
        cur.execute('SELECT * FROM income ORDER BY date DESC')
        rows = cur.fetchall()
        return jsonify([dict(row) for row in rows])

    if request.method == 'POST':
        data = request.json
        cur.execute('INSERT INTO income (amount, date) VALUES (?, ?)',
                    (data['amount'], data['date']))
        conn.commit()
        return jsonify({'status': 'created'})

@app.route('/api/income/<int:id>', methods=['PUT', 'DELETE'])
def modify_income(id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'PUT':
        data = request.json
        cur.execute('UPDATE income SET amount = ?, date = ? WHERE id = ?',
                    (data['amount'], data['date'], id))
        conn.commit()
        return jsonify({'status': 'updated'})

    if request.method == 'DELETE':
        cur.execute('DELETE FROM income WHERE id = ?', (id,))
        conn.commit()
        return jsonify({'status': 'deleted'})

# Category routes

@app.route('/categories')
def categories_page():
    return render_template('categories.html')

@app.route('/api/categories', methods=['GET', 'POST'])
def manage_categories():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'GET':
        cur.execute('SELECT * FROM categories')
        rows = cur.fetchall()
        return jsonify([dict(row) for row in rows])

    if request.method == 'POST':
        data = request.json
        cur.execute('INSERT INTO categories (name, budget) VALUES (?, ?)',
                    (data['name'], data.get('budget')))
        conn.commit()
        return jsonify({'status': 'created'})

@app.route('/api/categories/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_category(id):
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'PUT':
        data = request.json
        cur.execute('UPDATE categories SET name=?, budget=? WHERE id=?',
                    (data['name'], data['budget'], id))
        conn.commit()
        os.utime('templates/categories.html', None)
        return jsonify({'status': 'updated', 'redirect': '/categories'})

    if request.method == 'DELETE':
        cur.execute('DELETE FROM categories WHERE id=?', (id,))
        conn.commit()
        return jsonify({'status': 'deleted'})


if __name__ == '__main__':
    app.run(debug=True)
