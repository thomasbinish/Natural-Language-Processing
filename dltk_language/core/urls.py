from django.conf.urls import url
from core.controller.controller import pos, ner, dependency_parser, sentiment_analysis, tags_extractor, dependency_parser_svg

urlpatterns = [
        url(r'^pos/$', pos, name='pos_tagger'),
        url(r'ner/$', ner, name='ner_tagger'),
        url(r'^dependency-parser/$', dependency_parser, name='dependency_parser'),
        url(r'^dependency-parser/svg/$', dependency_parser_svg),
        url(r'^sentiment/$', sentiment_analysis, name='sentiment_analysis'),
        url(r'^tags/$', tags_extractor, name='tags_extractor'),
        ]
