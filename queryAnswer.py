# Andres Felipe Gomez
# Not Finished! :(
# 03/28/2014
import pickle
import math



def posIntersect(termList_X,termList_Y,k):
	a = 1;
	b = 1;
 	intersection = [];

	while a < len(termList_X) and b < len(termList_Y):
	
		if len(termList_X[a]) < len(termList_Y[b]):
			posArray_A = termList_Y[b]
			posArray_B = termList_X[a]
		else:
			posArray_A = termList_X[a]
			posArray_B = termList_Y[b]
		# print "docs: %d = %d " %(posArray_A[0],posArray_B[0])
		
		if posArray_A[0] == posArray_B[0]:
			doc = posIntersectFind(posArray_A,posArray_B,k);
			if (doc != 0 ) :
				intersection.append(doc)
			a += 1;
			b += 1;
		elif termList_X[a][0] < termList_Y[b][0]:
			a += 1;
		else :
			b += 1;
	
	return intersection	


def posIntersectFind(posArray_A,posArray_B,k):
	
	i = 2;
	j = 2;
	intersection = [];
	while i < len(posArray_A):
		# print (posArray_A);
		# print (posArray_B);
		
		while j < len(posArray_B):
			# print "%d : %d " % (posArray_A[i] , posArray_B[j]);

			if (abs(posArray_A[i] - posArray_B[j]) <= k):
				# print "Found"
				intersection.append(posArray_A[0]);
				return posArray_A[0];
			elif (posArray_B[j] > posArray_A[i]):
				# print "break"
				i = len(posArray_A)
				break;
			j += 1;
		
	
		# i = 1;

	# print intersection
	return 0;
	 
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

def tfIdf(termList, N, queryDocs):
	
	df = termList[0]
	idf = 0.0
	idf = N/float(df)
	idf = math.log(idf);
	tfIdf = {}
	print("tfIdf : %d * %f" % (df, idf))
	i = 1
	while i < len (termList):
		if termList[i][0] in queryDocs:
			tfIdf[termList[i][0]] = termList[i][1]*float(idf)
		i += 1

	return tfIdf

def euclidianNormalized(tfIdfArrayDic, termsDoc):
	# print tfIdfArrayDic
	magnitude = []
	normalizedArray = []
	for doc in termsDoc:
		result = 0
		for term in tfIdfArrayDic:
			result += math.pow(float(term[doc]),2)
		magnitude.append(math.sqrt(result))
	del normalizedArray[:]
	for term in tfIdfArrayDic:
		normalized = {}
		i = 0
		# print "term"
		for key,value in term.iteritems():
			normalized[key] = float(value) / float(magnitude[i])

		normalizedArray.append(normalized);
		
		# print normalized
	
	# print "magnitude"
	# print magnitude

	return magnitude
			


if __name__ == '__main__':
	# Loads the posting Index
	indexFile = open("posIndex.dat", "rb");
	# docsFile = "docs.txt";
	
	docsFile = open("docs.txt")
	data = docsFile.readlines()
	docsFile.close()

	docsList =[]
	for n, line in enumerate(data, 1):
		docsList.append(line.rstrip());
		# print '{:2}.'.format(n), line.rstrip()

	posIndex = pickle.load(indexFile);
	indexFile.close();
	docsFile.close();
	query =  "state middle university"
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
			termInDoc = []
			# print "%s -->\t %s\n" % (term, posIndex[term]);
			for docId  in posIndex[term]:
				termInDoc.append(docId);
				# print (docId);
			termIndex.append(termInDoc);
			i = i +1;
		# else:
		# 	print "%s -->\n" % (term);
		
	# for term in termIndex:
	# 	print term
	M = 0
	while M < 10:
		l1 = posIntersect(termIndex[0],termIndex[1],k);

		# print l1
		
		l2 = posIntersect(termIndex[0],termIndex[2],k);
		# print l2
		l3 = posIntersect(termIndex[1],termIndex[2],k);
		# print l3
		l12 = posIntersectArray(l1,l2,k);
		# print l12
		# find intersection l1 and l2 = l12
		l123 = posIntersectArray(l12,l3,k);
		print l123
		M = len(l123);
		tfIdfArray = [];
		if ( M>=10 ):
			# print "Compute"
			
			for termList in termIndex:
				# print termList
				tfIdfArray.append(tfIdf(termList, len(docsList), l123));

			print tfIdfArray
			euclidianNormalized(tfIdfArray, l123);

			# compute scores
			#Compute scores using qqq.ddd = ltn.ltc 
		else:
			# print "Increase"
			k *= 0.5;
	print "# Andres Felipe Gomez \nNot Finished! \n03/28/2014"


	
	print "out"	

	# find intersection l12 and l3 
	
	#if size of l123 > 10 compute score

	#else k= 1.5k and repeat


	#Show results decreasing order of ranking, Ranking - URL


