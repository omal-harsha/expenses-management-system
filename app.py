from flask import Flask, render_template, redirect, url_for, request, jsonify

app = Flask(__name__)

entries = [
    {"id": 1, "category": "food", "describe": "getting food for party", "amount": 1000, "date": "2024-10-08", "type": "expense"},
    {"id": 2, "category": "bills", "describe": "electricity bill", "amount": 1000, "date": "2024-10-08", "type": "expense"},
    {"id": 3, "category": "travel", "describe": "vacation picnic", "amount": 1000, "date": "2024-10-08", "type": "expense"},
    {"id": 4, "category": "entertainment", "describe": "movie night tickets", "amount": 500, "date": "2024-10-07", "type": "expense"},
    {"id": 5, "category": "groceries", "describe": "weekly grocery shopping", "amount": 1500, "date": "2024-10-06", "type": "expense"},
    {"id": 6, "category": "transportation", "describe": "fuel for car", "amount": 2000, "date": "2024-10-05", "type": "expense"},
    {"id": 7, "category": "health", "describe": "gym membership fee", "amount": 3000, "date": "2024-10-04", "type": "expense"},
    {"id": 8, "category": "education", "describe": "buying books for school", "amount": 4000, "date": "2024-10-03", "type": "expense"},
    {"id": 9, "category": "clothing", "describe": "shopping for new clothes", "amount": 2500, "date": "2024-10-02", "type": "expense"},
    {"id": 10, "category": "gifts", "describe": "birthday present for friend", "amount": 3500, "date": "2024-10-01", "type": "expense"}
]

categories = [
    "food", "bills", "travel", "entertainment", "groceries", 
    "transportation", "health", "education", "clothing", "gifts"
]

def get_totals():
    total_expenses = sum(entry['amount'] for entry in entries if entry['type'] == 'expense')
    total_income = sum(entry['amount'] for entry in entries if entry['type'] == 'income')
    remaining_balance = total_income - total_expenses
    return total_expenses, total_income, remaining_balance

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html', hide_nav=True)

@app.route('/register')
def register():
    return render_template('register.html', hide_nav=True)

@app.route('/home')
def home():
    total_expenses, total_income, remaining_balance = get_totals()
    return render_template('home.html', entries=entries,
                           total_expenses=total_expenses, total_income=total_income,
                           remaining_balance=remaining_balance)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Handle form submission
        new_entry = {
            "id": max(entry['id'] for entry in entries) + 1,
            "category": request.form['category'],
            "describe": request.form['describe'],
            "amount": float(request.form['amount']),
            "date": request.form['date'],
            "type": request.form['type']
        }
        entries.append(new_entry)
        return redirect(url_for('home'))
    return render_template('add_edit_item.html', action='Add',categories=categories)

@app.route('/edit_item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    entry = next((entry for entry in entries if entry['id'] == id), None)
    if entry is None:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # Handle form submission
        entry.update({
            "category": request.form['category'],
            "describe": request.form['describe'],
            "amount": float(request.form['amount']),
            "date": request.form['date'],
            "type": request.form['type']
        })
        return redirect(url_for('home'))
    return render_template('add_edit_item.html', action='Edit', entry=entry, categories=categories)

@app.route('/report')
def report():
    return render_template('report.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['POST'])
def login_post():
    # Here you would normally check the credentials
    # For now, we'll just redirect to the home page
    return redirect(url_for('home'))

@app.route('/add_entry', methods=['POST'])
def add_entry():
    data = request.json
    new_entry = {
        "id": max(entry['id'] for entry in entries) + 1,
        "category": data['category'],
        "describe": data['describe'],
        "amount": float(data['amount']),
        "date": data['date'],
        "type": data['type']
    }
    
    entries.append(new_entry)
    
    total_expenses, total_income, remaining_balance = get_totals()
    
    return jsonify({
        "success": True,
        "new_entry": new_entry,
        "total_expenses": total_expenses,
        "total_income": total_income,
        "remaining_balance": remaining_balance
    })

@app.route('/edit_entry', methods=['POST'])
def edit_entry():
    data = request.json
    entry_id = int(data['id'])
    
    for entry in entries:
        if entry['id'] == entry_id:
            entry.update({
                "category": data['category'],
                "describe": data['describe'],
                "amount": float(data['amount']),
                "date": data['date'],
                "type": data['type']
            })
            break
    
    total_expenses, total_income, remaining_balance = get_totals()
    
    return jsonify({
        "success": True,
        "updated_entry": entry,
        "total_expenses": total_expenses,
        "total_income": total_income,
        "remaining_balance": remaining_balance
    })

@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    data = request.json
    entry_id = int(data['id'])
    
    global entries
    entries = [entry for entry in entries if entry['id'] != entry_id]
    
    total_expenses, total_income, remaining_balance = get_totals()
    
    return jsonify({
        "success": True,
        "total_expenses": total_expenses,
        "total_income": total_income,
        "remaining_balance": remaining_balance
    })

@app.route('/manage_categories')
def manage_categories():
    return render_template('manage_categories.html', categories=categories)

@app.route('/add_category', methods=['POST'])
def add_category():
    new_category = request.form['category']
    if new_category and new_category not in categories:
        categories.append(new_category)
    return redirect(url_for('manage_categories'))

@app.route('/edit_category', methods=['POST'])
def edit_category():
    old_category = request.form['old_category']
    new_category = request.form['new_category']
    if old_category in categories and new_category:
        index = categories.index(old_category)
        categories[index] = new_category
        # Update entries with the new category name
        for entry in entries:
            if entry['category'] == old_category:
                entry['category'] = new_category
    return redirect(url_for('manage_categories'))

@app.route('/delete_category', methods=['POST'])
def delete_category():
    category = request.form['category']
    if category in categories:
        categories.remove(category)
    return redirect(url_for('manage_categories'))

if __name__ == '__main__':
    app.run(debug=True)