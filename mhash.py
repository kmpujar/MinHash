from __future__ import division
from hashlib import sha1
from datasketch.minhash import MinHash
import io
import time
reviewsList=[]
read_file=io.open('reviews.txt','r',encoding='utf-8')
split= [line.strip() for line in read_file]
for line in split:
    reviewsList.append(line.split('\t')[0])

reviews_c= [row.lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ").replace(";", " ").replace(":", " ").replace("*", " ").replace("(", " ").replace(")", " ").replace("/", " ").
replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("0", "")
for row in reviewsList]

token_review=[]
for obs in reviews_c:
    if len(obs.split())>0:
        token_review.append(obs.split())

hashMap=[]
ab=[]
avnoun=[]
def eg1():
    start_time = time.time()
    for r in token_review:
        m1 = MinHash(num_perm=16)
        for d in r:
            m1.update(d.encode('utf8'))
        hashMap.append(m1)
    for i in range(0,len(hashMap)):
        for j in range(i+1,len(hashMap)):
            ab.append(hashMap[i].jaccard(hashMap[j]))
    elapsed_time = time.time() - start_time
    print("Time taken to calculate Jaccard distance is: "+str(elapsed_time))
    del(m1)


    start_time = time.time()
    for i in range(0,len(token_review)):
        for j in range(i+1,len(token_review)):
            s1 = set(token_review[i])
            s2 = set(token_review[j])
            actual_jaccard = float(len(s1.intersection(s2))) /\
                    float(len(s1.union(s2)))
            avnoun.append(actual_jaccard)
    elapsed_time = time.time() - start_time
    print("Time taken to calculate Jaccard distance is: "+str(elapsed_time))

if __name__ == "__main__":
    eg1()
    hashMap1=[]
    ab1=[]
    start_time = time.time()
    for r in token_review:
        m2 = MinHash()
        for d in r:
            m2.update(d.encode('utf8'))
        hashMap1.append(m2)
    for i in range(0,len(hashMap1)):
        for j in range(i+1,len(hashMap1)):
            ab1.append(hashMap1[i].jaccard(hashMap1[j]))
    elapsed_time = time.time() - start_time
    print("Time taken to calculate Jaccard distance is: "+str(elapsed_time))
    sum1=0
    sum2=0
    for i in range(0,len(ab)):
        sum1=sum1+(ab[i]-avnoun[i])*(ab[i]-avnoun[i])
        sum2=sum2+(ab1[i]-avnoun[i])*(ab1[i]-avnoun[i])
    print(sum1/len(ab))
    print(sum2/len(ab))
