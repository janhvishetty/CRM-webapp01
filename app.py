from flask import Flask, request, jsonify,render_template
import pyodbc

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = pyodbc.connect(
        # 'DRIVER={ODBC Driver 17 for SQL Server};'
        # 'SERVER=eldsserver.database.windows.net;'
        # 'DATABASE=eldsdb;'
        # 'UID=elds;'
        # 'PWD=eld@1234'
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=arabhiprojectserver.database.windows.net;'
        'DATABASE=crmdatabase;'
        'UID=arabhiserver;'
        'PWD=Arabhi1118'
    )
    return conn


@app.route('/')
def home():
   return render_template('management.html')

@app.route('/back')
def back():
   return render_template('employee_dashboard.html')

#LOGIN PAGE CHECKING--------------------------------------------------------
@app.route('/check_employee', methods=['POST'])
def check_employee():
    employee_email = request.form.get("employee_email")
    employee_password = request.form.get("employee_password")
    cur =get_db_connection()
    cursor = cur.cursor() 
    try:
        cursor.execute("SELECT * FROM Employees WHERE employee_email = ?", (employee_email))
        row = cursor.fetchone()
        if row:
            if row[3]==employee_password:
                return jsonify({'success': True,'msg': 'User login successful'})
            else:
                return jsonify({'success': False,'msg': 'Wrong password'})
            print(row)
        else:
            return jsonify({'success': False,'msg': 'User with this email doesnot exist'})
        
    except Exception as e:
        # Handle exceptions or errors
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
    finally:
        pass
@app.route('/employee_dashboard')
def emp_dashboard():
    return render_template('employee_dashboard.html')

#CUSTOMER APIS-----------------------------------------------------------------------

#inserting customer

@app.route('/add_customer')
def addcust():
   return render_template('createcustomer.html')

