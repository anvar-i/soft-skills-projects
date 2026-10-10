# Verifies mails to have @gmail.com, or other components
def verify(mail):
    final = ['@gmail.com', '@mail.com', '@mail.ru']

    for f in final:
        if f in mail: return mail
        else: pass
    
    return mail+ '@gmail.com'
    


# HASH - hides data from users, hashed values stored in json file.
def HASH(value : str): pass

# handling error about value range
def error_msg(error= "Error", range_beg= 0, range_end= 1):
    return (f"{error}. Value must be in range from {range_beg} to {range_end}. Other choices do not exist.\nPlease, try again!\n\n")


"""
Completed: error_msg(), verify()

Working:

Not Finished: HASH()
"""