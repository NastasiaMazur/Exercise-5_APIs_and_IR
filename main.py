import requests
import json
import string

from porter_stemmer import PorterStemmer

# Part 6

class Document:
    def __init__(self, lines):
        self.lines = lines

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
                # Remove apostrophes from the stemmed token
                stemmed_token = stemmed_token.replace("'", "")
                # print(stemmed_token)
                all_tokens.append(stemmed_token)



        return all_tokens


# Part 2

class Sonnet(Document):

    def __init__(self, sonnet_data):
        # Extract the number of the sonnet (in this case, 32) and title from the title string
        title_parts = sonnet_data["title"].split(":")
        self.id = int(title_parts[0].strip().split()[-1])  # Store it as a value of type int in attribute id
        self.title = str(title_parts[1].strip())           # Store it as a value of type str in attribute title

        self.lines = sonnet_data["lines"]                  # Store the lines of the sonnet in an attribute called lines.

    def __str__(self):
        # return "\n".join(self.lines) # to avoid indentation of two last line in matched sonnets
        return "\n".join(line.lstrip() for line in self.lines)

    def __repr__(self):
        return f"Sonnet {self.id}: {self.title}"


class Query(Document):
    def __init__(self, query: str):
        # Call the parent class's __init__ method to store the query as a single line
        super().__init__([query])


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

    #print(response.text)

    data = json.loads(response.text)

# Part 2/2: Convert the list of dictionaries to a list of Sonnet instances
    sonnets_instances = [Sonnet(sonnet_data) for sonnet_data in data]  # list comprehension

    # Print the lines of each sonnet
    for sonnet in sonnets_instances:
        print(f"\nSonnet {sonnet.id}: {sonnet.title}")
        print(sonnet.lines)

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

# Part 5
class Index(dict[str, set[int]]):
    def __init__(self, documents: list[Document]): #Sonnet to Document
        super().__init__()
        self.documents = documents

        for document in documents:
            self.add(document)

    def add(self, document):
        # Get the tokens from the document
        tokens = document.tokenize()


        # Iterate over tokens and update the index
        for token in tokens:

            if token not in self:    # Check if the token exists in the index

                self[token] = set()  # If not, add a new empty set using the token as key

            self[token].add(document.id)    # Get the set for the token and add the id of the document to the set


    def search(self, query: Query) -> list[Sonnet]:
                                        # Find document ids matching the query
        query_tokens = query.tokenize()
        matching_document_ids = set()

        for token in query_tokens:
            if token in self:
                if not matching_document_ids:
                    matching_document_ids = self[token].copy()
                else:
                    matching_document_ids.intersection_update(self[token])

        matching_sonnets = [sonnet for sonnet in self.documents if sonnet.id in matching_document_ids]
        matching_sonnets.sort(key=lambda x: x.id)  # Sort the resulting list by document id
        return matching_sonnets

# Part 5

sonnet_1 = {
    "title": "Sonnet 1: From fairest creatures we desire increase",
    "author": "William Shakespeare",
    "lines": [
      "From fairest creatures we desire increase,",
      "That thereby beauty's rose might never die,",
      "But as the riper should by time decease,",
      "His tender heir might bear his memory:",
      "But thou contracted to thine own bright eyes,",
      "Feed'st thy light's flame with self-substantial fuel,",
      "Making a famine where abundance lies,",
      "Thy self thy foe, to thy sweet self too cruel:",
      "Thou that art now the world's fresh ornament,",
      "And only herald to the gaudy spring,",
      "Within thine own bud buriest thy content,",
      "And tender churl mak'st waste in niggarding:",
      "  Pity the world, or else this glutton be,",
      "  To eat the world's due, by the grave and thee."
    ],
    "linecount": "14"
  }

sonnet_2 ={
    "title": "Sonnet 2: When forty winters shall besiege thy brow",
    "author": "William Shakespeare",
    "lines": [
      "When forty winters shall besiege thy brow,",
      "And dig deep trenches in thy beauty's field,",
      "Thy youth's proud livery so gazed on now,",
      "Will be a tatter'd weed of small worth held:",
      "Then being asked, where all thy beauty lies,",
      "Where all the treasure of thy lusty days;",
      "To say, within thine own deep sunken eyes,",
      "Were an all-eating shame, and thriftless praise.",
      "How much more praise deserv'd thy beauty's use,",
      "If thou couldst answer 'This fair child of mine",
      "Shall sum my count, and make my old excuse,'",
      "Proving his beauty by succession thine!",
      "  This were to be new made when thou art old,",
      "  And see thy blood warm when thou feel'st it cold."
    ],
    "linecount": "14"
  }

