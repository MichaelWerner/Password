# Password Generator and Word List Creator

I wrote this tool because I had the need to create passwords that meet
these requirements:

-   At least 15 characters long

-   Must contain at least one

    -   upper case letter

    -   lower case letter

    -   Number

    -   Special character

-   I wanted this password

    -   easy to remember

    -   create a second password for a different system that meets these
        requirements

        -   max. 10 characters long

        -   no special character

        -   does not end with a number

        -   no upper case characters

## Programs

-   password_generator_list.py -- creates the passwords

-   create_wordlist.py -- creates the word list for the password
    generator

-   password_generator_tk.py -- a UI for the password generator using
    the TK package

-   password_generator_wx.py -- a UI for the password generator using
    the WX package

-   create_wordlist_ui.py -- a UI to create the word list

## Password Generator

This program uses a word list, randomly picks words, combines them and
creates 2 passwords that meet the requirements.

So that I have something to choose from, the program generates 10
password pairs.

I also added a function to show how long it will take to crack each
password.

How do I get a word list? That's why I wrote the word list generator

## Word List Generator

This tool takes a text file as input. The text file can be any file
ending in .txt. A prayer, the lyrics of your favorite song, some legal
text, anything you have written or received.

The output is another text file that has one word of the input file per
line. It ensures there are no duplicate words and every word is at least
5 characters long.

## Password generator UI versions

Both (tk and wx) work the same. It is a UI to make it simpler to use the
tool. Calls password_generator_list.py,

A config,ini in the same directory must exist and contain the script
path

## Word list generator UI version

Just a simple UI to select the text file and create the word list. Calls
create_wordlist.py.

A config,ini in the same directory must exist and contain the script
path
