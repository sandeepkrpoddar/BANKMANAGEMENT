from datetime import datetime
import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"
    data = []

    # Load data
    if Path(database).exists():
        try:
            with open(database, "r") as fs:
                data = json.load(fs)
        except json.JSONDecodeError:
            data = []

    @classmethod
    def save_data(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def generate_account(cls):
     while True:
        account = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8
            )
        )

        exists = any(
            user.get("accountNo") == account
            for user in cls.data
        )

        if not exists:
            return account

    @classmethod
    def find_user(cls, account, pin):
        for user in cls.data:
            if (
                user["accountNo"] == account
                and user["pin"] == pin
            ):
                return user

        return None

    def create_account(self, name, age, email, pin):

        if not name:
            return "Name required"

        if age < 18:
            return "Age must be 18+"

        if len(str(pin)) != 4:
            return "PIN must be 4 digits"

        user = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": self.generate_account(),
            "transactions": [],
            "balance": 0
        }

        self.data.append(user)
        self.save_data()

        return user

    def deposit(self, account, pin, amount):

        user = self.find_user(account, pin)

        if not user:
            return "User not found"

        if amount <= 0:
            return "Invalid amount"

        user["balance"] += amount
        
        transation = {
            "type": "deposit",
            "amount": amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%p")
        }
        user["transactions"].append(transation)
        self.save_data()

        return "Deposit Successful"

    def withdraw(self, account, pin, amount):

        user = self.find_user(account, pin)

        if not user:
            return "User not found"

        if amount <= 0:
            return "Invalid amount"

        if amount > user["balance"]:
            return "Insufficient Balance"

        user["balance"] -= amount

        transation = {
            "type": "withdraw",
            "amount": amount,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M:%p")
        }
        user["transactions"].append(transation)
        self.save_data()

        return "Withdraw Successful"

    def get_details(self, account, pin):

        user = self.find_user(account, pin)

        if user:
            user_copy = user.copy()
            del user_copy["pin"]

            return user_copy

        return None
    def get_transactions(self, account, pin):

        user = self.find_user(account, pin)

        if user:
            return user["transactions"]

        return None