sonnet_3 = {
    "title": "Sonnet 3: Look in thy glass and tell the face thou viewest",
    "author": "William Shakespeare",
    "lines": [
      "Look in thy glass and tell the face thou viewest",
      "Now is the time that face should form another;",
      "Whose fresh repair if now thou not renewest,",
      "Thou dost beguile the world, unbless some mother.",
      "For where is she so fair whose unear'd womb",
      "Disdains the tillage of thy husbandry?",
      "Or who is he so fond will be the tomb,",
      "Of his self-love to stop posterity?",
      "Thou art thy mother's glass and she in thee",
      "Calls back the lovely April of her prime;",
      "So thou through windows of thine age shalt see,",
      "Despite of wrinkles this thy golden time.",
      "  But if thou live, remember'd not to be,",
      "  Die single and thine image dies with thee."
    ],
    "linecount": "14"
  }

# Initialize sonnet instances

#sonnet1 = Sonnet(sonnet_1)
#sonnet2 = Sonnet(sonnet_2)
#sonnet3 = Sonnet(sonnet_3)
#index = Index([sonnet1, sonnet2])   # Create an instance of the Index class and pass the list of sonnets

# Initialize sonnet instances
sonnets_list = sonnets_instances
# Part 7
index = Index(sonnets_list)

query = Query("love hate")
matching_sonnets = index.search(query)



while True:
    # Read user input
    user_input = input("Search for sonnets ('q' to quit)> ")

    # Check if the user wants to quit
    if user_input.lower() == 'q':
        print("Exiting...")
        break

    # Create a Query instance with the user input
    query = Query(user_input)
# for me:
    # Print the tokenized version of the user's query
    print(f"Tokenized Query: {query.tokenize()}")

    # Search for matching sonnets in the index
    matching_sonnets = index.search(query)

    # Display the results
    if matching_sonnets:
        matching_ids = ', '.join(str(sonnet.id) for sonnet in matching_sonnets)
        print(f"--> Your search for '{user_input}' matched {len(matching_sonnets)} sonnets ({matching_ids}):")
        for matching_sonnet in matching_sonnets:
            print(f"Sonnet {matching_sonnet.id}: {matching_sonnet}")
            print("\n-----------------------------------------")
    else:
        print(f"--> No sonnets found for '{user_input}'")


# Print the results
#print(f"Matching Sonnets:")
#for matching_sonnet in matching_sonnets:
#    print(f"-----------------------------------------\n{matching_sonnet}")


#print("Index Structure:")
#print(index)

# Checking the stemming of Sonnet 40:
sonnet40_data = {
    "title": "Sonnet 40: Take all my loves, my love, yea, take them all",
    "author": "William Shakespeare",
    "lines": [
        "Take all my loves, my love, yea, take them all;",
        "What hast thou then more than thou hadst before?",
        "No love, my love, that thou mayst true love call;",
        "All mine was thine, before thou hadst this more.",
        "Then if for my love, thou my love receivest,",
        "I cannot blame thee, for my love thou usest;",
        "But yet be blamed, if thou thyself deceivest",
        "By wilful taste of what thyself refusest.",
        "I do forgive thy robbery, gentle thief,",
        "Although thou steal thee all my poverty;",
        "And yet love knows it is a greater grief",
        "To bear love's wrong than hate's known injury.",
        "Lascivious grace, in whom all ill well shows,",
        "Kill me with spites, yet we must not be foes."
    ],
    "linecount": "14"
}

sonnet40 = Sonnet(sonnet40_data)

stemmed_tokens = sonnet40.tokenize()
print(f"\nStemmed Tokens of Sonnet 40:\n")
print(stemmed_tokens)

# To debug Part 5 put a dot near add method self -> documents
#  Sonnet 40 f.e. has "hate's"
# Ideas: One way to address this is to modify the tokenize method to keep both the original token and its stemmed version.
# Then, during the search, you can match both versions.
# ISSUE : the code does not use stemmed tokens during the search.
# the stemmed tokens are not compared to the stemmed tokens stored in the index.
# the code directly compares the stemmed tokens in the query to the original (unstemmed) tokens stored in the index.

# stem the query tokens BEFORE comparing them to the index