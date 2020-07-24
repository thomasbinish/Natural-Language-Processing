import base64
import os
import spacy
from spacy import displacy
from core.component.tags_extractor import Rake
from nltk.sentiment.vader import SentimentIntensityAnalyzer



nlp = spacy.load('en_core_web_sm')


def pos_tagger(params):
    text = params["text"]
    doc = nlp(text)
    response = {}
    pos_response = {}
    for token in doc:
        pos_response[token.text] = token.tag_
    response["result"] = pos_response
    response["text"] = text
    return response


def ner_tagger(params):
    text = params["text"]
    doc = nlp(text)
    response = {}
    ner_response = {}
    person_details = []
    org_details = []
    for ent in doc.ents:
        ner_response[str(ent)] = ent.label_
    response["result"] = ner_response
    response["text"] = text
    response["persons"] = person_details
    response["organizations"] = org_details
    return response


def parser(params):
    text = params["text"]
    doc = nlp(text)
    response = {}
    dependency_response = {}
    for token in doc:
        dependency_response[str(token.text)] = {"dep": token.dep_,
                                                "headText": token.head.text,
                                                "headPOS": token.head.pos_,
                                                "children": [str(child) for child in token.children]
                                                }
    response["result"] = dependency_response
    response["text"] = text
    return dependency_response


def sentiment(params):
    text = params["text"]
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    response = {}
    if scores["compound"] > 0:
        emotion = "POSITIVE"
        polarity = 3
    elif scores["compound"] < 0:
        emotion = "NEGATIVE"
        polarity = 1
    else:
        emotion = "NEUTRAL"
        polarity = 0
    response["emotion"] = emotion
    response["text"] = text
    response["polarity"] = polarity
    response["scores"] = scores
    return response


def tags(params):
    text = str(params["text"])
    rake = Rake("./core/resources/SmartStoplist.txt")
    keywords = rake.run(text)
    result = []
    response = {}
    for keyword in keywords:
        result.append(keyword[0])
    response["tags"] = result
    response["text"] = text
    return response


def parser_svg(params):
    try:
        text = params["text"]
        doc = nlp(text)
        svg = displacy.render(doc, style="dep")
        # svg2png(bytestring=svg, write_to='output.png')
        with open('output.png', "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string
    finally:
        os.remove('output.png')
