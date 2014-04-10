#!/usr/bin/env python
#Sagar Kurani
#Dr. Li

import pickle
from math import log10, sqrt, pow

#boolean search
def booleanSearch(queryTerms):
	termPosDic = {}				#stores the term position dict
	
	#loop and find the term position dict
	for term in queryTerms:
		try:
			#find the termDocIndex using term
			termCount, termDocIndex = index[term]
			#store teh term position list and doc in termPosDic
			termPosDic[term] = {doc:termPosList[1] for doc, termPosList in termDocIndex.items()}
		except:
			continue
	#return the sorted list of docs
	return [sorted([doc for doc in posDic.keys()]) for term, posDic in termPosDic.items() ]
	
#display the ouptut of queries
def display(cosTotal):
	#sorted the results using highest cos values
	sortedList = sorted(cosTotal, reverse = True , key=lambda x: cosTotal[x])
	#find the docs using doc id in documents and output them
	for doc in sortedList:
		for line in open("docs.txt"):
			if str(doc) == line.split()[1]:
				print cosTotal[doc], line.split()[0]
#finds df-raw		
def dfRaw(queryTerms):
	dfraw = []					#stores the df-raw
	#find the df-raw
	for term in queryTerms:
		try:
			#find the termDocIndex
			(trash, termDocIndex) = index[term]
			#find the total number of docs and add to dfraw
			dfraw.append(len(termDocIndex.keys()))
		except:
			continue
	return dfraw

#finds idf	
def IDF(queryTerm, dfraw):
	N = 0						#number of docs
	#find the number of docs
	for line in open("docs.txt"):
		N += 1
	return [log10(float(N)/float(dfcount)) for dfcount in dfraw]

#finds tf-raw		
def tfRaw(queryTerms):
	tfraw = {}					#stores the tf-raw
	#count the number of terms in the query
	for term in queryTerms:
		if tfraw.has_key(term):
			tfraw[term] += 1
		else:
			tfraw[term] = 1
			
	return [tfraw[term] for term in queryTerms]

#finds tf-raw for docs	
def tfRawDoc(index, doc, queryTerms):
	tfrawDoc = []				#stores the tf-raw for documents
	#get the termDocCount for each term in termDocIndex
	for term in queryTerms:
		try:
			termCount, termDocIndex = index[term]
			tfrawDoc.append(termDocIndex[doc][0])
		except:
			continue
	return tfrawDoc
	
#compute the qqq.ddd = ltn.ltc
def computeModel(mergeDocList, index, queryTerms):
	#compute queryTerms
	dfraw = dfRaw(queryTerms)			#compute dfraw
	idf = IDF(queryTerms, dfraw)		#compute idf
	tfraw = tfRaw(queryTerms)			#compute tfraw
	#compute tf
	tf = [1 + log10(float(tf_raw)) for tf_raw in tfraw]
	#compute tfidf
	tfidf = [i*t for i,t in zip(tf, idf)]
	
	#compute doc tf-raw
	tfrawDoc = {doc:tfRawDoc(index, doc, queryTerms) for doc in mergeDocList}
	#compute doc tf-doc
	tfDoc = {doc:[1+log10(float(t)) for t in tf_raw] for doc,tf_raw in tfrawDoc.items()}
	#compute doc tf-idf
	tfidfDoc = {doc:[tf*i for tf,i in zip(tf_raw,idf) ]for doc,tf_raw in tfDoc.items()}
	#compute docs magnitude
	magDoc = {doc:[pow(tf_idf,2) for tf_idf in value]for doc,value in tfidfDoc.items()}
	#finds the total of square root terms in magDoc
	for doc,value in magDoc.items():
		total = 0
		for tf_idf in value:
			total += tf_idf				#store the total of all squared terms
		total = sqrt(total)				#take the root
		magDoc[doc] = total				#store the total related with the doc
		
	cosTotal = {}						#stores the cos value
	for doc,value in tfidfDoc.items():
		total = 0
		#multiply the terms of query tfidf and doc's tfidf
		#and divide it with docs's magnitude
		for tf_idf_doc, tf_idf in zip(value, tfidf):
			total += tf_idf_doc*tf_idf			#add multiplied terms
			cosTotal[doc] = total/magDoc[doc]	#divide it with magnitude
	#return the cosTotal		
	return cosTotal
			
			
#calls intersect to merge the doc list
def findIntersectList(l):
	#do the first intersection of list 
	#if only one list(queryTerm = 1) then merge it with empty list
	try:
		l12 = intersect(l[0],l[1])	#merge the first 2 terms
		del l[0]					#delete the list term 1
		del l[0]					#delete the list term 2
	except:
		try:
			l12 = intersect(l[0],[])	#merge it with empty list
		except:
			return []				#if l has no docs return empty list
	
	#loop till the size of l and keep merging the list
	for i in range(0,len(l)):		
		l12 = intersect(l12, l[i])	#merge the list with l12
	#return the l12 list of merge docs
	return l12	

