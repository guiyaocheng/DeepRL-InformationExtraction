

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import codecs
import nltk
import re
import pickle


# function to build the dictionary for words to be used for context features
def getContextDictionary(articles):

    vectorizer1 = CountVectorizer(min_df=1)
    vectorizer2 = TfidfVectorizer(min_df=1)
    vectorizer1.fit(articles)
    vectorizer2.fit(articles)

    print "Computed vectorizers."
    return vectorizer1, vectorizer2


def load_data_file(data_file):
    print('loading file ', data_file)
    raw_data = []
    if not isinstance(data_file, list):
        data_file = [data_file]
    for file_name in data_file:
        with codecs.open(file_name, 'r', 'utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fields = line.split('\t')
                pID = fields[0]
                sourceID = fields[1]
                targetID = fields[2]
                rels = fields[3].split(',')
                sent = fields[4]
                raw_data.append((pID,sourceID,targetID,rels,sent,len(raw_data)))
    return raw_data


def load_confidence(conf_file):
    raw_conf = []
    rels = []
    with codecs.open(conf_file, 'r', 'utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('\t')
            if len(rels) == 0:
                rels = fields
            else:
                confs = (rels,[float(f) for f in fields])
                raw_conf.append(confs)
    return rels, raw_conf

def load_entity_name(entity_name_file):
    entity_map = dict()
    with codecs.open(entity_name_file, 'r', 'utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('\t')
            id = fields[0]
            name = fields[1]
            if id not in entity_map:
                entity_map[id] = name
    return entity_map

def combine(raw_data, raw_conf):
    return [(pid,sid,tid,rlabels,sent,predrs,confs,id1) for (pid,sid,tid,rlabels,sent,id1), (predrs,confs) in zip(raw_data,raw_conf)]


def group(combined_raw):
    grouped_data = dict()
    for pid,sid,tid,rlabels,sent,predrs,confs,id in combined_raw:
        if (pid,sid,tid) not in grouped_data:
            grouped_data[(pid,sid,tid)] = [(rlabels,sent,predrs,confs,id)]
        else:
            grouped_data[(pid,sid,tid)].append((rlabels,sent,predrs,confs,id))
    return grouped_data

def make_data(grouped_data, entity_map, rels):
    articles = []
    identifiers = []
    preds = []
    confidences = []
    entities = []
    for (pid,sid,tid), slist in grouped_data.items():
        articlelist = []
        conflist = []
        predlist = []
        sname = entity_map[sid]
        tname = entity_map[tid]
        assert sname
        assert tname
        for rlabels,sent,predrs,confs,id in slist:
            articlelist.append(sent)
            predlist.append(predrs)
            conflist.append(confs)
        articles.append([articlelist])
        entities.append([(sname,tname)])
        preds.append([predlist])
        confidences.append([conflist])
        identifier = []
        rlabelset = set(rlabels)
        for i in range(len(rels)):
            if rels[i] in rlabelset:
                identifier.append(rels[i])
            else:
                identifier.append('NA')
        identifiers.append([identifier])
    return articles,identifiers,entities,preds,confidences


def calculate_cosine_sim(first_articles,downloaded_articles,numLists=1):
    ''' now to calculate cosine_sim using tf-idf calculated using all the downloaded articles'''

    tfidf_vectorizer = TfidfVectorizer()
    cosine_sim = [None] * len(first_articles)
    for i in range(len(cosine_sim)):
        cosine_sim[i] = [None] * numLists

    for indx, article in enumerate(first_articles):
        allArticles = [article]
        for i in range(numLists):
            allArticles += downloaded_articles[indx][i]

        tfidf_matrix = tfidf_vectorizer.fit_transform(allArticles)
        cnt = 1
        for listNum in range(len(downloaded_articles[indx])):
            sublist = downloaded_articles[indx][listNum]
            if len(sublist) > 0:
                cosine_sim[indx][listNum] = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[cnt:cnt + len(sublist)])[0]
            else:
                print "not enough elements in sublist for cosine_sim"
                cosine_sim[indx][listNum] = []
            # pdb.set_trace()
            cnt += len(sublist)
        #     cnt += len(sublist)
    return cosine_sim

def extract_entity_context(article,entity,vectorizer,context=3):
    '''extract context of entity in an article'''
    vocab = vectorizer.vocabulary_
    raw_article = article.lower()
    cleaned_article = re.sub(r'[^\x00-\x7F]+', ' ',raw_article)
    tokens = nltk.word_tokenize(cleaned_article)
    std_entity = nltk.word_tokenize(entity.lower())
    phrase = []
    vec = []
    for i,word in enumerate(tokens):
        if word in std_entity:
            for j in range(1, context + 1):
                if i - j >= 0:
                    phrase.append(tokens[i - j])
                else:
                    phrase.append('XYZUNK')  # random unseen phrase
            for j in range(1, context + 1):
                if i + len(std_entity) - 1 + j < len(tokens):
                    phrase.append(tokens[i + len(std_entity) - 1 + j])
                else:
                    phrase.append('XYZUNK')  # random unseen phrase
            break

    mat = vectorizer.transform([' '.join(phrase)]).toarray()
    for w in phrase:
        feat_indx = vocab.get(w)
        if feat_indx:
            vec.append(float(mat[0, feat_indx]))
        else:
            vec.append(0.)
    # take care of all corner cases
    if len(vec) == 0:
        vec = [0. for q in range(2 * context)]

    return vec

def extract_context(articles, entities, vectorizer, context=3):
    contexts = [None] * len(articles)
    for i in range(len(contexts)):
        contexts[i] = [None] * len(articles[i])
        for j in range(len(contexts[i])):
            contexts[i][j] = [None] * len(articles[i][j])

    for indx, queryLists in enumerate(articles):
        for listNum, articleList in enumerate(queryLists):
            ent1, ent2 = entities[indx][listNum]
            for articleNum, ents in enumerate(articleList):
                article = articles[indx][listNum][articleNum]
                vec1 = extract_entity_context(article,ent1,vectorizer,context)
                vec2 = extract_entity_context(article,ent2,vectorizer,context)
                contexts[indx][listNum][articleNum] = []
                contexts[indx][listNum][articleNum].append(vec1)
                contexts[indx][listNum][articleNum].append(vec2)

    return contexts

def fillblank(size):
    s = ''
    for i in range(size):
        s += ' '
    return s



dir = '/home/gyc/Data/held_out_02'
mode = 'test'

raw_data = load_data_file('{}/{}.sent.txt'.format(dir,mode))
rels, raw_conf = load_confidence('{}/{}.scores.txt'.format(dir,mode))
entity_map = load_entity_name('/home/gyc/Data/held_out_dir/filtered-freebase-simple-topic-dump-3cols.tsv')
sents = [sent for pid,sid,tid,rs,sent,rid in raw_data]

combined_raw = combine(raw_data,raw_conf)
grouped_data = group(combined_raw)

articles,identifiers,entities,preds,confidences = make_data(grouped_data, entity_map, rels)


vec1,vec2 = getContextDictionary(sents)

contexts1 = extract_context(articles,entities,vec1,context=3)
contexts2 = extract_context(articles,entities,vec2,context=3)

with open('{}/{}.p'.format(dir,mode), "wb") as f:
    pickle.dump([articles,identifiers,entities,preds,confidences,contexts1,contexts2,vec1,vec2],f)

sentence = u'But he doubted that modified calendars produce any overall academic benefits , a view shared by Gene V. Glass , a professor of education policy at Arizona State University , who said that at least a half-dozen studies suggest that \'\' there is not a scrap of evidence that shows a year-round calendar improves achievement . \'\''
vec = extract_entity_context(sentence,u'Gene V. Glass',vec2)
print vec