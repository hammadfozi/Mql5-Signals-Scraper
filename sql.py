import pypyodbc


def init_db():
    db = pypyodbc.connect('Driver={SQL Server};Server=localhost\SQLEXPRESS; Database=master;Trusted_Connection=True;',
                          autocommit=True)

    sql_command = "Create Database test"
    execute_no_reply_command(db, sql_command)

    execute_no_reply_command(db, sql_command="CREATE TABLE Positions (DateTime varchar(18), Type varchar(4), "
                                                 "Volume float(3), Symbol varchar(10), Price float(6), SL float(6), "
                                                 "TP float(6), Price2 float(6), Commission float(6), Swap float(3), "
                                                 "Profit float(4) )")
    execute_no_reply_command(db, sql_command="CREATE TABLE History (DateTime varchar(18), Type varchar(4), "
                                                 "Volume float(3), Symbol varchar(10), Price float(6), SL float(6), "
                                                 "TP float(6), Time varchar(18), Price2 float(6), Commission float(6), "
                                                 "Swap float(3), Profit float(4), Comment varchar(150) )")


def execute_no_reply_command(db, sql_command):
    try:
        cursor = db.cursor()
        cursor.execute(sql_command)
        db.commit()
    except pypyodbc.Error as e:
        if str(e.args[0] == "42S01"):
            print("ERROR: Table already exists")


def execute_insertion(db, table_name, values):
    cursor = db.cursor()
    sql_command = ""

    if table_name is "positions":
        sql_command = "INSERT INTO Positions (DateTime, Type, Volume, Symbol, Price, SL, TP, Price2, Commission, " \
                      "Swap, Profit) VALUES (?,?,?,?,?,?,?,?,?,?,?) "
    elif table_name is "history":
        sql_command = "INSERT INTO History (DateTime, Type, Volume, Symbol, Price, SL, TP, Time, Price2, Commission, "\
                                                 "Swap, Profit, Comment) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) "

    cursor.execute(sql_command, values)
    db.commit()
