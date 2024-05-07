from database import close_database

def cleanup():
    print("Cleaning up resources!")
    close_database()