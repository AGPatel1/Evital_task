from flask import Flask, jsonify, request
import sqlite3

db_conn = sqlite3.connect('bank_database.db') 
# connect() -> Gives a connection object from which you can connect to db
# Parameter of fucntion is db file. Can be created automatically by connect()

cursor = db_conn.cursor()
#Allows to send Sql commands to Database

# Table  Account -> Account Number primary key (Auto incremented) , Name ,Balance 
cursor.execute(
    "CREATE TABLE IF NOT EXISTS Accounts (account_number INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, balance REAL)"
)

cursor.execute('SELECT * FROM Accounts')
rows_number = cursor.fetchall()

# Only Executed one time when Empty DB is Created
# Inserts Values in Empty DataBase
if len(rows_number)<1:
    cursor.execute('INSERT INTO Accounts(account_number,name,balance) VALUES (1001,"abc",1000)')
    cursor.execute('INSERT INTO Accounts(name,balance) VALUES ("abcd",5000)')
    cursor.execute('INSERT INTO Accounts(name,balance) VALUES ("xyz",8000)')

#Prints values from DB
cursor.execute('SELECT * FROM Accounts')
rows = cursor.fetchall()
for row in rows:
    print(row)

db_conn.commit()
db_conn.close()

app = Flask(__name__)

@app.route('/create_account', methods = ['POST'])
# create account ->R auto(account number), name , balance
def create_account():
    data = request.form
    db_conn = sqlite3.connect('bank_database.db')
    cursor = db_conn.cursor()

    cursor.execute(
        "INSERT INTO Accounts (name , balance) VALUES (?, ?)",(data.get('name'),data.get('balance'))
    )

    cursor.execute(
        "SELECT * FROM Accounts ORDER BY account_number DESC LIMIT 1"
    )

    acc_details = cursor.fetchone()

    db_conn.commit()
    db_conn.close()

    return jsonify({'message': 'Account created successfully','Account Details':acc_details})

@app.route('/update_account', methods = ['PUT'])
# update account details ->Req : account number , balance -> Return : balance (updated)
def update_account():
    data = request.form
    db_conn = sqlite3.connect('bank_database.db')
    cursor = db_conn.cursor()

    cursor.execute(
        "UPDATE Accounts SET balance = ?  WHERE account_number = ?", (data.get('balance'),data.get('account_number'))
    )

    db_conn.commit()
    db_conn.close()

    return jsonify({'message': 'Account Updated Successfully'})

@app.route('/delete_account', methods = ['DELETE'])
# delete account  -> Req : Account number -> Returns : None (Deletes Account)
def delete_account():
    data = request.form
    db_conn = sqlite3.connect('bank_database.db')
    cursor = db_conn.cursor()

    cursor.execute(
        "DELETE FROM Accounts WHERE account_number ="+ data.get('account_number')
    )

    db_conn.commit()
    db_conn.close()

    return jsonify({'message': 'Account Deleted Successfully'})

@app.route('/show_account_details/<account_number>', methods = ['GET'])
# show acount details -> Req : account number -> Returns : Account number, name, balance
def show_account_details(account_number):
    db_conn = sqlite3.connect('bank_database.db')
    cursor = db_conn.cursor()

    cursor.execute(
        "SELECT balance , name FROM Accounts where account_number="+ account_number
    )

    details = cursor.fetchone()
    db_conn.close()

    if details:
        return jsonify({'Details': details})
    
    return jsonify({'message': 'Account not Found'})

@app.route('/check_balance/<account_number>', methods = ['GET'])
# check current balance -> Req : account number -> Returns: balance
def check_balance(account_number):
    db_conn = sqlite3.connect('bank_database.db')
    cursor = db_conn.cursor()

    cursor.execute(
        "SELECT balance FROM Accounts where account_number="+ account_number
    )

    balance = cursor.fetchone()
    db_conn.close()

    if balance:
        return jsonify({'balance': balance})
    
    return jsonify({'message': 'Account not Found'})

if __name__ == "__main__":
    app.run()