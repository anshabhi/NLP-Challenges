import re
import sys
with open('corpus.txt') as fin:
    corpus = fin.read()

pattern = re.compile(r" |:|;|,|-|\n|'|\.|\"|\'|!")
corpus = pattern.split(corpus.lower())
corpus = [w.strip() for w in corpus]
corpus = [w for w in corpus if len(w) > 1]

N = int(input())

names = sys.stdin.readlines()

males = set(['he', 'his', 'him', 'himself', 'father', 'brother', 'uncle', 'half-brother', 'halfbrother', 'son', 'boy', 'dad', 'grandfather', 'king', 'nephew', 'actor', 'steward', 'barman', 'groom', 'chairman', 'man', 'gentleman', 'hero', 'host', 'husband', 'landlord', 'lord', 'monk', 'prince', 'waiter', 'widower', 'character', 'marquis', 'earl', 'italian', 'sir', 'cousin', 'englishman', 'attack', 'war', 'ranger', 'businessman', 'crowned','co-founder','corporation','technology','engineering','slays','intemperate', 'washerman,', 'berating', 'wayward', 'kill','buried','ruin','settle','exile','secretary','foreign','verses'])

females = set(['she','girl', 'hers', 'her', 'herself', 'mother', 'sister', 'aunt', 'half-sister', 'halfsister', 'daughter', 'girl', 'mom', 'grandmother', 'queen', 'niece', 'actress', 'stewardess', 'barmaid', 'bride', 'chairwoman', 'lady', 'headmistress', 'heroine', 'hostess', 'wife', 'landlady', 'lady', 'nun', 'princess', 'waitress', 'widow', 'dear', 'little', 'businesswoman','impure','forest','abducted','marries','purity','listen','earth','furrow','goddess','brother-in-law','queen','woman','female','women','baroness','dedication,', 'self-sacrifice','wifely', 'womanly', 'virtues'])
for k, name in enumerate(names):
    name = name.strip().lower()

    pos_lst = [i for i, x in enumerate(corpus) if x == name]
    
    male = 0
    female = 0
    for i in pos_lst:
        male += sum([corpus[i-25:i+25].count(w) for w in males])
        female += sum([corpus[i-25:i+25].count(w) for w in females])

    if male > female:
        print ('Male')
    else:
        print ('Female')