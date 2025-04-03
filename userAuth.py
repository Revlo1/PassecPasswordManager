from dbconnect import usersTable
from utils import hashPass, passStrengthTester, generatePass


#add checks for whether reg details are secure (dont need it for logging in if inputs are sanitized on reg)
def register():
    username = None
    emailAddress = None
    password = None

    while username is None:
        tempUsername = input("Enter a username: ")
        if usersTable.find_one({"username": tempUsername}):
            print("Username already exists, try again.")
        else:
            username = tempUsername
    
    while emailAddress is None:
        tempEmail = input("Enter a valid email address: ")
        if usersTable.find_one({"email": tempEmail}):
            print("Email address already exists, try again.")
        else:
            emailAddress = tempEmail

    print("PassecManager requires the user to have a strong password in order to securely hold the other passwords.\n---==<{Password Policy}>==---\n1. Must be 8 or more Characters long\n2. Must have at least 1 special character (!?@#%)\n3. Must contain at least one uppercase character")   
    while password is None:
        
        print("Enter a new password, if you want us to automatically generate a strong one then leave the field empty")
        tempPassword = input("Enter a new password: ")
   
        if tempPassword == "":
            tempPassword = generatePass(16)
        
        if not passStrengthTester(tempPassword):
            print("Password not strong enough, follow the policy above.")
        else:
            password = tempPassword

    print(f"Save your password: {password}")

    userData = {"username": username, "email": emailAddress, "password": hashPass(password)}
    usersTable.insert_one(userData)
    print("Account successfully created")
    return True


def login():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    checkUser = usersTable.find_one({"username": username})

    if checkUser and checkUser["password"] == hashPass(password):
        userID = checkUser["_id"]
        print("Successfully Logged in")
        return username, userID
    else:
        print("Invalid details, try again.")
        return None, None
    