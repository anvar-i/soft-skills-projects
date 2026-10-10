from service import Register, LogIn, leave
from security import error_msg

if __name__ == "__main__":
    print(
    "\n◄---------------------------------------------------►\n",
     "Welcome to MVP version of Banking System with Python!\n",
     "◄---------------------------------------------------►\n")
    while(True):
        print("Enter operation number:\n0. Register\n1. Log In\n2. Exit\n\n")
        try:
            choice = int(input('>> '))
            match(choice):
                case 0:
                    Register()
                case 1:
                    LogIn()

                case 2:
                    leave()
                case _:
                    print(error_msg(error = "ValueError", range_end=2))
                    continue
        except TypeError:
            print(error_msg(error="TypeError"))
            continue