@app.route('/customers', methods=['POST'])
def register_customer():
    try:
        customer_name=request.form.get('name')
        email=request.form.get('email')
        signup_date=request.form.get('date')
        #loyalty_score=request.form.get('score')
        conn = get_db_connection()
        cursor = conn.cursor()
        if customer_name != "" and email!= "" and signup_date != "":
            cursor.execute("insert into Customer (customer_name,email,signup_date) values(?,?,?)",(customer_name,email,signup_date))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True,'message': 'Customer registered successfully'}), 201
        else:
            return jsonify({'success': False,'message': 'Please fill the form'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#updating customer
@app.route('/update_customer')
def updatecust():
   return render_template('updatecust.html')
@app.route('/update_customers_details', methods=['POST'])
def update_customer():
    customer_id=request.form.get('Cust_Id')
    Update_field=request.form.get('Update Field')
    Update_value=request.form.get('Update Value')

    conn = get_db_connection()
    cursor = conn.cursor()
    if(Update_field=='email'):
        cursor.execute("update Customer set email=? where customer_id=?",(Update_value,customer_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Customer email updated successfully'}), 201
    elif(Update_field=='loyalty_score'):
        cursor.execute("update Customer set loyalty_score=? where customer_id=?", (Update_value, customer_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Customer loyalty score updated successfully'}), 201
    elif(Update_field=='customer_name'):
        cursor.execute("update Customer set customer_name=? where customer_id=?", (Update_value, customer_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Customer Name updated successfully'}), 201
    else:
        return jsonify({'success': False,'message': 'Please fill the form'})
    cursor.close()
    conn.close()

#viewing customer
@app.route('/get_customer')
def get_cust():
   return render_template('get_detailscustomers.html')


@app.route('/view_customers', methods=['GET'])
def get_customers():
    try:
        # Extract query parameters
        filter_by = request.args.get('filter_by')
        value = request.args.get('value')

        # Construct SQL query based on the provided parameters
        query = """
            SELECT *
            FROM Customer
            WHERE 
        """
        params = []

        if filter_by == 'customer_id':
            query += " customer_id = ?"
            params.append(value)
        elif filter_by == 'signup_date':
            query += "signup_date = ?"
            params.append(value)
        elif filter_by == 'all':
            # If 'all' is selected, fetch all interactions
            query = """
                SELECT *
                FROM Customer
            """
        elif filter_by == '--Please Select an Option--':
            query = ""
        else:
            pass
        # If no specific parameters provided, fetch all customers
        # if not any([filter_by, value]):
        #     query = """
        #         SELECT *
        #         FROM Customer
        #     """
        #     params = []

        # Establish connection and execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        # Fetch all rows from the query result
        customers = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Render customers.html template with customers data
        return render_template('show_customers.html', customers=customers)

    except Exception as e:
        return jsonify({'error': str(e)}), 500





# LOG INTERACTION APIS----------------------------------------------------------------
@app.route('/customer_interaction')
def add_interaction():
   return render_template('createinteraction.html')


@app.route('/interactions', methods=['POST'])
def log_interaction():
    try:
        customer_id = request.form.get('custid')
        interaction_date = request.form.get('date')
        channel = request.form.get('channel')
        subject = request.form.get('subj')
        response_time_minutes = request.form.get('restime')

        conn = get_db_connection()
        cursor = conn.cursor()
        if customer_id!= "" and interaction_date!="" and channel!="" and subject!="" and response_time_minutes!="":
            cursor.execute('''insert into Interaction (customer_id,interaction_date,channel,subject,response_time_minutes)
            values(?,?,?,?,?)''',
                        (customer_id, interaction_date, channel, subject, response_time_minutes))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True,'message': 'Interaction logged successfully'}), 201
        else:
            return jsonify({'success': False,'message': 'Please fill the form'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#view Interaction

@app.route('/get_interaction')
def view_interaction():
   return render_template('give_detailsinteraction.html')


@app.route('/view_interactions', methods=['GET'])
def get_interactions():
    try:
        # Extract query parameters
        search_by = request.args.get('search_by')
        value = request.args.get('value')

        # Construct SQL query based on the provided parameters
        query = """
            SELECT interaction_id, customer_id, interaction_date, channel, subject, response_time_minutes
            FROM Interaction
            WHERE 
        """
        params = []

        # Add condition based on provided search_by parameter
        if search_by == 'customer_id':
            query += "customer_id = ?"
            params.append(value)
        elif search_by == 'interaction_id':
            query += "interaction_id = ?"
            params.append(value)
        elif search_by == 'channel':
            query += "channel = ?"
            params.append(value)
        elif search_by == 'all':
            # If 'all' is selected, fetch all interactions
            query = """
                SELECT *
                FROM Interaction
            """
        elif search_by == '--Please Select an Option--':
            query = ""
        else:
            pass

        # Establish connection and execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        # Fetch all rows from the query result
        interactions = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Render interactions.html template with interactions data
        return render_template('show_interactions.html', interactions=interactions)

    except Exception as e:
        return jsonify({'error': str(e)}), 500




#MARKETING CAMPAIGN APIS-----------------------------------------------------------

#inserting
@app.route('/marketing_campaign')
def add_campaign():
   return render_template('createcampaign.html')
@app.route('/campaigns', methods=['POST'])
def create_campaign():
    try:
        campaign_name=request.form.get('campname')
        start_date=request.form.get('startdate')
        end_date=request.form.get('enddate')
        budget=request.form.get('budget')
        response_rate=request.form.get('res_rate')
        conn = get_db_connection()
        cursor = conn.cursor()
        if campaign_name!="" and start_date!="" and end_date!="" and budget!="" and response_rate!="":
            cursor.execute('''insert into MarketingCampaign(campaign_name,
            start_date,end_date,budget,response_rate) 
            values(?,?,?,?,?)''',(campaign_name,start_date,end_date,budget,response_rate))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True,'message': 'Campaign created successfully'}), 201
        else:
            return jsonify({'success': False,'message': 'Please fill the form'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#updating
@app.route('/update_campaign')
def updatecamp():
   return render_template('updatecampaign.html')

@app.route('/update_campaign_details', methods=['POST'])
def update_campaign_details():
    campaign_id=request.form.get('Campaign_Id')
    Update_field=request.form.get('Update Field')
    Update_value=request.form.get('Update Value')
    #loyalty_score=request.form.get('score')
    conn = get_db_connection()
    cursor = conn.cursor()
    if(Update_field=='budget'):
        cursor.execute("update MarketingCampaign set budget=? where campaign_id=?",(Update_value,campaign_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Marketing Campaign details updated successfully'}), 201
    elif(Update_field=='response_rate'):
        cursor.execute("update MarketingCampaign set response_rate=? where customer_id=?", (Update_value, campaign_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Marketing Campaign details updated successfully'}), 201
    else:
        return jsonify({'success': False,'message': 'Please fill the form'})
    cursor.close()
    conn.close()


#viewing

@app.route('/get_campaign')
def get_camp():
   return render_template('get_detailscampaign.html')


@app.route('/view_campaigns', methods=['GET'])
def get_campaigns():
    try:
        # Extract query parameters
        search_by = request.args.get('search_by')
        value = request.args.get('value')

        # Construct SQL query based on the provided parameters
        query = """
            SELECT campaign_id, campaign_name, start_date, end_date, budget, response_rate
            FROM MarketingCampaign
            WHERE
        """
        params = []

        if search_by == 'campaign_id':
            query += "campaign_id = ?"
            params.append(value)
        elif search_by == 'campaign_name':
            query += "campaign_name = ?"
            params.append(value)
        elif search_by == 'start_date':
            query += "start_date = ?"
            params.append(value)
        elif search_by == 'end_date':
            query += "end_date = ?"
            params.append(value)
        elif search_by == 'all':
            query = """
                SELECT *
                FROM MarketingCampaign
            """
            params = []
        elif search_by == '--Please Select an Option--':
            query = ""
        else:
            pass
    
        # Establish connection and execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        # Fetch all rows from the query result
        campaigns = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Render campaigns.html template with campaigns data
        return render_template('show_campaigns.html', campaigns=campaigns)

    except Exception as e:
        return jsonify({'error': str(e)}), 500








#SUPPORT TICKETS APIS-------------------------------------------------------------

#inserting support tickets
@app.route('/support_tickets')
def add_ticket():
   return render_template('createticket.html')
@app.route('/support_tickets', methods=['POST'])
def create_support_ticket():
    try:
        customer_id=request.form.get('custid')
        issue_date=request.form.get('date')
        issue_type=request.form.get('type')
        resolution_time_hours=request.form.get('res_time')
        conn = get_db_connection()
        cursor = conn.cursor()
        if customer_id!="" and issue_date!="" and issue_type!= "" and resolution_time_hours!="":
            cursor.execute('''insert into SupportTicket
            (customer_id,issue_date,issue_type,
            resolution_time_hours) values(?,?,?,?)''',(customer_id,issue_date,issue_type,resolution_time_hours))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True,'message': 'Support ticket created successfully'}), 201
        else:
            return jsonify({'success': False,'message': 'Please fill the form'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#viewing support tickets

@app.route('/get_tickets')
def get_ticket():
   return render_template('get_detailsticket.html')


@app.route('/view_tickets', methods=['GET'])
def get_support_tickets():
    try:
        # Extract query parameters
        filter_by = request.args.get('filter_by')
        value = request.args.get('value')

        # Construct SQL query based on the provided parameters
        query = """
            SELECT ticket_id, customer_id, issue_date, issue_type, resolution_time_hours
            FROM SupportTicket
            WHERE 
        """
        params = []

        if filter_by == 'ticket_id':
            query += "ticket_id = ?"
            params.append(value)
        elif filter_by == 'customer_id':
            query += "customer_id = ?"
            params.append(value)
        elif filter_by == 'issue_date':
            query += "issue_date = ?"
            params.append(value)
        elif filter_by == 'issue_type':
            query += "issue_type = ?"
            params.append(value)
        elif filter_by == 'all':
            # If 'all' is selected, fetch all interactions
            query = """
                SELECT *
                FROM SupportTicket
            """
        elif filter_by == '--Please Select an Option--':
            query = ""
        else:
            pass
        
        # If no specific parameters provided, fetch all support tickets
        # if not any([filter_by, value]):
        #     query = """
        #         SELECT ticket_id, customer_id, issue_date, issue_type, resolution_time_hours
        #         FROM SupportTicket
        #     """
        #     params = []

        # Establish connection and execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        # Fetch all rows from the query result
        support_tickets = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Render support_tickets.html template with support ticket data
        return render_template('show_tickets.html', support_tickets=support_tickets)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



#SALES APIS---------------------------------------------------------------

@app.route('/create_sales')
def add_sales():
   return render_template('createsales.html')
@app.route('/salesentry', methods=['POST'])
def create_sales_entry():
    try:
        customer_id=request.form.get('custid')
        product_id=request.form.get('pdid')
        sale_date=request.form.get('date')
        sale_amount=request.form.get('amount')
        conn = get_db_connection()
        cursor = conn.cursor()
        if customer_id!="" and product_id!="" and sale_date!="" and sale_amount!="":
            cursor.execute('''insert into Sales
            (customer_id,product_id,sale_date,
            sale_amount) values(?,?,?,?)''',(customer_id,product_id,sale_date,sale_amount))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True,'message': 'Sales entries created successfully'}), 201
        else:
            return jsonify({'success': False,'message': 'Please fill the form'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
#updating sales

@app.route('/update_sales')
def updatesales():
   return render_template('updatesales.html')

@app.route('/update_sales_details', methods=['POST'])
def update_sales_details():
    sale_id=request.form.get('Sale_Id')
    Update_field=request.form.get('Update Field')
    Update_value=request.form.get('Update Value')

    conn = get_db_connection()
    cursor = conn.cursor()
    if(Update_field=='sale_amount'):
        cursor.execute("update Sales set sale_amount=? where sale_id=?",(Update_value,sale_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Product details updated successfully'}), 201
    elif(Update_field=='product_id'):
        cursor.execute("update Sales set product_id=? where sale_id=?", (Update_value, sale_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Product details updated successfully'}), 201
    else:
        return jsonify({'success': False,'message': 'Please fill the form'})
    cursor.close()
    conn.close()


#viewing sales

@app.route('/get_sales')
def view_sales():
   return render_template('get_detailssales.html')


@app.route('/view_sales', methods=['GET'])
def get_sales():
    try:
        # Extract query parameters
        search_by = request.args.get('search_by')
        value = request.args.get('value')

        # Construct SQL query based on the provided parameters
        query = """
            SELECT sale_id, customer_id, product_id, sale_date, sale_amount
            FROM Sales
            WHERE 
        """
        params = []

        if search_by == 'customer_id':
            query += "customer_id = ?"
            params.append(value)
        elif search_by == 'product_id':
            query += "product_id = ?"
            params.append(value)
        elif search_by == 'sale_date':
            query += "sale_date = ?"
            params.append(value)
        elif search_by == 'all':
            # If 'all' is selected, fetch all interactions
            query = """
                SELECT *
                FROM Sales
            """
        elif search_by == '--Please Select an Option--':
            query = ""
        else:
            pass
        # elif search_by == 'all':
        #     query = """
        #         SELECT *
        #         FROM Sales
        #     """
        #     params = []

        # Establish connection and execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        # Fetch all rows from the query result
        sales = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Render sales.html template with sales data
        return render_template('show_sales.html', sales=sales)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#PRODUCT APIS---------------------------------------------------------------------------

#inserting product
@app.route('/create_product')
def add_product():
   return render_template('createproduct.html')
@app.route('/productsentry', methods=['POST'])
def create_products_entry():
    try:
        product_name=request.form.get('name')
        product_price=request.form.get('price')
        description=request.form.get('des')
        conn = get_db_connection()
        cursor = conn.cursor()
        if product_name!="" and product_price!="" and description!="":
            cursor.execute('''insert into Product
            (product_name,product_price,
            description) values(?,?,?)''',(product_name,product_price,description))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'success': True,'message': 'Product entries created successfully'}), 201
        else:
            return jsonify({'success': False,'message': 'Please fill the form'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#updating product
@app.route('/update_product')
def updateprod():
   return render_template('updateproduct.html')

@app.route('/update_product_details', methods=['POST'])
def update_product_details():
    product_id=request.form.get('Product_Id')
    Update_field=request.form.get('Update Field')
    Update_value=request.form.get('Update Value')

    conn = get_db_connection()
    cursor = conn.cursor()
    if(Update_field=='product_price'):
        cursor.execute("update Product set product_price=? where product_id=?",(Update_value,product_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Product details updated successfully'}), 201
    elif(Update_field=='description'):
        cursor.execute("update Product set description=? where product_id=?", (Update_value, product_id))
        conn.commit()
        return jsonify({'success': True,'message': 'Product details updated successfully'}), 201
    else:
        return jsonify({'success': False,'message': 'Please fill the form'})
    cursor.close()
    conn.close()
    

#viewing product

@app.route('/get_product')
def view_prod():
   return render_template('give_detailsproducts.html')


@app.route('/view_products', methods=['GET'])
def get_products():
    try:
        # Extract query parameters
        search_by = request.args.get('search_by')
        value = request.args.get('value')

        # Construct SQL query based on the provided parameters
        query = """
            SELECT product_id, product_name, product_price, description
            FROM Product
            WHERE 
        """
        params = []

        if search_by == 'product_name':
            query += "product_name = ?"
            params.append(value)
        elif search_by == 'all':
            query = """
                SELECT product_id, product_name, product_price, description
                FROM Product
            """
        elif search_by == 'description':
            query += "description = ?"
            params.append(value)
        elif search_by == 'all':
            # If 'all' is selected, fetch all interactions
            query = """
                SELECT *
                FROM Product
            """
        elif search_by == '--Please Select an Option--':
            query = ""
        else:
            pass
        

        # Establish connection and execute query
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        # Fetch all rows from the query result
        products = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Render products.html template with products data
        return render_template('show_products.html', products=products)

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)