### Poor in the beginning:
ACM
University of California
UCI
of
is
master of software engineering
the
a
of
and
or



### Decent in the beginning:
cristina lopes
machine learning
student
computer science


### Good in the beginning
Information retrieval
krone martins
robot
computer
search
store


### Improvements
In the beginning, mostly it was because the way how we implemented the inverted index was to save into just one file instead of many, which caused issues such that it has to read every single line of the inverted index to figure out what is needed and what should be discarded. Just iterating through each line through the inverted index already takes around 1.4 seconds. 

We were able to improve it by durastically changing how we store the inverted index. Instead of in one file, it is broken up to `n` number of files, where `n` is the number of tokens in the corpus. Such that we also have a master file that points from each word to a filename. Such like `of -> 4` that leads to `file4.txt` which contains the posting that the word `of` was in. This way we only have to load up the master file, which is around 5 seconds in the initializing stage of the querier, then we just have to go through it to figure out which file to read, and then read those specific files to reduce redaundant time.


