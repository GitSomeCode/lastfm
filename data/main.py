import os, unirest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from app.models import Tag, TagRelation
from __future__ import division
import itertools, json

api_url = "http://ws.audioscrobbler.com/2.0/"
api_key = "ff51b4c5accb4afdc6dee971884949b3"