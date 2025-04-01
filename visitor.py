import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import db1  # Assuming your db1 module is set up correctly.

st.title("Welcome to the Visitor Management System!")

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Login", "Registration", "View", "Update", "Delete"],
        icons=["person", "person", "list-task", "person-lines-fill", "trash"]
    )

if selected == "Login":
    st.header("Login Page")
    with st.form('form'):
        name = st.text_input("Name")
        contact = st.text_input("Contact")
        submitted = st.form_submit_button("Submit")

    if submitted:
        if not name or not contact:
            st.error("Please fill in both Name and Contact.")
        else:
            data = (name, contact)
            res = db1.login(data)
            if res:
                st.success("User logged in successfully!")
            else:
                st.error("Invalid credentials. Please try again.")

elif selected == "Registration":
    st.header("Registration Page")
    with st.form('form'):
        name = st.text_input("Name")
        purpose = st.text_input("Purpose")
        contact = st.text_input("Contact (10-digit number)")
        date = st.date_input("Date")
        submitted = st.form_submit_button("Submit")

    if submitted:
        if not name or not purpose or not contact or not date:
            st.error("Please fill in all the fields.")
        elif len(contact) != 10 or not contact.isdigit():
            st.error("Please enter a valid 10-digit contact number.")
        else:
            data = (name, purpose, contact, str(date))
            res = db1.reg(data)
            if res:
                st.success("Visitor registered successfully!")
            else:
                st.error("Registration failed. Please try again.")

elif selected == "View":
    st.header("Viewing Page")
    res = db1.view()
    if res:
        df = pd.DataFrame(res, columns=["ID", "Name", "Purpose", "Contact", "Date"])
        st.dataframe(df)
    else:
        st.error("No records found.")

elif selected == "Update":
    st.header("Update Page")
    id = st.number_input("Enter ID",min_value=0)
    res = db1.readone(id)

    if res:
        with st.form('form'):
            name = st.text_input("Name", value=res[1])
            purpose = st.text_input("Purpose", value=res[2])
            contact = st.text_input("Contact", value=res[3])
            date = st.date_input("Date", value=pd.to_datetime(res[4]))
            submitted = st.form_submit_button("Submit")

        if submitted:
            if not name or not purpose or not contact or not date:
                st.error("Please fill in all the fields.")
            elif len(contact) != 10 or not contact.isdigit():
                st.error("Please enter a valid 10-digit contact number.")
            else:
                data = (name, purpose, contact, str(date), id)
                res = db1.update(data)
                if res:
                    st.success("Data updated successfully!")
                else:
                    st.error("Update failed. Please try again.")
    else:
        st.error("No record found with the given ID.")

elif selected == "Delete":
    st.header("Delete Page")
    id = st.number_input("Enter ID", step=1, min_value=0)
    res = db1.readone(id)

    if res:
        with st.form('form'):
            name = st.text_input("Name", value=res[1])
            purpose = st.text_input("Purpose", value=res[2])
            contact = st.text_input("Contact", value=res[3])
            date = st.date_input("Date", value=pd.to_datetime(res[4]))
            button = st.form_submit_button("Delete")

        if button:
            result = db1.delete(id)
            if result:
                st.success("Record deleted successfully!")
            else:
                st.error("Deletion failed. Please try again.")
    else:
        st.error("No record found with the given ID.")
