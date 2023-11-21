import sys
import math


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()
    with open (filename,encoding='utf-8') as f:
        # TODO: add your code here
        content = f.read()
        for i in range(ord('A'), ord('Z') + 1):
            X[chr(i)] = 0
        for char in content:
            # Check if the character is a letter
            if char.isalpha():
                upper_case_char = char.upper()
                if ord(upper_case_char) < ord('A') or ord(upper_case_char) > ord('Z'):
                    continue
                X[upper_case_char] += 1
    return X

def F(X, e, s, y):
    term1 = 0
    term2 = 0
    if y == "English":
        term1 = math.log(0.6)
        p = e
    elif y == "Spanish":
        term1 = math.log(0.4)
        p = s
    for i in range(0, 26):
        term2 += X[chr(ord('A')+i)] * math.log(p[i])
    return term1 + term2

# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!
def main():
    #Q1
    print("Q1")
    X = shred("letter.txt")
    for i in range(ord('A'), ord('Z') + 1):
        print(chr(i) + " " + str(X[chr(i)]))
    
    #Q2
    print("Q2")
    e, s = get_parameter_vectors()
    #X_1log_e1
    print(format(X["A"] * math.log(e[0]), '.4f'))
    #X_1log_s1
    print(format(X["A"] * math.log(s[0]), '.4f'))

    #Q3
    print("Q3")
    #F(english)
    F_english = F(X, e, s, "English")
    print(format(F_english, ".4f"))
    #F(spanish)
    F_spanish = F(X, e, s, "Spanish")
    print(format(F_spanish, ".4f"))

    #Q4
    print("Q4")
    #P (Y = English | X)
    P = 0
    if F_spanish - F_english >= 100:
        P = 0
    elif F_spanish - F_english <= -100:
        P = 1
    else:
        P = 1/(1+math.exp(F_spanish-F_english))
    print(format(P, ".4f"))


if __name__ == "__main__":
    main()
