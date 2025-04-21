class transition_dmp:

    #Cant rename this function, constructor
    def __init__(self, present_state, input_symbol, stack_top, popped, pushed, next_state):
        self.present_state = present_state
        self.input_symbol = input_symbol
        self.stack_top = stack_top
        self.popped = popped
        self.pushed = pushed
        self.next_state = next_state

    #Cant rename this function, to string
    def __str__(self):
        return (
            f"----------------------------------------------------------------------------------\n"
            f"Present State: {self.present_state}\n"
            f"Current input symbol under R-head: {self.input_symbol or 'epsilon'}\n"
            f"Stack Top: {self.stack_top or 'epsilon'}\n"
            f"Symbol popped from Stack: {self.popped or 'epsilon'}\n"
            f"Symbols pushed onto Stack: {self.pushed or 'epsilon'}\n"
            f"Next state: {self.next_state}\n"
            f"----------------------------------------------------------------------------------\n"
        )

S = 'S'
Vn =['S','T','C','H','Y','N'] 
Vt =['.','0','1','2','3','4','5','6','7','8','9','+','-','*','/','(',')','a','b']
delta = []

#pda.append(transition_dmp())

def parseString_dmp(w):
    print(w)

def main_dmp():
    #Handles input and runs the PDA for multiple test cases.
    while True:
        try:
            n = int(input("Enter number of total strings to be tested: "))
            if n < 0:
                print("Please enter a non-negative number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    for i in range(n):
        while True:
            w = input(f"Enter string {i+1} of {n}: ")
            parseString_dmp(w)
            print('\n__________________________________________________________________________________________________\n')
            break


# Intro Message
print("Project 2 for CS341")
print("Section: 002")
print("Semester: Spring 2025")
print("Written by: Daniel Pol (dmp)")
print("Instructor: Arashdeep Kaur, ak3257@njit.edu\n")

print(f"Vn: {Vn}")
print(f"Vt: {Vt}")
print(f"Start Symbol: {S}\n")

# Begin Code Loop
main_dmp()
