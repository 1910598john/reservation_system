import connection as conn

mycursor = conn.mydb.cursor()
room_id = 101
rooms = 60
sql = "INSERT INTO rooms (room_id, type, capacity, check_in_date, check_out_date, availability) VALUES (%s, %s, %s, %s, %s, %s)"
for x in range(rooms):
    if x < 10:
        val = (room_id, "STANDARD", "SINGLE", "mm/dd/yy", "mm/dd/yy", "Available")
    elif x >= 10 and x < 20:
        val = (room_id, "STANDARD", "DOUBLE", "mm/dd/yy", "mm/dd/yy", "Available")
    elif x >= 20 and x < 30:
        val = (room_id, "ECONOMY", "SINGLE", "mm/dd/yy", "mm/dd/yy", "Available")
    elif x >= 30 and x < 40:
        val = (room_id, "ECONOMY", "DOUBLE", "mm/dd/yy", "mm/dd/yy", "Available")
    elif x >= 40 and x < 50:
        val = (room_id, "VIP", "SINGLE", "mm/dd/yy", "mm/dd/yy", "Available")
    elif x >= 50 and x < 60:
        val = (room_id, "VIP", "DOUBLE", "mm/dd/yy", "mm/dd/yy", "Available")
        
    room_id += 1
    mycursor.execute(sql, val)
    conn.mydb.commit()
