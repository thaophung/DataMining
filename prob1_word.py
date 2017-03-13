import os
import sys
#from __future__ import division
import re
import random
import time
import binascii
from bisect import bisect_right
from heapq import heappop, heappush

doc_file1 = sys.argv[1]  
doc_file2 = sys.argv[2]

shinglesInDoc1 = set() 
shinglesInDoc2 = set()

f1 = open(doc_file1, "rU")
f2 = open(doc_file2, "rU")

#SH3 2-gram/shingle based on words
words1 = f1.readline().split(" ")
words2 = f2.readline().split(" ")
for i in range(0, len(words1)-1):
    shingle1 = words1[i]+" " + words1[i+1] 
    shinglesInDoc1.add(shingle1)

for i in range(0, len(words2)-1):
    shingle2 = words2[i]+ " " + words2[i+1]
    shinglesInDoc2.add(shingle2)

inter = shinglesInDoc1.intersection(shinglesInDoc2)
uni = shinglesInDoc1.union(shinglesInDoc2)
jacc_similar = 1.0*len(inter)/len(uni)
print jacc_similar
f2.close()
f1.close()
    
