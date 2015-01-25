import os, unirest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from app.models import Tag 
from __future__ import division
import itertools, json

print "this works"