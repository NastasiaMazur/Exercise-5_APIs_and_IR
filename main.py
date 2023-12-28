import requests
import json


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


sonnet_data_example = {
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
    for sonnet_instance in sonnets_instances:
        print(f"\nSonnet {sonnet_instance.id}: {sonnet_instance.title}")
        # print(str(sonnet_instance.lines))
        print(sonnet_instance.lines)

else:
    print(f"Error: Unable to fetch data. Status Code: {response.status_code}")


sonnet_instance = Sonnet(sonnet_data_example)

print(repr(sonnet_instance))

print(str(sonnet_instance))

