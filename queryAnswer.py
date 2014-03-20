import pickle


def posInsert(termList_A,termList_B,k):
	return 0;


if __name__ == '__main__':
	# Loads the posting Index
	index = open("posIndex.dat", "rb");
	posIndex = pickle.load(index);
	print posIndex['made'];

	query =  "Juan made of youtube"
	# query = raw_input('Please enter your query: ');

	queryTerms = ' '.join(query.split());
	queryTerms = queryTerms.split(' ');
	k = len(queryTerms);
	print (queryTerms);

	i = 0;
	for term in queryTerms:
		queryTerms[i] = term.lower();
		if term in posIndex.keys():
			print "%s -->\t %s\n" % (term, posIndex[term]);
		else:
			print "%s -->\n" % (term);
		i = i +1;
		
