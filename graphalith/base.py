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

def main():
    # prompt for input string
    while True:
        try:
            input_string = input("Enter an expression string: ")
        except ValueError:
            print("Oops!  That was no valid string.  Try again...")
    
        exp = Expression(value=input_string)
        #print(exp)
        print(exp.expression_evaluate())
   

if __name__ == "__main__":
    main()
