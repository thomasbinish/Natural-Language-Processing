import json
import traceback

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core.lib.lib import pos_tagger, ner_tagger, parser, sentiment, tags, parser_svg
from core.constants import *


@csrf_exempt
def pos(request):
    try:
        if request.method == "POST":
            params = json.loads(request.body.decode(CHARSET))
            response = pos_tagger(params)
            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e.args, status=500, content_type=CONTENT_TYPE)


@csrf_exempt
def ner(request):
    try:
        if request.method == "POST":
            params = json.loads(request.body.decode(CHARSET))
            response = ner_tagger(params)
            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e.args, status=500, content_type=CONTENT_TYPE)


@csrf_exempt
def dependency_parser(request):
    try:
        if request.method == "POST":
            params = json.loads(request.body.decode(CHARSET))
            response = parser(params)
            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e.args, status=500, content_type=CONTENT_TYPE)


@csrf_exempt
def dependency_parser_svg(request):
    try:
        if request.method == "POST":
            params = json.loads(request.body.decode(CHARSET))
            response = parser_svg(params)
            return HttpResponse(response, content_type=CONTENT_TYPE)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e.args, status=500, content_type=CONTENT_TYPE)



@csrf_exempt
def sentiment_analysis(request):
    try:
        if request.method == "POST":
            params = json.loads(request.body.decode(CHARSET))
            response = sentiment(params)
            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e.args, status=500, content_type=CONTENT_TYPE)


@csrf_exempt
def tags_extractor(request):
    try:
        if request.method == "POST":
            params = json.loads(request.body.decode(CHARSET))
            response = tags(params)
            return HttpResponse(json.dumps(response), content_type=CONTENT_TYPE)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e.args, status=500, content_type=CONTENT_TYPE)
