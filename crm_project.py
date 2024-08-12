from flask import Flask, jsonify, request
import pyodbc
import pandas as pd
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=arabhiprojectserver.database.windows.net;'
        'DATABASE=crmdatabase;'
        'UID=arabhiserver;'
        'PWD=Arabhi1118'
    )
    return conn

def insert_customer_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create Customer DataFrame from Customer_Data.csv
        Customer_df = pd.read_csv("CMR_PROJECT\\Customer_Data_1.csv")

        # Insert DataFrame into SQL Server:
        for index, row in Customer_df.iterrows():
            cursor.execute("INSERT INTO Customer ( customer_name, email, signup_date, loyalty_score) VALUES ( ?, ?, ?, ?)", row.customer_name, row.email, row.signup_date, row.loyalty_score)
            conn.commit()
    finally:
        pass
 
def insert_interaction_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create Customer DataFrame from Interaction_Data.csv
        Customer_df = pd.read_csv("CMR_PROJECT\\Interaction_Data.csv")
        # Insert DataFrame into SQL Server
        for index, row in Customer_df.iterrows():
            # Convert date string to datetime object if needed
            interaction_date = datetime.strptime(row['interaction_date'], '%d-%m-%Y')  # Adjust format as per your CSV
            # Execute SQL query with parameters as a tuple
            cursor.execute("INSERT INTO Interaction (customer_id, interaction_date, channel, subject, response_time_minutes) VALUES (?, ?, ?, ?, ?)",
                           (row['customer_id'], interaction_date, row['channel'], row['subject'], row['response_time_minutes']))
            conn.commit()
    except Exception as e:
        print(f"Error inserting data: {str(e)}")
    finally:
        pass


def insert_marketing_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        Marketing_df = pd.read_csv("CMR_PROJECT\\Marketing_Campaign_Data.csv")
        for index, row in Marketing_df.iterrows():
            start_date = datetime.strptime(row['start_date'], '%d-%m-%Y').date()
            end_date = datetime.strptime(row['end_date'], '%d-%m-%Y').date()
            cursor.execute("INSERT INTO MarketingCampaign (campaign_name, start_date, end_date, budget, response_rate) VALUES (?, ?, ?, ?, ?)",
                           (row['campaign_name'], start_date, end_date, row['budget'], row['response_rate']))
            conn.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {str(e)}")
    finally:
        cursor.close()
        conn.close()


def insert_product_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create Customer DataFrame from Customer_Data.csv
        Customer_df = pd.read_csv("CMR_PROJECT\\Product.csv")

        # Insert DataFrame into SQL Server:
        for index, row in Customer_df.iterrows():
            cursor.execute("INSERT INTO Product (product_name,product_price,description) VALUES ( ?, ?, ?)", row.product_name,row.product_price,row.description)
            conn.commit()
    finally:
        pass


def insert_sales_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        Sales_df = pd.read_csv("CMR_PROJECT\\Sales_Data.csv")
        for index, row in Sales_df.iterrows():
            sale_date = datetime.strptime(row['sale_date'], '%d-%m-%Y').date()
            cursor.execute("INSERT INTO Sales (customer_id, product_id, sale_date, sale_amount) VALUES (?, ?, ?, ?)",
                           (row['customer_id'], row['product_id'], sale_date, row['sale_amount']))
            conn.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {str(e)}")
    finally:
        pass


def insert_support_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        support_df = pd.read_csv("CMR_PROJECT\\Support_Tickets_Data.csv")
        for index, row in support_df.iterrows():
            issue_date = datetime.strptime(row['issue_date'], '%d-%m-%Y').date()
            cursor.execute("INSERT INTO SupportTicket (customer_id, issue_date, issue_type, resolution_time_hours) VALUES (?, ?, ?, ?)",
                           (row['customer_id'], issue_date, row['issue_type'], row['resolution_time_hours']))
            conn.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {str(e)}")
    finally:
        pass

insert_customer_data()

insert_interaction_data()

insert_marketing_data()

insert_product_data()

insert_sales_data()

insert_support_data()

if __name__ == '__main__':
    app.run(debug=True)
