import mysql.connector

# Establishing database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="votes_db"
)
mycursor = mydb.cursor()

# Function to insert candidate data
def insert_candidate(candidate_name):
    sql_insert_candidate = "INSERT INTO candidates (candidate_name) VALUES (%s)"
    mycursor.execute(sql_insert_candidate, (candidate_name,))
    mydb.commit()
    print(f"Candidate {candidate_name} added successfully")

# Function to view all candidates
def view_candidates():
    mycursor.execute("SELECT * FROM candidates")
    candidates = mycursor.fetchall()
    if candidates:
        print("List of Candidates:")
        for candidate in candidates:
            print(f"Candidate ID: {candidate[0]}, Candidate Name: {candidate[1]}")
    else:
        print("No candidates found")

# Function to record a vote
def record_vote(candidate_id):
    sql_check_candidate = "SELECT * FROM votes WHERE candidate_id = %s"
    mycursor.execute(sql_check_candidate, (candidate_id,))
    candidate_vote = mycursor.fetchone()

    if candidate_vote:
        # Update existing candidate's vote count
        vote_count = candidate_vote[2] + 1  # Index 2 is vote_count in the table
        sql_update_vote = "UPDATE votes SET vote_count = %s WHERE candidate_id = %s"
        mycursor.execute(sql_update_vote, (vote_count, candidate_id))
    else:
        # Insert new candidate vote with initial count
        sql_insert_vote = "INSERT INTO votes (candidate_id, vote_count) VALUES (%s, %s)"
        mycursor.execute(sql_insert_vote, (candidate_id, 1))

    mydb.commit()
    print(f"Vote recorded successfully for Candidate ID: {candidate_id}")

# Function to view vote counts for all candidates
def view_vote_counts():
    mycursor.execute("SELECT c.candidate_name, COALESCE(v.vote_count, 0) AS vote_count \
                      FROM candidates c LEFT JOIN votes v ON c.candidate_id = v.candidate_id")
    vote_results = mycursor.fetchall()
    if vote_results:
        print("Candidate Vote Counts:")
        for candidate in vote_results:
            print(f"Candidate: {candidate[0]}, Votes: {candidate[1]}")
    else:
        print("No votes recorded yet")

# Example usage:
while True:
    print("\n--- Election Management System Menu ---")
    print("1. Add Candidate")
    print("2. View Candidates")
    print("3. Record Vote")
    print("4. View Vote Counts")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        candidate_name = input("Enter candidate name: ")
        insert_candidate(candidate_name)
    
    elif choice == '2':
        view_candidates()
    
    elif choice == '3':
        view_candidates()
        candidate_id = int(input("Enter candidate ID to record vote: "))
        record_vote(candidate_id)
    
    elif choice == '4':
        view_vote_counts()
    
    elif choice == '5':
        print("Exiting...")
        break
    
    else:
        print("Invalid choice. Please enter a number from 1 to 5.")

# Close the cursor and database connection
mycursor.close()
mydb.close()
