import random

# def guess_the_number():
#     number = random.randint(1, 100)
#     attempts = 0
#
#     # Function to gen number, one takes number and return response, private variable
#
#     print("Welcome to Guess the Number!")
#     print("I'm thinking of a number between 1 and 100.")
#
#     while True:
#         try:
#             guess = int(input("Take a guess: "))
#             attempts += 1
#         except ValueError:
#             print("Invalid input. Please enter a number.")
#             continue
#
#         if guess < number:
#             print("Too low!")
#         elif guess > number:
#             print("Too high!")
#         else:
#             print(f"Congratulations! You guessed the number in {attempts} attempts.")
#             break

def genNumber():
    number = random.randint(1, 100)
    return number

def numberGame(number, attempts=0):
    guess = int(input("Guess: "))
    attempts += 1

    if guess > number:
        # print("Ran " + str(attempts))
        print("Too High!")
        return numberGame(number, attempts)
    elif guess < number:
        # print("Ran1 " + str(attempts))
        print("Too Low!")
        return numberGame(number, attempts)
    else:
        # print("Ran WOOOOOOO " + str(attempts))
        return f"Congratulations! You guessed the number {number} in {attempts} attempts."

numberGame(genNumber())

if __name__ == "__main__":
    pass
