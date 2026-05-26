from datetime import datetime
import json
import random
import string
from pathlib import Path


class Bank:

    database = "data.json"
    data = []

    # Load database
    if Path(database).exists():
        try:
            with open(database, "r") as fs:
                data = json.load(fs)

        except json.JSONDecodeError:
            data = []

    @classmethod
    def save_data(cls):

        with open(
            cls.database,
            "w"
        ) as fs:

            json.dump(
                cls.data,
                fs,
                indent=4
            )

    @classmethod
    def generate_account(cls):

        while True:

            account = ''.join(
                random.choices(
                    string.ascii_uppercase +
                    string.digits,
                    k=8
                )
            )

            exists = any(
                user.get(
                    "accountNo"
                ) == account
                for user in cls.data
            )

            if not exists:
                return account

    @classmethod
    def find_user(
        cls,
        account,
        pin
    ):

        for user in cls.data:

            if (
                user["accountNo"] == account
                and user["pin"] == pin
            ):

                return user

        return None

    # ---------------- CREATE ----------------

    def create_account(
        self,
        name,
        age,
        email,
        pin
    ):

        if not name:
            return "Name required"

        if age < 18:
            return "Age must be 18+"

        if (
            not str(pin).isdigit()
            or len(str(pin)) != 4
        ):
            return (
                "PIN must be exactly "
                "4 digits"
            )

        if (
            "@" not in email
            or "." not in email
        ):
            return "Invalid Email"

        user = {

            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo":
            self.generate_account(),
            "balance": 0,
            "transactions": []

        }

        self.data.append(user)

        self.save_data()

        return user

    # ---------------- DEPOSIT ----------------

    def deposit(
        self,
        account,
        pin,
        amount
    ):

        user = self.find_user(
            account,
            pin
        )

        if not user:
            return "User not found"

        if amount <= 0:
            return "Invalid Amount"

        user["balance"] += amount

        transaction = {

            "type": "Deposit",
            "amount": amount,
            "date":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )

        }

        user["transactions"].append(
            transaction
        )

        self.save_data()

        return "Deposit Successful"

    # ---------------- WITHDRAW ----------------

    def withdraw(
        self,
        account,
        pin,
        amount
    ):

        user = self.find_user(
            account,
            pin
        )

        if not user:
            return "User not found"

        if amount <= 0:
            return "Invalid Amount"

        if amount > user["balance"]:
            return (
                "Insufficient Balance"
            )

        user["balance"] -= amount

        transaction = {

            "type": "Withdraw",
            "amount": amount,
            "date":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )

        }

        user["transactions"].append(
            transaction
        )

        self.save_data()

        return "Withdraw Successful"

    # ---------------- DETAILS ----------------

    def get_details(
        self,
        account,
        pin
    ):

        user = self.find_user(
            account,
            pin
        )

        if user:

            user_copy = user.copy()

            del user_copy["pin"]

            return user_copy

        return None

    # ---------------- DELETE ----------------

    def delete_account(
        self,
        account,
        pin
    ):

        user = self.find_user(
            account,
            pin
        )

        if not user:
            return "User not found"

        self.data.remove(user)

        self.save_data()

        return (
            "Account Deleted Successfully"
        )

    # ---------------- UPDATE ----------------

    def update_account(
        self,
        account,
        pin,
        new_name,
        new_email
    ):

        user = self.find_user(
            account,
            pin
        )

        if not user:
            return "User not found"

        if new_name:
            user["name"] = new_name

        if new_email:
            user["email"] = new_email

        self.save_data()

        return (
            "Account Updated Successfully"
        )

    # ---------------- HISTORY ----------------

    def get_transactions(
        self,
        account,
        pin
    ):

        user = self.find_user(
            account,
            pin
        )

        if user:
            return user[
                "transactions"
            ]

        return None