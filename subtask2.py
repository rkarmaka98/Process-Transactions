from flask import Flask, request, jsonify
import pandas as pd

# Load the users data
file_path = 'usersSubTask1.csv'
users_df = pd.read_csv(file_path)

app = Flask(__name__)

# Helper function to update CSV file after a transaction
def update_csv(df, file_path):
    df.to_csv(file_path, index=False)

@app.route('/transfer', methods=['POST'])
def transfer():
    # Extract data from request
    data = request.json
    sender_id = int(data['sender_id'])
    receiver_id = int(data['receiver_id'])
    amount = float(data['amount'])
    
    # Check if sender account exists
    sender = users_df[users_df['user_id'] == sender_id]
    if sender.empty:
        return jsonify({"message": "Invalid sender account id, transaction was not processed."}), 513
    
    # Check if receiver account exists
    receiver = users_df[users_df['user_id'] == receiver_id]
    if receiver.empty:
        return jsonify({"message": "Invalid receiver account id, transaction was not processed."}), 514
    
    # Check if sender has enough balance
    if sender.iloc[0]['balance'] < amount:
        return jsonify({"message": "Invalid balance, transaction was not processed."}), 512
    
    # Process the transaction
    users_df.loc[users_df['user_id'] == sender_id, 'balance'] -= amount
    users_df.loc[users_df['user_id'] == receiver_id, 'balance'] += amount
    
    # Update the CSV file
    update_csv(users_df, file_path)
    
    return jsonify({"message": "Successful transaction, users.csv has been appended."}), 200

if __name__ == '__main__':
    app.run(debug=True)
