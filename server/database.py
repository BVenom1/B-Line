'''
This is the file where the database is set up.
'''

# Connect to the PostgreSQL database using credentials.json
import os, json

credentials = {}
cred_file_loc = os.path.join(os.path.dirname(__file__), "credentials.json")
with open(cred_file_loc, "r", encoding="utf-8") as file:
    credentials = json.load(file)

# main function for testing
if __name__ == "__main__":
    print(credentials)