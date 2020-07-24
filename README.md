# Natural-Language-Processing(NLP)
## Description
DLTK NLP allows you to analyze text to collect data from content such as ideas, entities, key phrases, subgroups, feelings, emotions, relationships, textual norms, using the understanding of the natural language, and to identify specific entities and relationships in unstructured text.

### Features provided

**Sentiment Analysis (sentiment)** : Analyses the sentiments of the text and categorise them as  positive, negative neutral or sentiment.

**Tags (tags)**: For extracting keywords from a paragraph.

**NER Tagger (ner)**: Locate and classify named entities mentioned in unstructured text into pre-defined categories such as person names, organizations, locations, medical codes, time expressions, quantities, monetary values, percentages, etc.

**POS Tagger (pos)**: labelling each word in a sentence with its appropriate part of speech(eg. Noun, Adjectives, Adverbs etc).

**Dependency Parser (dependency-parser)**: Dependency Parser represents the Grammatical Structure of the Sentence.

## Try out DLTK NLP [Demo](https://dev.dltk.ai/nlp/).

## Motivation
This Repository is created to showcase how Natural Language Processing is used to analyze text and get insights such as ideas, entities, key phrases, subgroups, feelings, emotions, relationships, textual norms, using the understanding of the natural language, and to identify specific entities and relationships in unstructured text.

## Frameworks/Tech stack used
[Django](https://www.djangoproject.com/) : Python-based open-source web framework that follows the model-view-template (MVC) architectural pattern.

[NLTK](https://www.nltk.org/): Leading open-source platform for natural language processing.

[SpaCy](https://spacy.io/): Open-source software library for advanced natural language processing.

## How to use?
**Option-1**: Executing ***dltk-language-core*** as a service. 

1. Clone the repository
2. Install all the required dependencies.
`pip install requirements.txt` 
3. Open command prompt/Terminal and run the django server 
`python manage.py runserver 0.0.0.0:8189`
4. Start using the APIs listed below:

**Sentiment API:**
`curl --location --request POST 'http://0.0.0.0:8189/dltk-language/nlp/sentiment/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text":"DLTK is a good open source platform"
}'`

**Tags extraction API:**
`curl --location --request POST 'http://0.0.0.0:8189/dltk-language/nlp/tags/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text":"DLTK is an open source platform"
}'`

**Named Entity Recognition API:**
`curl --location --request POST 'http://0.0.0.0:8189/dltk-language/nlp/ner/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text":"For QubitAI Company, Shreeram Iyer is the CEO"
}'`

**Part-of-Speech Tagging:**
`curl --location --request POST 'http://0.0.0.0:8189/dltk-language/nlp/pos/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text":"DLTK is an open source platform"
}'`

**Dependency Parser API:**
`curl --location --request POST 'http://0.0.0.0:8189/dltk-language/nlp/dependency-parser/svg/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text":"DLTK is a good open source platform"
}'`

**Option-2**: Executing ***dltk-language-core*** as a docker container.

**Docker**: Docker is an advanced OS virtualization software platform that makes it easier to create, deploy, and run applications in a Docker container.

Install Docker by following this [link](https://docs.docker.com/get-docker/).

**Docker compose**: Docker Compose is that users can activate all the services (containers) using a single command.

Install Docker Compose by following this [link](https://docs.docker.com/compose/install/)

Steps:

1. Clone the repository;
2. Go to the path where docker-compose.yml is placed.
3. Run the command to start the container `sudo docker-compose up -d`
4. Now check the containers `sudo docker ps`
![docker-output](https://github.com/dltk-ai/Natural-Language-Processing/blob/master/docker.png)
5. Execute the CURL Command mentioned in option-1
6. Run the command to stop the container `sudo docker-compose down`

## Lead Maintainer
[![](https://github.com/shreeramiyer.png?size=50)](https://github.com/shreeramiyer)
## Core Mainteiners
[![](https://github.com/dltk-ai.png?size=50)](https://github.com/dltk-ai)
## Core Contributers 
[![](https://github.com/GHub4Naveen.png?size=50)](https://github.com/GHub4Naveen)
[![](https://github.com/SivaramVeluri15.png?size=50)](https://github.com/SivaramVeluri15)
[![](https://github.com/vishnupeesapati.png?size=50)](https://github.com/vishnupeesapati)
[![](https://github.com/EpuriHarika.png?size=50)](https://github.com/EpuriHarika/)
[![](https://github.com/nageshsinghc4.png?size=50)](https://github.com/nageshsinghc4)
[![](https://github.com/appareddyraja.png?size=50)](https://github.com/appareddyraja)

## License
