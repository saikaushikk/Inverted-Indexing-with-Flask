import re
import sys

"""This is the main API file which has class definitions for all the data structures we need. The index_document() function is the index function specified
    in the assignment. The clear_index function is the function for clearing the index. The lookup_query function can be used for searching the index."""


class Appearance:
    """
    Represents the appearance of a term in a given document, along with the
    frequency of appearances in the same one.
    """

    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency

    def __repr__(self):
        """
        String representation of the Appearance object
        """
        return str(self.__dict__)


class Database:
    """
    In memory database representing the already indexed documents.
    """

    def __init__(self):
        self.db = dict()

    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.__dict__)

    def get(self, id):
        return self.db.get(id, None)

    def add(self, document):
        """
        Adds a document to the DB.
        """
        return self.db.update({document["id"]: document})

    def remove(self, document):
        """
        Removes document from DB.
        """
        return self.db.pop(document["id"], None)


class InvertedIndex:
    """
    Inverted Index class.
    """

    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        """
        String representation of the Database object
        """
        return str(self.index)

    def index_document(self, document):
        """
        Process a given document, save it to the DB and update the index.
        """

        # Remove punctuation from the text.
        clean_text = re.sub(r"[^\w\s]", "", document["text"])
        terms = clean_text.split(" ")
        appearances_dict = dict()
        # Dictionary with each term and the frequency it appears in the text.
        for term in terms:
            term_frequency = (
                appearances_dict[term].frequency if term in appearances_dict else 0
            )
            appearances_dict[term] = Appearance(document["id"], term_frequency + 1)

        # Update the inverted index
        update_dict = {
            key: [appearance]
            if key not in self.index
            else self.index[key] + [appearance]
            for (key, appearance) in appearances_dict.items()
        }
        self.index.update(update_dict)
        # Add the document into the database
        self.db.add(document)
        return document

    def lookup_query(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        """
        return {
            term: self.index[term] for term in query.split(" ") if term in self.index
        }

    # This function can be used to clear a index created for a particular file.
    def clear_index(self):
        self.index.clear()


def highlight_term(id, term, text):
    replaced_text = text.replace(term, "[{term}]".format(term=term))
    return "--- document {id}: {replaced}".format(id=id, replaced=replaced_text)


db = Database()
index = InvertedIndex(db)


def indexing(filename, searchterm):
    with open(filename, encoding="utf8") as f:
        lines = f.read().lower()
    """This is the main function that is being used in the app for uploading a text file and searching for a term. 
        It returns a list of max length 10 of the search results for the search term."""
    tests = lines.split("\n\n")
    docdictionary = {}
    array = []
    for i in range(0, len(tests)):
        docdictionary["id"] = str(i)
        docdictionary["text"] = tests[i]
        array.append(docdictionary)
        docdictionary = {}

    for ele in array:
        index.index_document(ele)
    datastr = []
    result = index.lookup_query(searchterm)
    i = 0
    for term in result.keys():
        for appearance in result[term]:
            if i == 11:
                break
            document = db.get(appearance.docId)
            datastr.append(highlight_term(appearance.docId, term, document["text"]))
            i = i + 1
    return datastr
