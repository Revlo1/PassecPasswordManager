from userAuth import register, login, recoverPassword
from passwordManager import passecMain


#   =-=-=-=-=-=-=-=-=TO DO LIST =-=-=-=-=-=-=-=-=-=
# Cloud Functionality

passecArt = """
  _____                        __  __                                   
 |  __ \                      |  \/  |                                  
 | |__) |_ _ ___ ___  ___  ___| \  / | __ _ _ __   __ _  __ _  ___ _ __ 
 |  ___/ _` / __/ __|/ _ \/ __| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 | |  | (_| \__ \__ \  __/ (__| |  | | (_| | | | | (_| | (_| |  __/ |   
 |_|   \__,_|___/___/\___|\___|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                                                         __/ |          
                                                        |___/           
"""


def main():
    print(passecArt)
    while True:
        print("\nWhat would you like to do?\n1. Register a new account\n2. Login to an existing account\n3. Forgot your password?\n4. Exit") 
        try:
            menuValue = int(input("Input Value Here: "))
        except ValueError:
            print("Invalid Option")
            continue

        match menuValue: 
            case 1:
                register()
            case 2:
                username, userID = login()
                if username:
                    passecMain(username, userID)
            case 3:
                recoverPassword()
            case 4:
                print("Exiting...")
                break
            case _: #if value is outwith specified options
                print("Invalid Option")
    

main()