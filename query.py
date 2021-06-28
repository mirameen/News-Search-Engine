import string
import numpy as np
from numpy import *
from numpy.linalg import norm
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import time
from nltk.stem.porter import *


start_time = time.time()

df = pd.read_csv("news_summary_more.csv")
df = df.head(2000)

news_sum = df['text'].tolist()
news_hl = df['headlines'].tolist()
stop_words = np.array(stopwords.words('english'))
unt_ind = {}


def tokenize_normalize(text):  # used to tokenize and normalize a document
    lower_text = str(np.char.lower(text))
    tokens = word_tokenize(lower_text)
    #p_stem = PorterStemmer()
    #tokens = [p_stem.stem(w) for w in tokens]
    final_tokens = [w for w in tokens if
                    w not in stop_words and w not in string.punctuation]  # remove stop words and punctuation
    return final_tokens


def tokenize(documents):  # tokenize all documents
    documents = [tokenize_normalize(str(np.char.replace(d, "'", ""))) for d in documents]
    return documents


def idf(documents):        # calculates idf for all terms in the collection
    tkn_dict = {}
    unt = [word for token_list in documents for word in token_list]
    for i in range(len(unt)):
        if unt[i] in tkn_dict:
            tkn_dict[unt[i]] += 1
        else:
            tkn_dict[unt[i]] = 1
    unt = np.unique(unt)
    df_tk = np.array([1 / tkn_dict[unt[i]] for i in range(unt.shape[0])])
    df_tk *= (len(news_sum))
    df_tk = np.log(df_tk)
    df_tk += 1
    idf_pre = {}
    global unt_ind
    for i in range(unt.shape[0]):
        idf_pre[unt[i]] = df_tk[i]
        unt_ind[unt[i]] = i
    return df_tk


def get_tf(ntk):                # calculates tf for all terms in the collection
    global unt_ind
    tk = np.zeros(shape=(len(ntk), len(unt_ind)))
    for i in range(len(ntk)):
        for j in range(len(ntk[i])):
            if ntk[i][j] in unt_ind:
                tk[i][unt_ind[ntk[i][j]]] += 1

    tk = ma.log(tk)
    tk += 1
    tk = tk.filled(0)
    return tk


def tf_idf(tf, idf_a):                 # calculates tf-idf for all documents
    return tf * idf_a


def cos_similarity(vector1, vector2):  # calculates cosine similarity between query and document
    return dot(vector1, vector2) / (norm(vector1) * norm(vector2))


nt = (tokenize(news_sum))
idf_c = idf(nt)
tf_c = get_tf(nt)
tf_idf_c = tf_idf(tf_c, idf_c)
print(tf_idf_c.shape)
print("Preprocessing done!")
print("Time to preprocess : --- %s seconds ---" % (time.time() - start_time))


def get_cos_similarity(query_str):                  # takes query and generates search results
    qt = []
    st = time.time()
    query_token = tokenize_normalize(str(np.char.replace(query_str, "'", "")))
    qt.append(query_token)
    qt_tf = get_tf(qt)
    # print(query_token)
    tf_idf_qt = tf_idf(qt_tf, idf_c)
    tf_idf_query = tf_idf_qt[0]

    if norm(tf_idf_query) == 0:
        query_doc_sim = [0 for tfidf_doc in tf_idf_c]
    else:
        query_doc_sim = [cos_similarity(tf_idf_query, tfidf_doc) for tfidf_doc in tf_idf_c]
    # print(query_doc_sim)
    temp_sim = sorted(range(len(query_doc_sim)), key=lambda k: query_doc_sim[k])
    temp_sim.reverse()

    news_results = [(news_hl[temp_sim[i]], news_sum[temp_sim[i]]) for i in range(10)]
    et = time.time()
    return news_results, et - st
