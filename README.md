_This project is not longer being actively maintained, however, PR's are still welcome!_

## Synopsis

The purpose of this script is to automatically verify Apple ID's after
creation.

## Motivation

This project exist to be used in conjuction with Apple ID creation scripts,
it's purpose is to automatically verify the emails sent after creating the
Apple ID's. In the past this had to be done by hand, which is fairly time
consuming.

## Installation & Usage

The project only requires that you have python 3.4 or greater installed.
After that, download the project, navigate to it's directory and run:

`python idverification.py example.csv`

Example.csv is a csv file containing the Apple ID's and and password, it is
expected to be in the format:
```
appleid1@gmail.com,email_password,id_password
appleid2@gmail.com,email_password,id_password
appleid3@gmail.com,email_password,id_password
...
```

## Common Issues

**This will only work with accounts that use gmail servers.**

A common issue users have is that they create all these Apple ID's and the
verification links will expire, this script will detect if a link is expired
and automatically request a new one. When this happens the script will let you
know. Simply run the script at a later time, the reason for this is to give apple
time to resend the verification email.

## Contributors

[Adam Furbee](https://github.com/BadStreff)

## License

GNU-GPL v3
