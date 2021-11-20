import random
# random.seed(42)
# Generate markov chain from text file
def markov_chain(file):
    """Takes a file and returns a dictionary that maps
    words to a list of possible suffixes, which is also a dictionary.

    Args:
        file (str): name of file to read
    
    Returns:
        dict: dictionary of words to list of suffixes
    """
    # open file
    with open(file, 'r') as f:
        # read file
        text = f.read()
        # split text into words
        words = text.split()
        # create dictionary
        output = {}
        # loop through words
        for i in range(len(words) - 1):
            # if word is not in dictionary
            if words[i] not in output:
                # add word to dictionary
                output[words[i]] = [words[i + 1]]
            # if word is in dictionary
            else:
                # add word to dictionary
                output[words[i]].append(words[i + 1])
        # return dictionary
        return output

# Generate random text from markov chain
def random_text(language, length):
    """ Generates random text from a markov chain.

    Args:
        language (dict): dictionary of words to list of suffixes
        length (int): length of text to generate

    Returns:
        str: random text
    """
    keys = list(language.keys())  # create list of keys
    option = random.choice(keys) # get random key, set as the first word
    text = [] # create empty list
    for i in range(length): # loop through length of text
        if option not in language: # if word is not in dictionary
            break
        else: # if word is in dictionary
            text.append(option)
            option = random.choice(language[option]) # set word to random word
    return " ".join(text) # return text

k = markov_chain('test.txt')
# print(k)
print(random_text(k, 20))
# print(markov_text(k, 200))
