from __future__ import unicode_literals, print_function

import plac
import spacy

TEXTS = [
    u'Despite a new blanket ban on the ivory trade in China, the closest major city to Mozambique\'s largest nature reserve remains a smuggling hotspot for criminal gangs.'
]


@plac.annotations(
    model=("Model to load (needs parser and NER)", "positional", None, str))

def main(model='en_core_web_sm'):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))

    for text in TEXTS:
        doc = nlp(text)
        relations = extract_sequence(doc)
        #print(relations)
        for r1 in relations:
            print(r1)
            #print('{:<10}\t{}\t{}'.format(r1.text, r2.ent_type_, r2.text))


def extract_sequence(doc):
    # merge entities and noun chunks into one token
    #spans = list(doc.ents) + list(doc.noun_chunks)
    #for span in spans:
        #span.merge()

    relations = []
    for location in filter(lambda w: w.ent_iob_ == 'B', doc):
        if location.ent_type_ == 'GPE':
            span = [location]
            index = location.i
            location_nbor = location.nbor()
            while location_nbor.ent_iob_ == 'I':
                span.append(location.nbor())
                location_nbor = location_nbor.nbor()
                span.merge()
            for parent in location.ancestors:
                if parent.pos_ == 'VERB':
                    s = ""
                    for t in parent.subtree:
                        s += t.text
                        s += " "
                    relations.append((location, s))
                    break
    return relations
    '''for location in filter(lambda w: w.ent_type_ == 'GPE' , doc):
        print(location)
        print('.')
        print(location.head)
        print('.')
        print(location.text)
        print([token.text for token in location.head.rights])
        if location.head in (location.rights):
            relations.append(location)
            for word in location.rights:
                if word in location.head.lefts:
                    relations.append(word)
            relations.append(location.head)
        else:
            relations.append(location.head)
            for word in location.lefts:
                if word in location.head.rights:
                    relations.append(word)
            relations.append(location)
        return relations'''
    '''for location in filter(lambda w: w.ent_type_ == 'GPE', doc):
        if location.dep_ in ('nsubj'):
            subject = [w for w in location.head.children if w.dep_ == 'dobj']
            thing = location.head
            print(thing)
            if subject:
                subject = subject[0]
            if thing:
                thing = thing[0]
                relations.append((location, thing, subject))'''

if __name__ == '__main__':
    plac.call(main)
