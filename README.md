This is a quick readme that will be expanded upon when the project is
fully complete.

The purpose of this script is to automatically verify apple id's after
creation. It is to be used in conjunction with the Apple ID Creator
available at my github.


usage:
    'python3.4 idverification.py file.csv'
    
File is expected to be a csv file of the format:
'appleid,email_password,appleID_password'

Note that there can be as many columns as you want , but the first 2
must be the username/password

If you get an error log saying that the email has expired, the script will
automatically contact apple to request a fresh verification link, simply run
the script again after a few minutes to give apple time to resend the email.

This has been tested with gmail only. If you have issues or need assistance
feel free to submit at issue on my github @ https://github.com/BadStreff/