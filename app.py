from findRelevantDays2 import findRelevantDays
from generateInstagramPost import generateInstagramPost

days = findRelevantDays(10)

posts = [generateInstagramPost(day) for day in days ]

print(posts)


