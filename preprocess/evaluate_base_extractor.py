from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import codecs

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


raw_data = load_data_file('/home/gyc/Data/held_out_dir/test.sent.txt')
raw_conf = load_confidence('/home/gyc/Data/held_out_dir/test.scores.txt')

y_true = [rlabels[0] for (sid,tid,rlabels,sent), id1 in raw_data]
y_pred = [rpred for (rpred,conf), id2 in raw_conf]

# multi-class and multi-label evaluation
# return f1_score(y_true, y_pred, average='macro')
# return f1_score(y_true, y_pred, average='micro')
print f1_score(y_true, y_pred, average='weighted')
# print f1_score(y_true, y_pred, average=None)
print confusion_matrix(y_true, y_pred)


y_true_set = set([(sid,tid,rlabels[0]) for (sid,tid,rlabels,sent), id1 in raw_data])
y_pred_conf = [((sid,tid,rpred),conf) for ((sid,tid,rlabels,sent), id1), ((rpred,conf), id2) in zip(raw_data,raw_conf)]
y_pred_sorted = sorted(y_pred_conf, key=lambda d:d[1], reverse=True)


count_pred,count_correct = 0.0,0.0
count_total = len(y_true_set)
for y,p in y_pred_sorted:
    sid,tid,r = y
    count_pred += 1
    if y in y_true_set:
        count_correct += 1

    precision = count_correct/count_pred
    recall = count_correct/count_total
    f1score = 2*precision*recall/(precision+recall)
    print 'precision, recall, f1 :: ', precision,recall,f1score

