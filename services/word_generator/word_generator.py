import random
import time
import os

def word_generator():
    """
    First opens the file of English words, saving it to a list stored as a variable.
    Checks the number.txt file once per second to see if the user has requested a new list of numbers.
    If they have, we randomly select the number of words they have requested, and overwrite the random_words.txt file.
    Once this is done, we reset the number.txt file to await the user's next request
    """

    dir = os.path.dirname(__file__)
    os.chdir(dir)

    with open('words.txt', 'r') as source_file:
        lines = source_file.read().splitlines()
    while True:
        time.sleep(1)
        with open('number.txt', 'r') as number_file:
            data = number_file.read()
        try:
            word_number = int(data)
            print(data)
            with open('random_words.txt', 'w') as word_file:
                for n in range(word_number):
                    word_file.write(random.choice(lines) + "\n")
            with open('number.txt', 'w') as number_file:
                number_file.write("Replace this with number of words to be generated")
        except ValueError:
            continue


if __name__ == '__main__':
    word_generator()
