"""
graphalith base module.

This is the principal module of the graphalith project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""

from expression import*


def processString(input_string : str) -> Expression:
    exp = Expression(string=input_string)


def main():
    # prompt for input string
    while True:
        try:
            input_string = input("Enter a string: ")
            break
        except ValueError:
            print("Oops!  That was no valid string.  Try again...")
    
    processString(input_string)
   

if __name__ == "__main__":
    main()
