def print_banner(message):
    #Prints a banner with a message.
    print("\n" + "=" * len(message))
    print(message)
    print("=" * len(message))

def print_section_header(message, char='-'):
    #Prints a section header with a specified character.
    print("\n" + char * len(message))
    print(message)
    print(char * len(message))
