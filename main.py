import requests
import json
import string

from porter_stemmer import PorterStemmer


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

            # tokens_2 = ['this', 'day']
            for token in tokens:
                # Use the stemmer on a token
                stemmed_token = stemmer.stem(token, 0, len(token) - 1)
                # Remove apostrophes from the stemmed token
                stemmed_token = stemmed_token.replace("'", "")
                # print(stemmed_token)
                all_tokens.append(stemmed_token)

        return all_tokens


class Sonnet(Document):

    def __init__(self, sonnet_data):
        # Extract the number of the sonnet and title from the title string
        title_parts = sonnet_data["title"].split(":")
        self.id = int(title_parts[0].strip().split()[-1])  # Store it as a value of type int in attribute id
        self.title = str(title_parts[1].strip())  # Store it as a value of type str in attribute title

        self.lines = sonnet_data["lines"]  # Store the lines of the sonnet in an attribute called lines.

    def __str__(self):
        # return "\n".join(self.lines) # to avoid indentation of two last line in matched sonnets
        return "\n".join(line.lstrip() for line in self.lines)

    def __repr__(self):
        return f"Sonnet {self.id}: {self.title}"


class Query(Document):
    def __init__(self, query: str):
        # Call the parent class's __init__ method to store the query as a single line
        super().__init__([query])


url = "https://poetrydb.org/author,title/Shakespeare;Sonnet"

response = requests.get(url)

if response.status_code == 200:
    print("Request was successful!")

    data = json.loads(response.text)

    #  Convert the list of dictionaries to a list of Sonnet instances
    sonnets_instances = [Sonnet(sonnet_data) for sonnet_data in data]  # list comprehension

    # Print the lines of each sonnet:
    # for sonnet in sonnets_instances:
    #    print(f"\nSonnet {sonnet.id}: {sonnet.title}")
    #    print("\n".join(line for line in sonnet.lines))

else:
    print(f"Error: Unable to fetch data. Status Code: {response.status_code}")


class Index(dict[str, set[int]]):
    def __init__(self, documents: list[Document]):  # Sonnet to Document
        super().__init__()
        self.documents = documents

        for document in documents:
            self.add(document)

    def add(self, document):
        # Get the tokens from the document
        tokens = document.tokenize()

        # Iterate over tokens and update the index
        for token in tokens:

            if token not in self:  # Check if the token exists in the index

                self[token] = set()  # If not, add a new empty set using the token as key

            self[token].add(document.id)  # Get the set for the token and add the id of the document to the set

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


# Initialize sonnet instances

# sonnet1 = Sonnet(sonnet_1)
# sonnet2 = Sonnet(sonnet_2)
# sonnet3 = Sonnet(sonnet_3)
# index = Index([sonnet1, sonnet2])   # Create an instance of the Index class and pass the list of sonnets

# Initialize sonnet instances
sonnets_list = sonnets_instances

index = Index(sonnets_list)

query = Query("love hate")
matching_sonnets = index.search(query)

while True:
    # Read user input
    user_input = input("\nSearch for sonnets ('q' to quit)> ")

    # Check if the user wants to quit
    if user_input.lower() == 'q':
        print("Exiting...")
        break

    # Create a Query instance with the user input
    query = Query(user_input)
    # for me (bc the user might not need to see it:
    # Print the tokenized version of the user's query
    print(f"Tokenized Query: {query.tokenize()}")

    # Search for matching sonnets in the index
    matching_sonnets = index.search(query)

    # Display the results
    if matching_sonnets:
        matching_ids = ', '.join(str(sonnet.id) for sonnet in matching_sonnets)
        print(f"--> Your search for '{user_input}' matched {len(matching_sonnets)} sonnets ({matching_ids}): \n")
        for matching_sonnet in matching_sonnets:
            print(f"Sonnet {matching_sonnet.id}: [{matching_sonnet.title}]\n")
            print(matching_sonnet)
            print("\n-----------------------------------------")

    else:
        print(f"--> No sonnets found for '{user_input}'")


# Notes - done during the work:

# Sonnet 40 f.e. has "hate's"

# Ideas: One way to address this is to modify the tokenize method to keep both the original token and its stemmed
# version. Then, during the search, you can match both versions. ISSUE : the code does not use stemmed tokens during
# the search. the stemmed tokens are not compared to the stemmed tokens stored in the index. the code directly
# compares the stemmed tokens in the query to the original (unstemmed) tokens stored in the index.

# stem the query tokens BEFORE comparing them to the index
