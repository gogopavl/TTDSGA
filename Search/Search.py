import re
from enum import Enum
from Processor import PreProcessor

class QueryType(Enum):
    BOOL = 1
    TERM = 2

class SearchEngine:
    _index = {}
    _preprocessor = PreProcessor()

    _re_bool = re.compile("(.*?)\\b(AND NOT|AND|OR)\\b(.*)")

    def __init__(self, index):
        """ Set inverted index. """        
        self._index = index
        return

    def match(self, query):
        
        """Execute a boolean search and returns a list of matched document IDs."""
        docs = []

        query_type, parts = self.parse_query(query)
        if query_type == QueryType.BOOL:
            # If bool, recursively get results for left & right part
            left_set = self.match(parts[0])
            right_set = self.match(parts[2])
            
            # Perform boolean match
            op = parts[1]
            if op == "AND":
                docs = self.get_intersection([left_set, right_set])
            elif op == "OR":
                docs = self.get_union([left_set, right_set])
            elif op == "AND NOT":
                docs = self.get_difference([left_set, right_set])
        else:
            """Matches documents that contain all terms of a query."""
            tokens = self._preprocessor.process(query)
            doc_lists = []
            for token in tokens:
                if token in self._index:
                    doc_lists.append(self._index[token])
            docs = self.get_intersection(doc_lists)
            

        docs.sort()
        return docs

    def parse_query(self, query):
        """Identifies a query's type and its constituent parts."""
        match = self._re_bool.match(query)
        if not match is None:
            return QueryType.BOOL, match.group(1, 2, 3)        
        return QueryType.TERM, query
    
    def get_union(self, lists):
        if lists is None or len(lists) == 0:
            return []
        if len(lists) == 1:
            return list(set(lists[0]))

        union = list(set({}).union(*lists))
        union.sort()
        return union

    def get_intersection(self, lists):
        if lists is None or len(lists) == 0:
            return []
        if len(lists) == 1:
            return list(set(lists[0]))

        list_as_set = set(lists[0])
        intersect = list(list_as_set.intersection(*lists))
        intersect.sort()
        return intersect

    def get_difference(self, lists):
        if lists is None or len(lists) == 0:
            return []
        if len(lists) == 1:
            return list(set(lists[0]))

        difference = list(set(lists[0]).difference(lists[1]))
        difference.sort()
        return difference