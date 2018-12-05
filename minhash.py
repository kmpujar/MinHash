from __future__ import division
import io
import time
import random
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from nltk.corpus import stopwords
import binascii
import string
printable = set(string.printable)

cachedStopWords = stopwords.words("english")
reviewsList=[]
shinglesReviewList={}
#Reading the file to a list
read_file=io.open('reviews.txt','r',encoding='utf-8')
split= [line.strip() for line in read_file]
for line in split:
    reviewsList.append(line.split('\t')[0])


docCount1=len(reviewsList)
id=-1
for i in range(0,docCount1):
    #Elimination of stopwords and special characters
    reviewsList[i]=reviewsList[i].lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").replace(";", " ").replace(":", " ").replace("*", " ").replace("(", " ").replace(")", " ").replace("/", " ")
    reviewsList[i]=' '.join([word for word in reviewsList[i].split() if word not in cachedStopWords])
    reviewsList[i]=filter(lambda x: x in printable, reviewsList[i])
    wordList=reviewsList[i].split()
    output=set()
    if(len(wordList)>2):
        id+=1
        for w in range(0, len(wordList)-2):
            #Creating 3 word shingles
            shingle=wordList[w]+" "+wordList[w+1]+" "+wordList[w+2]
            #conversion to 32bit binary hash
            hashedShingle = binascii.crc32(shingle) & 0xffffffff
            output.add(hashedShingle)
        shinglesReviewList[str(id)]=output

docCount=len(shinglesReviewList)
mSize = int(docCount * (docCount - 1) / 2)
JacSim = [0 for x in range(mSize)]
estJacSim = [0 for x in range(mSize)]

#function to map list to matrix index
def getValue(i, j):
    if j < i:
        temp = i
        i = j
        j = temp
    k = int(i * (docCount - (i + 1) / 2.0) + j - i) - 1
    return k

#Calculation of pait wise jaccard similarity
start_time = time.time()
for i in range(0,docCount):
    for j in range(i+1,docCount):
        s1=set(shinglesReviewList[str(i)])
        s2=set(shinglesReviewList[str(j)])
        JacSim[getValue(i,j)]=(len(s1.intersection(s2)) / len(s1.union(s2)))
elapsed_time = time.time() - start_time
print("Time taken to calculate Jaccard distance is: "+str(elapsed_time))
numHashesList=[16,128]
maxShingleID = 2**32-1
nextPrime = 4294967311

#function to generate random coefficients
def createRandomCoeffs(k):
  randList = []
  while k > 0:
    randIndex = random.randint(0, maxShingleID)
    while randIndex in randList:
      randIndex = random.randint(0, maxShingleID)
    randList.append(randIndex)
    k = k - 1
  return randList

#function to calculate Mean Squared Error
def calMSe():
    summ=0
    for i in range(0, docCount):
      for j in range(0, docCount):
          Jsim=JacSim[getValue(i, j)]
          estJ = estJacSim[getValue(i, j)]
          summ=summ+((Jsim-estJ)*(Jsim-estJ))
    MSE=summ/docCount
    return(MSE)

#Estimation of Jaccard distance using minHash technique for 16 and 128 permutations
for numHashes in numHashesList:

    xcoeff = createRandomCoeffs(numHashes)
    ycoeff = createRandomCoeffs(numHashes)

    minshashSigns=[]
    start_time = time.time()
    for i in range(0,docCount):
        sign=[]
        for c in range(0, numHashes):
            minHashCode = nextPrime + 1
            for shingle in shinglesReviewList[str(i)]:
                hashCode = (xcoeff[c] * shingle + ycoeff[c]) % nextPrime
                if hashCode < minHashCode:
                    minHashCode = hashCode
            sign.append(minHashCode)
        minshashSigns.append(sign)
    for i in range(0,docCount):
        mhs1=minshashSigns[i]
        for j in range(i + 1, docCount):
            mhs2=minshashSigns[j]
            count = 0
            for k in range(0, numHashes):
                if (mhs1[k] == mhs2[k]):
                    count +=1
            estJacSim[getValue(i, j)]= (count/numHashes)
    elapsed_time = time.time() - start_time
    print("MSE for "+str(numHashes)+" random permutations is "+str(calMSe())+". Time taken:"+str(elapsed_time))
