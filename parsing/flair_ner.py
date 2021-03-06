from flair.data import Sentence

def _extract_persons(text, tagger):

    text = " ".join(text.strip().split()[:50])

    sentence = Sentence(text)

    tagger.predict(sentence)

    names = []
    name_parts = []

    chunks = sentence.to_tagged_string().split()

    for i, chunk in enumerate(chunks):
        if '<S-PERSON>' in chunk:
            names.append(chunks[i - 1])
        elif '<B-PERSON>' in chunk or '<M-PERSON>' in chunk:
            name_parts.append(chunks[i-1])
        elif '<E-PERSON>' in chunk:
            name_parts.append(chunks[i - 1])
            names.append(" ".join(name_parts))
            name_parts = []

    return names

def _extract_edu(section, tagger):

    edu = []

    for sent in section:

        sentence = Sentence(sent)

        tagger.predict(sentence)

        edu_parts = []

        chunks = sentence.to_tagged_string().split()

        for i, chunk in enumerate(chunks):
            if '<S-ORG>' in chunk or '<S-DATE>' in chunk:
                edu.append((chunks[i - 1], chunks[i]))
            elif '<B-ORG>' in chunk or '<M-ORG>' in chunk or ('<B-DATE>' in chunk or '<M-DATE>' in chunk):
                j = i
                edu_parts.append(chunks[i - 1])
                while (j < len(chunks)) and ('<E-' not in chunks[j]) and ('<S-' not in chunks[j]):
                    if ('<B-' not in chunks[j]) and ('<I-' not in chunks[j]):
                        edu_parts.append(chunks[j])
                    j += 1
            elif '<E-DATE>' in chunk or '<E-ORG>' in chunk:
                edu.append((" ".join(edu_parts), chunks[i]))
                edu_parts = []

    return edu