import sqlite3

def ADD(filePath):
    # Open DB
    db = sqlite3.connect(str(filePath))
    db_cur = db.cursor()
    
    # Quick explanation on what to do
    print("Please supply the required information for the new sign")
    print("NOTE: The search term must be in the form of a regular expression")
    print("EXAMPLE: r'\\t22\\t'\n")
    
    # Get user input
    _searchTerm = input("Search Term: ")
    _goodCount = input("Good Count: ")
    _fairCount = input("Fair Count: ")
    
    # Insert into database
    db_cur.execute("INSERT INTO health(search_term, good_count, fair_count, count) VALUES (?, ?, ?, 0)",
                   (_searchTerm, _goodCount, _fairCount))
    
    # Commit changes
    db.commit()
    
    # Close DB
    db_cur.close()
    db.close()

def CHANGE(filePath, sign):
    # Open DB
    db = sqlite3.connect(str(filePath))
    db_cur = db.cursor()
    
    # Quick explanation on what to do
    print("Please supply the required information for sign " + sign)
    print("NOTE: The search term must be in the form of a regular expression")
    print("EXAMPLE: r'\\t22\\t'\n")
    
    # Get user input
    _searchTerm = input("Search Term: ")
    _goodCount = input("Good Count: ")
    _fairCount = input("Fair Count: ")
    
    # Update database table
    db_cur.execute("UPDATE health SET search_term = ?, good_count = ?, fair_count = ? WHERE sign = ?",
                   (_searchTerm, _goodCount, _fairCount, sign))
    
    # Commit changes
    db.commit()
    
    # Close DB
    db_cur.close()
    db.close()

#def DELETE(sign):
    ## Open DB
    #db = sqlite3.connect('health.db')
    #db_cur = db.cursor()
    
    ## Quick explanation of what is happening
    #print("Deleteing sign " + sign)
    
    ## Update database
    #db_cur.execute("DELETE FROM health WHERE sign = ?", sign)
    
    ## Commit changes
    #db.commit()
    
    ## Close DB
    #db_cur.close()
    #db.close()
