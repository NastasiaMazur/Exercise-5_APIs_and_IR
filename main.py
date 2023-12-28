import requests
import json
import string

from porter_stemmer import PorterStemmer

# Part 2

class Sonnet:
    def __init__(self, sonnet_data):
        # Extract the number of the sonnet (in this case, 32) and title from the title string
        title_parts = sonnet_data["title"].split(":")
        self.id = int(title_parts[0].strip().split()[-1])  # Store it as a value of type int in attribute id
        self.title = str(title_parts[1].strip())           # Store it as a value of type str in attribute title

        self.lines = sonnet_data["lines"]                  # Store the lines of the sonnet in an attribute called lines.

    def __str__(self):
        return "\n".join(self.lines)

    def __repr__(self):
        return f"Sonnet {self.id}: {self.title}"

    def tokenize(self) -> list[str]:
        all_tokens = []
        stemmer = PorterStemmer()
        for line in self.lines:
            # Split on whitespace, convert to lowercase, and remove punctuation
            tokens = line.lower().split()
            tokens = [token.strip(string.punctuation) for token in tokens]

# Part 4
            #tokens_2 = ['this', 'day']
            for token in tokens:
                # Use the stemmer on a token
                stemmed_token = stemmer.stem(token, 0, len(token) - 1)
                #print(stemmed_token)

            #all_tokens.extend(tokens)
                all_tokens.append(stemmed_token)

        return all_tokens


sonnet_example_32 = {
    "title": "Sonnet 32: If thou survive my well-contented day",
    "author": "William Shakespeare",
    "lines": [
        "If thou survive my well-contented day,",
        "When that churl Death my bones with dust shall cover",
        "And shalt by fortune once more re-survey",
        "These poor rude lines of thy deceased lover,",
        "Compare them with the bett'ring of the time,",
        "And though they be outstripp'd by every pen,",
        "Reserve them for my love, not for their rhyme,",
        "Exceeded by the height of happier men.",
        "O! then vouchsafe me but this loving thought:",
        "'Had my friend's Muse grown with this growing age,",
        "A dearer birth than this his love had brought,",
        "To march in ranks of better equipage:",
        "But since he died and poets better prove,",
        "Theirs for their style I'll read, his for his love'."
    ],
    "linecount": "14"
}

# Part 1
url = "https://poetrydb.org/author,title/Shakespeare;Sonnet"

response = requests.get(url)

if response.status_code == 200:
    print("Request was successful!")
    print("Response content:")

    # print(response.text)

    data = json.loads(response.text)

# Part 2/2: Convert the list of dictionaries to a list of Sonnet instances
    sonnets_instances = [Sonnet(sonnet_data) for sonnet_data in data]  # list comprehension

    # Print the lines of each sonnet
    for sonnet32 in sonnets_instances:
        print(f"\nSonnet {sonnet32.id}: {sonnet32.title}")
        # print(str(sonnet_instance.lines))
        print(sonnet32.lines)

else:
    print(f"Error: Unable to fetch data. Status Code: {response.status_code}")


# Part 2
sonnet32 = Sonnet(sonnet_example_32)

print(repr(sonnet32))

print(str(sonnet32))
print(f"\n")

# Part 3 - Tokenize and print the tokens
tokens = sonnet32.tokenize()
#print(f"\nTokens of {sonnet32.title}:")
print(tokens)
