# Transition Table in the form of a dictionary
dfa = {
    ('q0', 'letter'): 'q1',  # Start with a letter
    ('q1', 'letter'): 'q1',  # Continue with letters
    ('q1', '.'): 'q2',  # Dot in local part
    ('q2', 'letter'): 'q1',  # Letter after dot
    ('q1', '@'): 'q3',  # '@' must appear once
    ('q3', 'letter'): 'q4',  # Start domain with a letter
    ('q4', 'letter'): 'q4',  # Continue domain letters
    ('q4', '.'): 'q5',  # Dot before .gov/.gr
    ('q5', 'g'): 'q6',  # Correct transition for 'g' after dot
    ('q6', 'o'): 'q7',  # Next character after 'g'
    ('q7', 'v'): 'q8',  # ".gov" detected
    ('q7', 'r'): 'q8',  # ".gr" detected
}



initial_state = 'q0'
final_state = 'q8'

def get_input_type(char):
    #Categorize input characters into 'letter', 'dot', '@', or 'invalid'
    if char.isalpha() and char.islower():
        return 'letter'
    elif char == '.':
        return '.'
    elif char == '@':
        return '@'
    return 'invalid'

def test_string(email):
    #Process the input string through the DFA and determine if it's valid
    current_state = initial_state
    print(f"\nTesting string: {email}")
    print(f"Start State: {current_state}")

    for char in email:
        input_type = get_input_type(char)

        if input_type == 'invalid':
            print(f"❌ Invalid character '{char}' detected. Rejecting input.")
            return False

        if (current_state, input_type) in dfa:
            next_state = dfa[(current_state, input_type)]
            print(f"Current State: {current_state}, Input: '{char}', Next State: {next_state}")
            current_state = next_state
        else:
            print(f"❌ Transition error on input '{char}'. Rejecting input.")
            return False

    if current_state == final_state:
        print(f"✅ Accepted: {email}")
        return True
    else:
        print(f"❌ Rejected: {email}")
        return False

def main():
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
        email = input(f"Enter string {i+1} of {n}: ")
        test_string(email)


# Intro Message
print("Project 1 for CS341")
print("Section: 002")
print("Semester: Spring 2024")
print("Written by: Daniel Pol (dmp)")
print("Instructor: Arashdeep Kaur, ak3257@njit.edu\n")

# Begin Code Loop
main()
