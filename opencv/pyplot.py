import mysql.connector
import matplotlib.pyplot as plt

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="evgeny",
    password="253321",
    database="OPEN_CV"
)

# Create a cursor for executing SQL queries
cursor = conn.cursor()

def convert_data(dir):    
    # Query the data from the table and sort by the "date" column in ascending order
    query = f"SELECT date FROM nagaevo_counter WHERE direction = {dir} ORDER BY date ASC"
    cursor.execute(query)

    # Fetch all the column values
    dates = [row[0] for row in cursor]

    modified_dates = []
    characters = []
    characters_mod = []
    for string in dates:
        #splitting string into chars
        for char in string:
            characters.append(char)

        #selecting only August 1st (01.08)
        if characters[5] == '8':
            #deleting year month day and seconds
            hour = int(f'{characters[8]}{characters[9]}')
            minute = int(f'{characters[10]}{characters[11]}')
            #converting to minutes only format (24h = 1440 min)
            total_min = (hour*60) + minute
            #characters_mod.append(total_min)??????????????????????????
            #print(characters_mod)
            modified_dates.append(total_min)
            characters_mod = []
        characters = []
    print(len(modified_dates), dir)

    #counting detections per 20 min
    delta = 0
    counter = []
    splitted_dates = []

    for i in modified_dates:
        if delta <= i < (delta + 20):
            counter.append(i)

        else:
            splitted_dates.append(counter)
            counter = []
            counter.append(i)
            delta = delta + 20

    #print(splitted_dates)
    twenty_min_margin = []
    for i in splitted_dates:
        twenty_min_margin.append(len(i))
    print(twenty_min_margin)
    print(len(twenty_min_margin))
    return twenty_min_margin



#Creating time line
timeline = []
for i in range(23):
    timeline.append(i)

print(timeline)
print(len(timeline))

# Plot the chart using pyplot
plt.plot(convert_data(1), 'o-')
plt.plot(convert_data(-1), 'o-')
plt.xlabel("Hours")
plt.ylabel("Number of cars per 20 min")
plt.title("Traffic Chart")
plt.xticks(range(0, len(convert_data(1)), 3), timeline)  # Set x-ticks at every third position, with labels from time
plt.tight_layout()
#plt.show()
# Save the chart as an image file
plt.savefig("chart.png")

# Close the cursor and database connection
cursor.close()
conn.close()

