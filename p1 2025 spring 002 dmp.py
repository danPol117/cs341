# DFA Transition Table
dfa = {
    # Local part (before '@')
    ('q0', 'letter'): 'q1',  # Start with a letter
    ('q1', 'letter'): 'q1',  # Continue with letters
    ('q1', '.'): 'q2',       # Dot in local part
    ('q2', 'letter'): 'q1',  # Letter after dot

    # '@' Transition
    ('q1', '@'): 'q3',  # '@' must appear once

    # Domain part
    ('q3', 'letter'): 'q4',  # Start domain with a letter
    ('q4', 'letter'): 'q4',  # Continue domain letters
    ('q4', '.'): 'q5',       # Dot before .gov/.gr or subdomain

    # Handling multiple subdomains
    ('q5', 'letter-g'): 'q4',  # Subdomain continues with letters
    ('q5', 'g_'): 'q6',       # g 

    ('q6', 'letter-or'): 'q4',
    ('q6', 'r_'): 'q7',     #final state that can be moved off from as well to continue string. If string is completely proccessed, if it is on a final state, accept it, if not, reject it  
    ('q7', 'letter'): 'q4',
    ('q7', '.'): 'q5',

    ('q6', 'o_'): 'q8',  
    ('q8', 'letter-v'): 'q4',
    ('q8', 'v_'): 'q9',
    ('q8', '.'): 'q5',

    ('q9', 'letter'): 'q4',   #final state that can be moved off from as well to continue string. If string is completely proccessed, if it is on a final state, accept it, if not, reject it  
    ('q9', '.'): 'q5',

}

# Valid final states
final_states = {'q7', 'q9'}

def get_input_type_dmp(char):
    #Categorize input characters into 'letter', 'dot', '@', 'g_start', or 'invalid'
    if char.isalpha():
        if char.isupper():  # Reject uppercase letters
            return 'invalid'
        
        if char == 'g':
            return 'g_' 
        elif char == 'r':
            return 'r_'
        elif char == 'o':
            return 'o_'
        elif char == 'v':
            return 'v_'
        return 'letter'
    elif char == '.':
        return '.'
    elif char == '@':
        return '@'
    elif char.isdigit():  # Reject numbers
        return 'invalid'
    return 'invalid'  # Any other invalid character

def test_string_dmp(email):
    #Process the input string through the DFA and determine if it's valid
    while True:
        current_state = 'q0'
        print(f"\nTesting string: {email}")
        print(f"Start State: {current_state}")

        for i, char in enumerate(email):
            input_type = get_input_type_dmp(char)

            if input_type == 'invalid':
                print("Entered string contains invalid input bits")
                email = input("Enter a valid string: ")
                break  # Restart loop with new input


            if current_state == 'q5':
                if input_type== 'letter':
                    input_type = 'letter-g'
            elif current_state == 'q6':
                if input_type== 'letter':
                    input_type = 'letter-or'
            elif current_state == 'q8':
                if input_type== 'letter':
                    input_type = 'letter-v'
            elif current_state == 'q7' or current_state == 'q9' or current_state == 'q4' or current_state == 'q0' or current_state == 'q1' or current_state == 'q2' or current_state == 'q3':
                if input_type== 'g_' or  input_type== 'r_' or  input_type== 'o_' or  input_type== 'v_':
                    input_type = 'letter'

            print(input_type)
            if (current_state, input_type) in dfa:
                next_state = dfa[(current_state, input_type)]
                print(f"Current State: {current_state}, Input: '{char}', Next State: {next_state}")
                current_state = next_state
            else:
                print(f"Rejected: {email} (No valid transition from {current_state} for '{char}')")
                return False  # Reject if no valid transition exists



        # Accept if ending in a final state
        if current_state in final_states:
            print(f"Accepted: {email}")
            return True
        else:
            print(f"Rejected: {email} (Ended in non-final state {current_state})")
            return False

def has_number_or_uppercase_dmp(s):
    return any(c.isdigit() or c.isupper() for c in s)


def main_dmp():
    #Handles input and runs the DFA for multiple test cases.
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
            email = input(f"Enter string {i+1} of {n}: ")
            if has_number_or_uppercase_dmp(email):
                print("Invalid input: has number or uppercase letter. Try again.")
            else:
                test_string_dmp(email)
                print('\n__________________________________________________________________________________________________\n')
                break


# Intro Message
print("Project 1 for CS341")
print("Section: 002")
print("Semester: Spring 2024")
print("Written by: Daniel Pol (dmp)")
print("Instructor: Arashdeep Kaur, ak3257@njit.edu\n")

# Begin Code Loop
main_dmp()
