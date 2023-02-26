import flask
#SDID 1892523 Raahima Ahmed 
from flask import jsonify
from flask import request
from sql import create_connection, execute_read_query,execute_query
from datetime import datetime


app = flask.Flask(__name__)
app.config["DEBUG"] = True   #Setting up initial application. 

# Define the API endpoints
#Get Routes 
@app.route('/', methods=['GET'])
def get_snowboard():
    return "<h1>THE APP WORKS<h1>"  #Tests if API init works. [It does]

@app.route('/api/snowboard/all',methods=['GET']) #Creates url route to get all the snowboard info.
def api_all():
    snowboard = [] #This list will house the key/value pairs of snowboard information, this will be used for the GET methods
    conn = create_con('hw1cis3368.c8aubdep9gnu.us-east-2.rds.amazonaws.com', 'admin', 'Passward1!', 'hw1cis3368')
    sql = "SELECT * FROM snowboard"
    snow = execute_read_query(conn,sql)
    for board in snow:  #Add board to 'snowboard' list
        snowboard.append(board) 
    return jsonify(snowboard) #Turns the info in the snowboard list into a readable JSON format.

@app.route('/api/snowboard',methods=['GET']) #This gets a specific snowboard by ID with the URL looking like this: http://127.0.0.1:5000/api/snowboard?id=[ID]
def api_by_id():
    snowboard = [] #This list will house the key/value pairs of snowboard information, this will be used for the GET methods
    conn = create_con('hw1cis3368.c8aubdep9gnu.us-east-2.rds.amazonaws.com', 'admin', 'Passward1!', 'hw1cis3368')
    sql = "SELECT * FROM snow"
    snow = execute_read_query(conn,sql)
    for board in snow:  #Add snowboard to 'snowboard' list
        snowboard.append(board) 

    if 'id' in request.args:
        id= int(request.args['id']) #If the id in the request arguement matches an id in the DB the id will be compared in a for loop later on. 
    else:
        return "NO SNOWBOARD PARAM GIVEN" #If not the api wil return this.
    results = [] #This is where the results will be placed.
    for snowboard in snowboards: #This for loop parses through  the snowboard list. 
        if snowboard['id'] == id:
            results.append(snowboard) #Adds the snowboard info into the results list if the id in the request matches the id in the snowboard row in the snow table.
    return jsonify(results) #Turns the results list into a JSON.

#--------THE POST,PUT AND DELETE METHODS WILL USE THE LOG TABLE --------

@app.route('/api/snowboard', methods=['POST'])
def create_snowboard():
    conn = create_connection('hw1cis3368.c8aubdep9gnu.us-east-2.rds.amazonaws.com', 'admin', 'Passward1!', 'hw1cis3368')
    request_data = request.get_json() #Allow's user to add new json key value pairs to api.
    n_board_boardtype = request_data['boardtype'] #Adds boardtype (used later in json append)
    n_board_brand = request_data['brand'] #Adds brand (used later in json append)
    n_board_msrp = request_data['msrp'] #Adds msrp (used later in json append)
    n_board_size= request_data['size'] #Adds size(used later in json append)
    # THIS NEXT BLOCK WITH THE FUNCTION WILL ADD IT TO THE DB AND JSON
    add_sql = f"INSERT INTO snowboard VALUES (id,'{n_board_board}','{n_board_brand}','{n_board_msrp}',{n_board_size})" #Adds new record to DB with JSON post
    execute_query(conn,add_sql)
    new_board_sql = "SELECT * FROM snowboard ORDER BY id DESC LIMIT 0,1" #Fetches most recenty created record in the table
    new_board = execute_read_query(conn,new_board_sql)
    new_id = new_board[0]['id'] #Gets the new id of the recently created record.
    n_log_SQL = f"INSERT INTO log VALUES(id,CURRENT_TIMESTAMP,{new_id},'NEW {n_board_snowboard} ADDED')" #Adds change to log table. The time stamp will return a GMT time, because the server is in Phoenix.
    execute_query(conn,n_log_SQL)

    return "ADDED board"




@app.route('/api/board',methods=['PUT'])
def update_boardmal():
    if 'id' in request.args:
       conn = create_connection('hw1cis3368.c8aubdep9gnu.us-east-2.rds.amazonaws.com', 'admin', 'Passward1!', 'hw1cis3368')
       request_data = request.get_json() #Allow's user to add new json key value pairs to api.
       n_board_boardtype = request_data['boardtype'] #Adds boardtype (used later in json append)
       n_board_brand = request_data['brand'] #Adds brand (used later in json append)
       n_board_msrp = request_data['msrp'] #Adds msrp (used later in json append)
       n_board_size= request_data['size'] #Adds size(used later in json append)
       # THIS NEXT BLOCK WITH THE FUNCTION WILL ADD IT TO THE DB AND JSON
       update_board_sql = f"UPDATE snow SET boardtype='{u_board_boardtype}', band='{u_board_brand}', msrp='{u_board_msrp}', size={u_board_size}' WHERE id={id};"
       ex_update = execute_query(conn,update_board_sql) #Executes change in the DB
       #LOG TABLE CHANGE BELOW THIS
       u_log_SQL = f"INSERT INTO log VALUES(id,CURRENT_TIMESTAMP,{id},'{u_board_boardtype} WITH ID:{id} UPDATED')"
       execute_query(conn,u_log_SQL)
    else:
        return 'NO ID GIVEN TO UPDATE'

    return 'SNOWBOARD UPDATED'



@app.route('/api/animal',methods=['DELETE'])
def delete_animal():
    conn = create_connection('hw1cis3368.c8aubdep9gnu.us-east-2.rds.amazonaws.com', 'admin', 'Passward1!', 'hw1cis3368')
    if 'id' in request.args:
         id=int(request.args['id']) #Allows user to use ID as a parameter. 
    else:
        return "NO ID GIVEN TO DELETE"
    delete_sql = f"DELETE FROM snow WHERE id={id}" #SQL code to delete record in the DB
    execute_query(conn,delete_sql)
#LOG TABLE CHANGE BELOW THIS
    d_log_SQL = f"INSERT INTO log VALUES(id,CURRENT_TIMESTAMP,{id},'SNOWBOARD WITH ID:{id} DELETED')" #Adds change to the log table
    execute_query(conn,d_log_SQL)
    return "SNOWBOARD DELETED"




