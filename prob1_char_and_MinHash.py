import os
import sys
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

docsAsShingleSets = {}
#SH1 2-gram/shingle based on characters
#shingle1 = f1.read(2)
#shingle2 = f2.read(2)
#SH2 3-gram/shingle based on characteris
docNames = []
shingle1 = f1.read(3)
docNames.append(shingle1)
shingle2 = f2.read(3)
docNames.append(shingle2)
while(shingle1 != ""):
    shingle1 = f1.read(3)
    crc = binascii.crc32(shingle1) & 0xffffffff
    shinglesInDoc1.add(crc)
    #shingle1 = f1.read(2)
docsAsShingleSets[docNames[0]] = shinglesInDoc1
while(shingle2 != ""):
    shingle2 = f2.read(3)
    crc = binascii.crc32(shingle2) & 0xffffffff
    shinglesInDoc2.add(crc)
    #shingle2 = f2.read(2)
docsAsShingleSets[docNames[1]] = shinglesInDoc2
# Calculate Jaccard Similarity using intersection and union
inter = shinglesInDoc1.intersection(shinglesInDoc2)
uni = shinglesInDoc1.union(shinglesInDoc2)
jacc_similar = 1.0*len(inter)/len(uni)
print jacc_similar
f1.close()
f2.close()

# MinHash
t0 = time.time()
# The current shingle ID value to assign to the next new shingle we
# encounter. When a shingle gets added to the dictionary, we'll 
# increment this value
curShingleID = 0

# Create a dictionary of the articles, mapping the article identifier
# to the list of shingle IDs that appear in the document.
numHashes = 500 #20, 60, 200, 500

# Record the maximum shingleID that we assigned
maxShingleID = 2**32 - 1

# We need the next largest prime number above 'maxShingleID'
nextPrime = 4294967311

#Generate a list of 'k' random coefficients for the random hash functions
# while ensuring that the same value does not appear multiple times in the list
def pickRandomCoeffs(k):
    # Create a list of 'k' random values
    randList = []
    
    while k > 0:
    # Get a random shingle ID
  	randIndex = random.randint(0, maxShingleID)
    # Ensure that each random number is unique
 	while randIndex in randList:
	    randIndex = random.randint(0, maxShingleID)
    # Add the random number to the list
	randList.append(randIndex)
 	k = k-1
    return randList

# For each of the 'numHashes' hash functions, generate a different coefficient 'a' and 'b'
coeffA = pickRandomCoeffs(numHashes)
coeffB = pickRandomCoeffs(numHashes)

#print '\nGenerating MinHash signatures for all documents...'
# List of documents represented as signature vectors
signatures = []
# List of documents represented as signature vectors
shingleList1 = list(shinglesInDoc1)
shingleList2 = list(shinglesInDoc2)


# Rather than generating a random permutation of all possible shingles,
# we'll just hash the IDs of the shingles that are *actually in the document*,
# then take the lowest resulting hash code value. This corresponds to the index
# of the first shingle that you would have encountered in the random order.

# For each document...
for docID in docNames:
    # Get the shingle set for this document
    shingleIDSet = docsAsShingleSets[docID]
    
    # The resulting minhash signature for this document
    signature = []
    
    # For each of the random hash functions...
    for i in range(0, numHashes):
	# For each of the shingles actually in the document, calculate its hash code
	# using hash function 'i'
 	# Track the lowest hash ID seen. INitialize 'minHashCode' to be greater than 
	# the maximum possible valu output by the hash.
	minHashCode = nextPrime + 1
	
	# For each shingle in the document...
	for shingleID in shingleIDSet:
	    # Evaluate the hash function
	    hashCode = (coeffA[i] * shingleID + coeffB[i]) % nextPrime
	    # Track the lowest hash code seen
	    if hashCode < minHashCode:
		minHashCode = hashCode
 
            # Add the smallest hash code value as component number 'i' of the signature.
 	    signature.append(minHashCode)
 
    	# Store the MinHash signature for this document
    signatures.append(signature)
# Comparing MinHash signatures"

# Get the MinHash sinature for document i
signature1 = signatures[0]
# Get the MinhHash signature for document j 
signature2 = signatures[1]
count = 0
#Count the number of positions in the minhash signature which are equal.
for k in range(0, numHashes):
    count = count + (signature1[k] == signature2[k])
# Record the percentage of positions which matched
print (1.0 * count / numHashes)

# Calculate the elapsed time (in seconds)
elapsed = (time.time() - t0)
print elapsed 
