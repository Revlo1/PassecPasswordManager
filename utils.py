#from userAuth import checkPass
from dbconnect import usersTable, passwordsTable
from cryptography.fernet import Fernet
import hashlib 
import requests
import random

#Hashing/Encryption functions==================================================================================
def hashPass(password):
    return hashlib.sha256(password.encode()).hexdigest()

#one time use to generate and store key - maybe make it always check for file and auto generate if file doesnt exist
'''
def genKey():
    key = Fernet.generate_key() #use .env variable when improving security
    with open("secret.key", "wb") as keyFile:
        keyFile.write(key)

genKey()
'''

def loadKey():
    with open("secret.key", "rb") as keyFile:
        return keyFile.read()


key = loadKey()
cipher = Fernet(key)

def encryptData(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decryptData(data: str) -> str:
    return cipher.decrypt(data.encode()).decode()

#Password Functions=============================================================================================
def checkPwnedPass(password):
    #hashpassword
    hashedPass = hashlib.sha1(password.encode()).hexdigest().upper() #hash to sha1 - consists of 40 characters
    prefix, suffix = hashedPass[:5], hashedPass[5:] #prefix = first 5 characters, suffix = remaining 35 characters
    #send to api using first 5 chars of hash(prefix)
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url) #returns all hash suffixes (remaining characters in potential hashes NOT the final 5 chars as previously specified)

    if response.status_code == 200: #OK status
        hashes = response.text.splitlines() #split hashes into seperate lines in array
        for line in hashes: #loop through hashes
            hash_suffix, numberOfBreaches = line.split(":") #split at ":" (api returns hashes in the format of the hash_suffix:numberOfBreaches)
            if suffix == hash_suffix:
                return f"Password has been found in {numberOfBreaches} breaches"
        return "Password has not been found in breaches"
    else:
        return f"Error: {response.status_code}"

def checkPass(username, password):
    checkUser = usersTable.find_one({"username": username})

    if checkUser and checkUser["password"] == hashPass(password):
        return True
    else:
        return False
    
def checkAllPass(userID):
    dataset = passwordsTable.find({"userID": userID})
    i = 1
    for data in dataset:
        plainPass = decryptData(data['serPass'])
        print(f"{i}. {checkPwnedPass(plainPass)}")
        #print(f"Service: {data['service']}, Username: {data['username']}, Password: {plainPass}")

def generatePass(passLen):
    password = ""
    while password == "":
        for i in range(passLen):
            ranVal = random.randint(33, 126)
            password += chr(ranVal)

        if not passStrengthTester(password):
            password = ""

    return password

#Email Functions=============================================================================================
def formatData(data):
    varFound = data.get("found")
    sources = data.get("sources", [])
    
    nameArr = []
    dateArr = []

    for source in sources:
        nameArr.append(source["name"])
        dateArr.append(source["date"])

    if varFound > 0:
        print(f"Username or Email Address has been found in {varFound} breaches")
        print("----====(Breach-Details)====----")
        for i in range(len(nameArr)):
            print(f"{i+1}) Website: {nameArr[i]}, Date: {dateArr[i]}")
    else:
        print("Username or Email was not found in any breaches")

     
    

    return nameArr, dateArr
    # handle initial text (if success == True: continue)
    # then split domain and data into seperate arrays so that domain[i] and date[i] match
    # Structure - initial text - fields[ip2, address, dob, username, ip1, city, state, name, last_name, phone, ip, country, profile_name, password, zip, first_name, origin] - sources[name, date]
    # var = number of {} for raw text
    # nameArr[]*var, dateArr[]*var#

def checkPwnedEmail(userAcc):
    hashAcc = hashlib.sha256(userAcc.encode()).hexdigest()
    #print("Hash: " + hashAcc)
    response = requests.get(f'https://leakcheck.io/api/public?check={hashAcc}')

    if response.status_code == 200:
        #pprint.pprint(f"Response: {response.text}")
        #data = json.loads(response.text)
        formatData(response.json()) #sends json object to formatdata
    else:
        print (f"Error: {response.status_code}")

def getEmail(userID):
    checkEmail = usersTable.find_one({"_id": userID})

    if checkEmail:
        return checkEmail["email"]
    else:
        print("Error: could not find userID")
        return None
    
#string search function
#for uppercase get an ascii value for each char and check it is within a certain name
#returns true if password meets string search requirements and false if it doesnt
def stringSearch(password, passLen): 
    spChar = "!?@#%"
    spFlag = False #set true if special char found 
    uppercaseFlag = False #set true if uppercase char found

    for i in range(passLen):
        if 'A' <= password[i] <= 'Z':
            uppercaseFlag = True
        for x in range(len(spChar)):
            if password[i] == spChar[x]:
                spFlag = True

    return uppercaseFlag, spFlag

#Test password Strengh - needs a register function
#Returns true if pass is valid, false if pass is invalid
# ===========RULES===========
# Must be 8 or more Characters long
# Must have at least 1 special character (!?@#%)
# Must contain at least one uppercase character#
def passStrengthTester(password):
    passIsValid = True
    passLen = len(password)
    uppercaseFlag, spFlag = stringSearch(password, passLen)
    
    if passLen < 8:
        print("Password must be 8 or more Characters long")
        passIsValid = False
    if not uppercaseFlag:
        print("Password must have at least 1 uppercase character")
        passIsValid = False
    if not spFlag:
        print("Password must have at least 1 special character (!?@#%)")
        passIsValid = False

    return passIsValid