# Passec Password Manager

## Description
Passec Manager is a terminal based password manager designed to securely store, retrieve and manage user passwords with built in security fuctions.

## Features
Passec Manager includes:
- Account registration and login
- Email verification
- Password reset
- Strong master password enforcement
- Auto generates strong passwords
- Have I been Pwned and Leakcheck API usage - check for user's private information in data breaches
- Inactivity auto logout
- MongoDB database storing account information and user's passwords
- Store, edit and retrieve passwords

## Setup Instructions
Note: This program is best run on a Linux machine as it is easier to set environment variables. 

1. Install 'pymongo' package
```bash
pip install pymongo
```
2. Setup pymongo database and tables
3. Create a gmail account to send out email verification/password reset codes
    - An app password needs to be generated for this rather than the initially set account password
4. Generate an encryption key - there is a function commented out in utils.py, uncomment and run this function once, then save the encryption key for later steps
5. Set Environment Variables

    Check which shell your machine is using
    ```bash
    echo $SHELL
    ```
    1) If the output is bash then it will look like this:
    ```bash
    usr/bin/bash
    ```

    Add environment variables to shell config file
    ```bash
    nano ~/.bashrc
    ```


    2) If the output is zsh then it will look like this:
    ```bash
    usr/bin/zsh
    ```

    Add environment variables to shell config file
    ```bash
    nano ~/.zshrc
    ```

    After opening the shell config file in the text editor, the following environment variables need to be set to the values you got from the previous steps:
    
    **File:** `.bashrc or .zshrc`
    ```bash
    export mongodbURI="mongodbExampleURI"
    export secretKey="12341234123412341234123412341234123412341234"
    export passecEmail="example@gmail.com"
    export passecEmailPass="pass pass pass pass"

    ```

## What Makes a Strong Password?
Passec Password Manager attempts to find the middle ground between having a strong secure password and avoiding scaring off users with too many strict rules.
#### Passec Manager's Password Policy:
- Contains at least 8 or more characters
- Contains at least 1 special character (!?@#%)
- Contains at least one uppercase, lowercase and numerical character

## How To Use Passec Password Manager
The application has a fairly linear design therefore the menus are easy to follow. Input prompt for the user asks for either a numerical value (for navigating menu options) or a string value (for entering details to store/authenticate). Despite this, further insight into each feature/function is given in this section.

### Pre-Login Menu
The pre-login menu contains four different options:
1. <b>Register</b>a new account for the service. This requires input from three different fields: Username, Email Address and Password. Email verification is required for this and is performed by sending a code to the input email address and waiting for the user to input it into Passec Password Manager during the registration phase.

2. <b>Login</b> to an existing account on the service. This requires a valid username and password. After inputing them you will be taken to the post login menu which is covered in the next section.

3. <b>Recover password</b> by sending a verification code to the email address attached to the user's account. Upon entering the correct code the user will be given the opportunity to either enter a new password or have a strong password generated for them. The user will then be returned to the pre-login menu where they can login into there account using the new password.

4. <b>Exit</b> the application - The application simply stops running.

### Post-Login Menu
The post-login menu has an inactivity timer which will automatically log you out of your account if it does not receive an input from you for 2 minutes. This menu contains seven different options:
1. <b>Retrieve all passwords</b> that have previously been stored on your account. This is displayed in the form of a list, each row being a password. It shows you the service name, the username for the service and the password for the service respectively.

2. <b>Store a new password</b> on your account. This will require you to enter the service name, username and password.

3. <b>Edit a stored password</b>. This requires the service name of the password to be input. After that the option is given to either enter a new password or have Passec Manager generate a strong password for you.

4. <b>Email Breach Check</b> searches for instances of the email address attached to your account appearing in data breaches. This will return a list of websites where the email address has been breached and the date that it was breached - each row being a new record.

5. <b>Password Breach Check</b> searches for instances of the master password appearing in data breaches. This returns an integer value of the number of breaches that the password has been found in. This will first require that the user retypes their master password so that this can be performed securely.

6. <b>General Security Test</b> performs the same functionality as the previous menu option, however it carries this out on every single password stored on the user's account and displays the results for each one. It also performs a general password strength check on each password as stored passwords are not required to follow the password policy that the master password does. If a password is lacking in an area of strength then it will be pointed out in the general security check to encourage the user to improve it and their security along with it.

7. <b>Logout</b> does exactly what you would expect it to do and logs the user out of their account. They are returned to the pre-login menu.
