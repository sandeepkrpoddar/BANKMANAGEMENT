import streamlit as st
from main import Bank

bank = Bank()

st.set_page_config(
    page_title="Bank App",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Simple Banking System")

# Sidebar Menu
menu = [
    "Create Account",
    "Deposit",
    "Withdraw",
    "Check Details",
    "Delete Account",
    "Update Account",
    "Transaction History"
]

choice = st.sidebar.selectbox(
    "Select Option",
    menu
)

# ---------------- CREATE ACCOUNT ----------------

if choice == "Create Account":

    st.subheader("Create New Account")

    name = st.text_input("Name")

    age = st.number_input(
        "Age",
        min_value=1,
        step=1
    )

    email = st.text_input("Email")

    pin = st.text_input(
        "4-digit PIN",
        type="password"
    )

    if st.button("Create Account"):

        if not pin.isdigit():

            st.error(
                "PIN should contain numbers only"
            )

        else:

            result = bank.create_account(
                name,
                age,
                email,
                int(pin)
            )

            if isinstance(result, dict):

                st.success(
                    "Account Created Successfully ✅"
                )

                st.write(
                    "Account Number:",
                    result["accountNo"]
                )

            else:
                st.error(result)

# ---------------- DEPOSIT ----------------

elif choice == "Deposit":

    st.subheader("Deposit Money")

    account = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    amount = st.number_input(
        "Amount",
        min_value=1
    )

    if st.button("Deposit"):

        if not pin.isdigit():

            st.error("Invalid PIN")

        else:

            result = bank.deposit(
                account,
                int(pin),
                amount
            )

            if "Successful" in result:
                st.success(result)

            else:
                st.error(result)

# ---------------- WITHDRAW ----------------

elif choice == "Withdraw":

    st.subheader("Withdraw Money")

    account = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    amount = st.number_input(
        "Amount",
        min_value=1
    )

    if st.button("Withdraw"):

        if not pin.isdigit():

            st.error("Invalid PIN")

        else:

            result = bank.withdraw(
                account,
                int(pin),
                amount
            )

            if "Successful" in result:
                st.success(result)

            else:
                st.error(result)

# ---------------- CHECK DETAILS ----------------

elif choice == "Check Details":

    st.subheader("Account Information")

    account = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    if st.button("Check Details"):

        if not pin.isdigit():

            st.error("Invalid PIN")

        else:

            user = bank.get_details(
                account,
                int(pin)
            )

            if user:

                st.success(
                    "Account Found ✅"
                )

                st.json(user)

            else:
                st.error(
                    "User Not Found"
                )

# ---------------- DELETE ACCOUNT ----------------

elif choice == "Delete Account":

    st.subheader("Delete Account")

    account = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    if st.button("Delete Account"):

        if not pin.isdigit():

            st.error("Invalid PIN")

        else:

            result = bank.delete_account(
                account,
                int(pin)
            )

            if "Successful" in result:
                st.success(result)

            else:
                st.error(result)

# ---------------- UPDATE ACCOUNT ----------------

elif choice == "Update Account":

    st.subheader("Update Account")

    account = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    new_name = st.text_input(
        "New Name"
    )

    new_email = st.text_input(
        "New Email"
    )

    if st.button("Update Account"):

        if not pin.isdigit():

            st.error("Invalid PIN")

        else:

            result = bank.update_account(
                account,
                int(pin),
                new_name,
                new_email
            )

            if "Successful" in result:
                st.success(result)

            else:
                st.error(result)

# ---------------- TRANSACTION HISTORY ----------------

elif choice == "Transaction History":

    st.subheader(
        "Transaction History"
    )

    account = st.text_input(
        "Account Number"
    )

    pin = st.text_input(
        "PIN",
        type="password"
    )

    if st.button(
        "View History"
    ):

        if pin.isdigit():

            transactions = (
                bank.get_transactions(
                    account,
                    int(pin)
                )
            )

            if transactions:

                st.success(
                    "Transactions Found ✅"
                )

                st.table(
                    transactions
                )

            else:

                st.error(
                    "No Transactions Found"
                )

        else:

            st.error(
                "Invalid PIN"
            )