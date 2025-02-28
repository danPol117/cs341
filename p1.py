dfa = {
    ('q0', 'a'): 'q1',   # Start with a letter
    ('q1', 'a'): 'q1',   # Continue with letters
    ('q1', '.'): 'q2',   # Dot in local part
    ('q2', 'a'): 'q1',   # Letter after dot is allowed
    ('q1', '@'): 'q3',   # '@' must appear once
    ('q3', 'a'): 'q4',   # Start domain with a letter
    ('q4', 'a'): 'q4',   # Continue domain letters
    ('q4', '.'): 'q5',   # Dot in domain
    ('q5', 'g'): 'q6',   # Start of ".gov" or ".gr"
    ('q6', 'o'): 'q7',
    ('q7', 'v'): 'q8',   # ".gov" detected
    ('q7', 'r'): 'q8',   # ".gr" detected
}

inital_state = 'q0'
final_state = 'q8'

def main():
    n = int(input("Enter number of total strings to be tested: "))
    for i in range(n):
        email = input(f"Enter string {i+1} of {n}: ")
        testString(email)

def testString(email):
    print(f"Testing string {email}")


main()