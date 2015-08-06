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

## Synopsis

The purpose of this script is to automatically verify apple id's after
creation. It is to be used in conjunction with the Apple ID Creator
available at my github.

## Motivation

This project exist to be used in conjuction with apple id creation scripts,
it's purpose is to automatically verify the emails sent after creating the
apple id's.

## Installation & Usage

The project only requires that you have python 3.4 or greater installed.
After that, downloed the project, navigate to it's directory and run:

`python idverification.py example.csv'

Example.csv is a csv file containing the apple id's and and password, it is
expected to be in the format:
```appleid1@gmail.com,email_password,id_password
appleid2@gmail.com,email_password,id_password
appleid3@gmail.com,email_password,id_password
.
.
.
```

## Common Issues

**This will only work with accounts that use gmail servers.**

A common issue users have is that they create all these apple id's and the
verification links will expire, this script will detect if a link is expired
and automatically request a new one. When this happens the script will let you
know. Simply run the script at a later time, the reason for this is to give apple
time to resend the verification email.

## Contributors

Myself (Adam J Furbee)

## License

GNU-GPL v3