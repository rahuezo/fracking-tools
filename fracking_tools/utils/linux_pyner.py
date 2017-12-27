from nltk.tag import StanfordNERTagger
from itertools import groupby
from files import ExtensionHandler

import os

os.environ['JAVAHOME'] = r'C:\Program Files (x86)\Java\jre1.8.0_144\bin\java.exe'
 
SNER_WD = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'SNER_2017')
JAR_PATH = os.path.join(SNER_WD, 'stanford-ner.jar')
DEFAULT_CLASSIFIER = os.path.join(SNER_WD, 'classifiers', 'english.muc.7class.distsim.crf.ser.gz')

    
def join_groups(gs):
    result = ''
    for g in gs: 
        flag = g[0][1]
        if flag == 'O': 
            result += ' '.join([i[0] for i in g])
        else: 
            result += ' <{f}>{words}</{f}> '.format(f=flag, words=' '.join([i[0] for i in g]))
    return result

    
def format_tags(tags): 
    results = []
    tab = 0     
    for group in [list(j) for i, j in groupby([i[1] for i in tags])]: 
        results.append(tags[tab:len(group) + tab])
        tab += len(group)        
    return join_groups(results)


def tag_document(content):
    print "PATH EXISTS: ", os.path.exists(JAR_PATH)
    print "REAL PATH: ",  os.path.dirname(os.path.realpath(__file__))
    print "CURRENT DIR: ", os.getcwd()
    
    st = StanfordNERTagger(DEFAULT_CLASSIFIER, path_to_jar=JAR_PATH)
    tags = st.tag(content.split())
    
    return format_tags(tags)
    
    
# with open('test.txt', 'r') as f:     
#     print tag_document(f.read())