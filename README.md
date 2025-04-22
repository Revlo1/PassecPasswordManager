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