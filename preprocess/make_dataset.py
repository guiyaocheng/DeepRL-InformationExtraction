

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
                sample = parse_line(line)
                raw_data.append((sample, len(raw_data)))
    return raw_data


def parse_line(line):
    '''You should write specific paring code here'''

    fields = line.split('\t')
    sourceID = fields[0]
    targetID = fields[1]
    rels = fields[2].split(',')
    sent = fields[3]

    return sourceID,targetID,rels,sent

def load_confidence(conf_file):
    raw_conf = []
    with codecs.open(conf_file, 'r', 'utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('\t')
            prediction = fields[0]
            conf = fields[1]
            conf = float(conf)
            raw_conf.append(((prediction,conf), len(raw_conf)))
    return raw_conf

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
    return [(sid,tid,rlabels,sent,rpred,conf,id1) for ((sid,tid,rlabels,sent), id1), ((rpred,conf), id2) in zip(raw_data,raw_conf)]

def separate(raw_data, raw_conf):
    entity_pairs = [(sid,tid) for (sid,tid,rs,sent),rid in raw_data]
    rels = [rs for (sid,tid,rs,sent),rid in raw_data]
    sents = [sent for (sid,tid,rs,sent),rid in raw_data]
    confs = [(pred,conf) for (pred,conf), rid in raw_conf]
    return entity_pairs,rels,sents,confs

def group(combined_raw):
    grouped_data = dict()
    for sid,tid,rlabels,sent,rpred,conf,id in combined_raw:
        if (sid,tid) not in grouped_data:
            grouped_data[(sid,tid)] = [(rlabels,sent,rpred,conf,id)]
        else:
            grouped_data[(sid,tid)].append((rlabels,sent,rpred,conf,id))
    return grouped_data

def make_data(grouped_data, entity_map):
    first_articles = []
    downloaded_articles = []
    identifiers = []
    entities = []
    confidences = []
    for (sid,tid), slist in grouped_data.items():
        articlelist = []
        conflist = []
        entitylist = []
        sname = entity_map[sid]
        tname = entity_map[tid]
        assert sname
        assert tname
        for rlabels,sent,rpred,conf,id in slist:
            articlelist.append(sent)
            conflist.append([conf,conf,conf])
            entitylist.append([rpred,sname,tname])
        downloaded_articles.append([articlelist])
        entities.append([entitylist])
        confidences.append([conflist])
        identifiers.append([rlabels[0],sname,tname]) ## todo : not sure if it is fine to select the first label?
        first_articles.append(articlelist[0])
    return first_articles,downloaded_articles,identifiers,entities,confidences


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

def extract_context(downloaded_articles, entities, vectorizer, context=3):
    contexts = [None] * len(entities)
    for i in range(len(contexts)):
        contexts[i] = [None] * len(entities[i])
        for j in range(len(contexts[i])):
            contexts[i][j] = [None] * len(entities[i][j])

    for indx, queryLists in enumerate(entities):
        for listNum, articleList in enumerate(queryLists):
            for articleNum, entities in enumerate(articleList):
                article = downloaded_articles[indx][listNum][articleNum]
                rpred,ent1,ent2 = entities
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

def write_group(grouped_data,entity_map,filename):
    with codecs.open(filename, 'w', 'UTF-8') as f:
        for (sid,tid), raws in grouped_data.items():
            sn = entity_map[sid]
            tn = entity_map[tid]
            s1st = sid+'\t'+tid+'\t'+sn+'\t'+tn+'\t'
            stmp = fillblank(len(sid)) + '\t'
            stmp += fillblank(len(tid)) + '\t'
            stmp += fillblank(len(sn)) + '\t'
            stmp += fillblank(len(tn)) + '\t'
            for i in range(len(raws)):
                if i==0:
                    s = s1st
                else:
                    s = stmp
                rlabels, sent, rpred, conf, id = raws[i]
                slabel = ''
                for r in rlabels:
                    slabel += r + ';'
                s += slabel + '\t'
                s += rpred + '\t'
                s += str(conf) + '\t'
                s += str(id) + '\t'
                s += sent + '\n'
                f.write(s)

mode = 'test'

raw_data = load_data_file('/home/gyc/Data/held_out_dir/{}.sent.txt'.format(mode))
raw_conf = load_confidence('/home/gyc/Data/held_out_dir/{}.scores.txt'.format(mode))
entity_map = load_entity_name('/home/gyc/Data/held_out_dir/filtered-freebase-simple-topic-dump-3cols.tsv')

combined_raw = combine(raw_data,raw_conf)
grouped_data = group(combined_raw)

first_articles,downloaded_articles,identifiers,entities,confidences = make_data(grouped_data, entity_map)

cosine_sim = calculate_cosine_sim(first_articles,downloaded_articles,1)

entity_pairs,rels,sents,confs = separate(raw_data, raw_conf)
vec1,vec2 = getContextDictionary(sents)

contexts1 = extract_context(downloaded_articles,entities,vec1,context=3)
contexts2 = extract_context(downloaded_articles,entities,vec2,context=3)

with open('/home/gyc/Data/held_out_dir/{}.p'.format(mode), "wb") as f:
    pickle.dump([first_articles,downloaded_articles,identifiers,entities,confidences,cosine_sim,contexts1,contexts2,vec1,vec2],f)

sentence = u'But he doubted that modified calendars produce any overall academic benefits , a view shared by Gene V. Glass , a professor of education policy at Arizona State University , who said that at least a half-dozen studies suggest that \'\' there is not a scrap of evidence that shows a year-round calendar improves achievement . \'\''
vec = extract_entity_context(sentence,u'Gene V. Glass',vec2)

write_group(grouped_data,entity_map,'/home/gyc/Data/held_out_dir/{}.grouped.txt'.format(mode))