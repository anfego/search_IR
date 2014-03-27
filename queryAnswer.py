import pickle


def posIntersect(termList_A,termList_B,k):
	a = 1;
	b = 1;
	intersection = [];
	
	while a < len(termList_A) and b < len(termList_B):
		
		if termList_A[a][0] == termList_B[b][0]:
			intersection.append(termList_A[a][0]);
			a += 1;
			b += 1;
		elif termList_A[a][0] < termList_B[b][0]:
			a += 1;
		else :
			b += 1;
	return (intersection);
	 
def posIntersectListArray(termList_A,termArray_B,k):
	
	a = 1;
	b = 0;
	intersection = [];
	
	while a < len(termList_A) and b < len(termArray_B):
		
		if termList_A[a][0] == termArray_B[0]:
			intersection.append(termList_A[a][0]);
			a += 1;
			b += 1;
		elif termList_A[a][0] < termArray_B[0]:
			a += 1;
		else :
			b += 1;
	return (intersection);

def posIntersectArray(termArray_A,termArray_B,k):
	
	a = 0;
	b = 0;
	intersection = [];
	
	while a < len(termArray_A) and b < len(termArray_B):
		if termArray_A[a] == termArray_B[b]:
			intersection.append(termArray_A[a]);
			a += 1;
			b += 1;
		elif termArray_A[a] < termArray_B[b]:
			a += 1;
		else :
			b += 1;
	return (intersection);


if __name__ == '__main__':
	# Loads the posting Index
	index = open("posIndex.dat", "rb");
	posIndex = pickle.load(index);


	query =  "mtsu computer science"
	# query = raw_input('Please enter your query: ');

	queryTerms = ' '.join(query.split());
	queryTerms = queryTerms.split(' ');
	# let /k be the size of the query terms 
	k = len(queryTerms);
	i = 0;
	for term in queryTerms:
		queryTerms[i] = term.lower();
		i += 1
	
	# print (queryTerms);
	
	termIndex = []
	
	
	for term in queryTerms:
		if term in posIndex.keys():
			ternInDoc = []
			# print "%s -->\t %s\n" % (term, posIndex[term]);
			for docId  in posIndex[term]:
				ternInDoc.append(docId);
				# print (docId);
			termIndex.append(ternInDoc);
			i = i +1;
		# else:
		# 	print "%s -->\n" % (term);
		
	# for term in termIndex:
	# 	print term

	l1 = posIntersect(termIndex[0],termIndex[1],k);
	l2 = posIntersect(termIndex[0],termIndex[2],k);
	l3 = posIntersect(termIndex[1],termIndex[2],k);
	l12 = posIntersectArray(l1,l2,k);
	# find intersection l1 and l2 = l12
	l = posIntersectArray(l12,l3,k);
	# find intersection l12 and l3 
	print l1
	
	#if size of l123 > 10 compute score

	#else k= 1.5k and repeat

	#Compute scores using qqq.ddd = ltn.ltc 

	#Show results decreasing order of ranking, Ranking - URL


