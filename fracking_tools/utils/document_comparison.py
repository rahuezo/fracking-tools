from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SHINGLE_SIZE = 3


def get_cosine_similarity(content1, content2):
    try:
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform((content1, content2))
        cosim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)[0][-1]
        return round(cosim, 4)
    except IOError as msg:
        print msg
        return -1


def get_shingles(content, size):
    buff = content.lower()

    for i in range(0, len(buff) - size + 1):
        output = buff[i:i + size]
        yield output


def compute_jaccard(set1, set2):
    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    return x / float(y)


def get_jaccard_similarity(content1, content2):
    try:
        shingles_1 = set(get_shingles(content1, size=SHINGLE_SIZE))
        shingles_2 = set(get_shingles(content2, size=SHINGLE_SIZE))
        jasim = compute_jaccard(shingles_1, shingles_2)
        return round(jasim, 4)
    except IOError as msg:
        print msg
        return -1


def compair(content1, content2):
    cosim = get_cosine_similarity(content1, content2)
    jasim = get_jaccard_similarity(content1, content2)
    return [cosim, jasim]


# with open(r'D:\Dropbox\Fracking Networks Data Collection 2015\Newspaper aggregating\Adams Village\DailyGazette/FrackingANTIFRACKING GROUPS RA.txt', 'r') as f:
#     a = f.read()
#     b = f.read()
# print compair('this is osmething', 'this is osmething')


