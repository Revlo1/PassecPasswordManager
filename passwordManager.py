from dbconnect import usersTable, passwordsTable
from utils import hashPass, checkPass, passStrengthTester, checkPwnedPass, generatePass, checkPwnedEmail, getEmail, encryptData, decryptData

def passecMain(username, userID):
    while True:
        print(f"\n\n\n\nPassec Password Manager - Logged in as {username}, {userID}")
        
        print("\nWhat would you like to do?\n"
        "\n1. Retrieve all passwords"
        "\n2. Store a new password"
        "\n3. Edit a stored password"
        "\n4. Have I been PWNED? - Email"
        "\n5. Have I been PWNED? - Password"
        "\n6. General Security Check"
        "\n7. Logout")
        try:
            menuValue = int(input("Input Value Here: "))
        except ValueError:
            print("Invalid Option")
            continue

        match menuValue:
            case 1:
                getPass(userID)
            case 2:
                storePass(userID)
            case 3:
                editPass(userID)
            case 4:
                userEmail = getEmail(userID)
                if userEmail:
                    checkPwnedEmail(userEmail)
            case 5:
                password = input("Retype your password for security reasons: ")
                if checkPass(username, password):
                    print(checkPwnedPass(password))
                else:
                    print("Password incorrect")
            case 6:
                print("Work in progress")
                genSecCheck(userID)
                #generalSecurityCheckFunction - all passwords for breach and strength check
            case 7:
                print("Logging out...")
                break
            case _: #if value is outwith specified options
                print("Invalid Option")

def getPass(userID):
    dataset = passwordsTable.find({"userID": userID})

    for data in dataset:
        plainPass = decryptData(data['serPass'])
        print(f"Service: {data['service']}, Username: {data['username']}, Password: {plainPass}")

def editPass(userID):
    print("Input the service in which you would like to edit the password")
    inService = input("Service name: ")
    data = passwordsTable.find_one({"userID": userID, "service": inService})
    if not data or inService == "":
        print("Service not found in saved passwords")
        return False

    print("Now enter a new password, if you want us to automatically generate a strong one then leave the field empty")
    newPass = input("Enter a new password: ")

    
    if newPass == "":
        newPass = generatePass(16)
        print(newPass)
    

    encryptedPass = encryptData(newPass)
    hashedPass = hashPass(newPass)
    newData = {"$set": {"serPass": encryptedPass, "hashedPass": hashedPass}}
    
    passwordsTable.update_one({"userID": userID, "service": inService}, newData)

    print("Password successfully updated")
    return True

def storePass(userID):
    service = input("Service: ")
    serUser = input("Username: ")
    serPass = input("Password: ")

    hashedPass = hashPass(serPass) #use hashed pass to check for dupes as encryption is not consistent

    if passwordsTable.find_one({"userID": userID, "username": serUser, "service": service, "hashedPass": hashedPass}):
        print("Password already saved")
        return False
    
    serData = {"userID": userID, "service": service, "username": serUser, "serPass": encryptData(serPass), "hashedPass": hashedPass} 
    passwordsTable.insert_one(serData)
    print("Password Successfully saved")
    return True


def genSecCheck(userID):
    print("work in progress")

    dataset = passwordsTable.find({"userID": userID})
    i = 1
    for data in dataset:
        plainPass = decryptData(data['serPass'])
        service = data['service']
        print(f"\n{i}. {service}: {checkPwnedPass(plainPass)}")
        print("-Password Flaws-")
        passVal = passStrengthTester(plainPass)
        if passVal:
            print("Password is secure")
        i+=1