#merge the two doc list			
def intersect(p1, p2):
	answer = []				#stores the answer
	posP1 = 0				#index for p1 list
	posP2 = 0				#index for p2 list 
	#loop till the merge is compelete
	while posP1 < len(p1) and posP2 < len(p2):
		#if docs of p1 and p2 are same add the doc to answer
		if p1[posP1] == p2[posP2]:
			answer.append(p1[posP1])	#add doc
			posP1 += 1 					#increase the index of p1 and p2
			posP2 += 1
		elif p1[posP1] < p2[posP2]:		#p1 doc is else than p2 doc increase p1 index
			posP1 += 1					#increase p1 index
		else:
			posP2 += 1					#if doc p2 less than p1 increase p2 index

	return answer					#return answer
	
#split the kQuery and find the docId(s)
def querySplit(queryTerms, k):
	l1 = [queryTerms[0],queryTerms[1]]			#set the l1 terms
	#set up the l2 terms
	l2 = [queryTerms[0],queryTerms[len(queryTerms)-1]]
	l = []
	l.append(findDocId(
	, l1, k))		#find l1 query docs ex: term1,term2
	l.append(findDocId(index, l2, k))		#find l2 query docs ex: term1, term3

	#find the rest of the query combination docs ex: term2 term3 ...
	for pos in range(2,len(queryTerms)):
		queryWords = [queryTerms[pos-1], queryTerms[pos]]
		l.append(findDocId(index, queryWords, k))
	#return the answer
	return l


#finds the docId of the query terms ex: term1, term2 docs
def findDocId(index, queryWords, k):
	l = []				#stores the final docs 
	termPosDic = {}		#stores teh term position dictionary
	docs = {}			#stores docs for finding the positon of terms
	#find the term Position dictionary
	for queryTerm in queryWords:
		try:
			(termCount, termDocIndex) = index[queryTerm]
			#store the term as key and doc as key and value being termPosList
			#ex: {term: {doc: [position list]}}
			termPosDic[queryTerm] = {key:termPosList[1] for key, termPosList in termDocIndex.items()}
		except:
			continue
	#find the docs that are position correctly with the terms
	for term, posDic in termPosDic.items():
		#if the lenght is 1 of termPosDic then only 2 terms are same
		#ex: computer,computer
		if len(termPosDic) == 1:
			#iter throught the positions and see if within the reach of k
			for doc, posList in posDic.items():
				for pos in range(1,len(posList)):
					if(posList[pos] - posList[pos-1] < k):
						l.append(doc)
		else:
			#iter throught the first term and stores it's docs positions
			#iter throught the second term position
			#and find out if any positions are within the value of k
			for doc, posList in posDic.items():
				if(docs.has_key(doc)):
					for pos in posList:
						for docPos in docs[doc]:
							if (docPos - pos) < k:
								l.append(doc)
				else:
					docs[doc] = posList
	#remove the duplicate docs and return the answer in list form
	return list(set(l))


#read the index from file posIndex
def findIndex():
	f = open('posIndex.dat')					#open file posIndex.dat
	index = pickle.loads(f.read())				#read the pickle dump
	f.close()									#close file
	return index								#return the index

if __name__ == '__main__':
	M = 10										#query count
	index = findIndex()							#find the index
	#get user query and split
	queryTerms = raw_input("QUERY: ").lower().split()
	k = len(queryTerms)							#find the length of query
	
	#check if lenght is 1 or more
	if(len(queryTerms) > 1):
		l = querySplit(queryTerms, k)			#find the docs for merging
	else:
		l = booleanSearch(queryTerms)			#find the docs for length 1
		#put the docs in mergeDocList 
		try:
			mergeDocList = [docs for docs in l[0]]
		#if nothing in the list empty
		except:
			mergeDocList = []
		#compute the cosTotal
		cosTotal = computeModel(mergeDocList, index, queryTerms)
		display(cosTotal)						#display the results for length = 1
		exit(0)									#exit the program
	
	mergeDocList = findIntersectList(l)		#merge the docs list
	if(M >= len(mergeDocList)):					#check if docs equal to M
		k = int(k*1.5)							#change the k value by =k*1.5
		l2 = querySplit(queryTerms, k)			#find the docs for merging
		mergeDocList = findIntersectList(l2)	#merge the docs
	if(M >= len(mergeDocList)):					#check length again
		l3 = booleanSearch(queryTerms)			#do boolean search if M not met
		mergeDocList = findIntersectList(l3)	#merge the list of docs
	#compute the cos value
	cosTotal = computeModel(mergeDocList, index, queryTerms)
	display(cosTotal)							#output the results