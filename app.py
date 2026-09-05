from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'expense-tracker-demo-key'

# Render par database ko current project directory mein rakho
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, 'expenses.db')


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# IMPORTANT: Gunicorn/Render app start karte waqt bhi database tables create karega
init_db()


def today():
    return datetime.now().strftime('%Y-%m-%d')


@app.route('/')
def index():
    conn = db()

    income = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM income'
    ).fetchone()[0]

    expense = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM expenses'
    ).fetchone()[0]

    transactions = conn.execute(
        'SELECT COUNT(*) FROM expenses'
    ).fetchone()[0]

    today_expense = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date=?',
        (today(),)
    ).fetchone()[0]

    expenses = conn.execute(
        'SELECT * FROM expenses ORDER BY id DESC'
    ).fetchall()

    conn.close()

    return render_template(
        'index.html',
        income=income,
        expense=expense,
        transactions=transactions,
        today_expense=today_expense,
        balance=income - expense,
        expenses=expenses,
        query=''
    )


@app.post('/income/add')
def add_income():
    try:
        amount = float(request.form['amount'])
    except:
        amount = 0

    if amount <= 0:
        flash('Valid income amount enter karo.', 'error')
        return redirect(url_for('index'))

    conn = db()

    conn.execute(
        'INSERT INTO income(amount, date) VALUES(?, ?)',
        (amount, today())
    )

    conn.commit()
    conn.close()

    flash('Income successfully added.', 'success')
    return redirect(url_for('index'))


@app.route('/income/history')
def income_history():
    conn = db()

    rows = conn.execute(
        'SELECT * FROM income ORDER BY id DESC'
    ).fetchall()

    total = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM income'
    ).fetchone()[0]

    conn.close()

    return render_template(
        'income_history.html',
        rows=rows,
        total=total
    )


@app.post('/income/delete/<int:id>')
def delete_income(id):
    conn = db()

    conn.execute(
        'DELETE FROM income WHERE id=?',
        (id,)
    )

    conn.commit()
    conn.close()

    flash('Income deleted.', 'success')
    return redirect(url_for('income_history'))


@app.route('/income/edit/<int:id>', methods=['GET', 'POST'])
def edit_income(id):
    conn = db()

    row = conn.execute(
        'SELECT * FROM income WHERE id=?',
        (id,)
    ).fetchone()

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
        except:
            amount = 0

        if amount <= 0:
            flash('Valid amount enter karo.', 'error')
            conn.close()
            return redirect(url_for('edit_income', id=id))

        conn.execute(
            'UPDATE income SET amount=? WHERE id=?',
            (amount, id)
        )

        conn.commit()
        conn.close()

        flash('Income updated.', 'success')
        return redirect(url_for('income_history'))

    conn.close()

    return render_template(
        'edit_income.html',
        row=row
    )


@app.post('/expense/add')
def add_expense():
    category = request.form['category'].strip()
    desc = request.form['description'].strip()

    try:
        amount = float(request.form['amount'])
    except:
        amount = 0

    if amount <= 0 or not category:
        flash(
            'Amount aur category valid honi chahiye.',
            'error'
        )
        return redirect(url_for('index'))

    conn = db()

    conn.execute(
        '''
        INSERT INTO expenses(amount, category, description, date)
        VALUES(?, ?, ?, ?)
        ''',
        (amount, category, desc, today())
    )

    conn.commit()
    conn.close()

    flash('Expense successfully added.', 'success')
    return redirect(url_for('index'))


@app.route('/expense/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    conn = db()

    row = conn.execute(
        'SELECT * FROM expenses WHERE id=?',
        (id,)
    ).fetchone()

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
        except:
            amount = 0

        category = request.form['category'].strip()
        desc = request.form['description'].strip()

        if amount <= 0 or not category:
            flash(
                'Valid amount/category enter karo.',
                'error'
            )
            conn.close()
            return redirect(url_for('edit_expense', id=id))

        conn.execute(
            '''
            UPDATE expenses
            SET amount=?, category=?, description=?
            WHERE id=?
            ''',
            (amount, category, desc, id)
        )

        conn.commit()
        conn.close()

        flash('Expense updated.', 'success')
        return redirect(url_for('index'))

    conn.close()

    return render_template(
        'edit_expense.html',
        row=row
    )


@app.post('/expense/delete/<int:id>')
def delete_expense(id):
    conn = db()

    conn.execute(
        'DELETE FROM expenses WHERE id=?',
        (id,)
    )

    conn.commit()
    conn.close()

    flash('Expense deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/search')
def search():
    q = request.args.get('q', '').strip()

    conn = db()

    if q:
        expenses = conn.execute(
            '''
            SELECT * FROM expenses
            WHERE category LIKE ? OR description LIKE ?
            ORDER BY id DESC
            ''',
            (f'%{q}%', f'%{q}%')
        ).fetchall()
    else:
        expenses = conn.execute(
            'SELECT * FROM expenses ORDER BY id DESC'
        ).fetchall()

    income = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM income'
    ).fetchone()[0]

    expense = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM expenses'
    ).fetchone()[0]

    transactions = conn.execute(
        'SELECT COUNT(*) FROM expenses'
    ).fetchone()[0]

    today_expense = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date=?',
        (today(),)
    ).fetchone()[0]

    conn.close()

    return render_template(
        'index.html',
        income=income,
        expense=expense,
        transactions=transactions,
        today_expense=today_expense,
        balance=income - expense,
        expenses=expenses,
        query=q
    )


@app.route('/analytics')
def analytics():
    conn = db()

    categories = conn.execute(
        '''
        SELECT category, SUM(amount) total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
        '''
    ).fetchall()

    months = conn.execute(
        '''
        SELECT substr(date, 1, 7) month, SUM(amount) total
        FROM expenses
        GROUP BY month
        ORDER BY month DESC
        '''
    ).fetchall()

    total_expense = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM expenses'
    ).fetchone()[0]

    total_income = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) FROM income'
    ).fetchone()[0]

    highest_category = categories[0] if categories else None

    highest_month = (
        max(months, key=lambda x: x['total'])
        if months else None
    )

    conn.close()

    return render_template(
        'analytics.html',
        categories=categories,
        months=months,
        total_expense=total_expense,
        total_income=total_income,
        balance=total_income - total_expense,
        highest_category=highest_category,
        highest_month=highest_month
    )


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
