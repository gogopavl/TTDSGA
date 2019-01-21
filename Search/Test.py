from Search import SearchEngine
from Index import IndexBuilder

builder = IndexBuilder()
search = SearchEngine(builder.Index)
print(builder.Index)
docs = search.match("appl OR cherri OR banana")
print(docs)