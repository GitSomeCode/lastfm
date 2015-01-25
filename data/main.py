from __future__ import division
import os, unirest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.conf import settings
from app.models import Tag, TagRelation
import itertools, json

# To use api key, use settings.API_KEY

api_url = "http://ws.audioscrobbler.com/2.0/"

# this is only for one page! 50 artist per page, 20 pages total
topArtists = unirest.post(api_url, headers={"Accept":"application/json"}, params={"api_key":settings.API_KEY, "method":"chart.gettopartists", "format":"json"})

'''
topArtists_toprint = json.dumps(GTA.body, indent=2)
print topArtists_toprint
'''

result = topArtists.body
artists = []

for a in result["artists"]["artist"]:
  print a["name"]
  artists.append(a["name"])
  
one = artists[0]

tag = unirest.post(api_url, headers={"Accept":"application/json"}, params={"api_key":settings.API_KEY, "artist":one, "method":"artist.getTopTags", "format":"json"})

tag_body = tag.body

tagName = tag_body["toptags"]["tag"][0]["name"]
tagCount = tag_body["toptags"]["tag"][0]["count"]

tag1 = Tag(name = tagName, count = tagCount)
tag1.save()
