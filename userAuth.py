from dbconnect import usersTable
from utils import hashPass, passStrengthTester, generatePass
import random
import smtplib
import ssl
import os

#environment variables
appEmail = os.getenv("passecEmail")
appPass = os.getenv("passecEmailPass")

#============email verification and password reset======================
def genVerifyCode(): #generate recovery code
    code = ""
    for i in range(6):
        randNum = random.randint(48, 57)
        code += chr(randNum)
        
    return code

def sendEmail(userEmail, code):
    subject = "Passec Password Manager Code"
    body = f"Your code is: {code}\nEnter the code onto the application"
    message = f"Subject: {subject}\n\n{body}"
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            #print("Logging in")
            server.login(appEmail, appPass)
            #print("Sending email")
            server.sendmail(appEmail, userEmail, message)
            #print("Email sent")
    except Exception as e:
        print("Error sending email: ", e)

def verifyEmail(userEmail):
    code = genVerifyCode()
    sendEmail(userEmail, code)

    attempts = 0
    while attempts < 3:
        inputCode = input("Input the verification code sent to your email address: ")
        if inputCode == code:
            print("Email Verified!")
            return True
        else:
            attempts += 1
            print("Incorrect code, try again")

    print("Verifcation failed, too many incorrect codes")
    return False


def recoverPassword():
    userEmail = input("Email address: ")
    if not usersTable.find_one({"email": userEmail}):
        print("Email address not found")
        return False
    
    code = genVerifyCode()
    sendEmail(userEmail, code)

    attempts = 0
    while attempts < 3:
        inputCode = input("Input the recovery code sent to your email address: ")
        if inputCode == code:
            print("Success, now enter a new password")
            print("PassecManager requires the user to have a strong password in order to securely hold the other passwords.\n---==<{Password Policy}>==---\n1. Must be 8 or more Characters long\n2. Must have at least 1 special character (!?@#%)\n3. Must contain at least one uppercase character")   
            password = None
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
            usersTable.update_one(
                {"email": userEmail},
                {"$set": {"password": hashPass(password)}}
            )
            print("Password successfully updated")

            return True
        else:
            attempts += 1
            print("Incorrect code, try again")

    print("Verifcation failed, too many incorrect codes")
    return False


#=========================register and login functions========================
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
            if verifyEmail(tempEmail):
                emailAddress = tempEmail
            else:
                print("Invalid Email")

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
    