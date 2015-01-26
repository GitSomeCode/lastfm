from __future__ import division
import django
from django.db.models import F
import os, unirest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.conf import settings
from app.models import Tag, TagRelation
import itertools, json
django.setup()


api_url = "http://ws.audioscrobbler.com/2.0/"
artists = []

##################################
def calc(exampleTuple, percent):
  """
  Calculates metric between two tags.
  Divides each tag's count by 100 and takes average.
  Adds this to the percent.
  Takes average of this total.
  """
  print "In calc function"
  #import pdb; pdb.set_trace();
  tag1count = exampleTuple[0][1]/100
  tag2count = exampleTuple[1][1]/100
  tagSum = tag1count + tag2count
  tagAvg = tagSum/2
  metric = round((percent + tagAvg)/2, 4)
  resultTuple = (exampleTuple[0][0], exampleTuple[1][0], metric)
  
  print "returning resultTuple --- " + str(resultTuple)
  return resultTuple
##################################

# takes in list of tuples [(), (), ..., ()]
def calcGroup(group):
  """
  Calculates the relationship between every distinct pair of tags in an artist group. 
  Artist group is a list.
  Tuples in list are ('tag_name', tag_count)
  """
  percent = 1/len(group)
  print "percent is " + str(percent)
  
  for i in itertools.combinations(group, 2):
    
    relation = calc(i, percent)
    
    tag_name1 = relation[0]
    tag_name2 = relation[1]
    metric = relation[2]
    
    # do tagRelation stuff here 
    relExists = getRelation(tag_name1, tag_name2)
    if not relExists:
      print "NEW RELATION"
      relExists = TagRelation.objects.create(tag_to=Tag.objects.get(name=i[0][0]), tag_from=Tag.objects.get(name=i[1][0]), metric=metric)
    relExists.metric += metric
    relExists.save()
      
    '''
    if TagRelation exists, then just update the metric, 
    else create new TagRelation with new metric
    '''
##################################    
def getRelation(name1, name2):
    """
    Checks to see is a relation exists between the two names.
    If it does, return it, else return None.
    """
    def t(n1, n2):
        return TagRelation.objects.get(tag_to__name = n1, tag_from__name = n2)
    
    try:
      return t(name1, name2)
    except TagRelation.DoesNotExist:
      try:
        return t(name2, name1)
      except TagRelation.DoesNotExist:
        pass
    return None
#################################

def getTopArtists():
  '''
  Calls api method "chart.getTopArtists"
  Stores artist names in list
  '''
  topArtists = unirest.post(api_url, headers={"Accept":"application/json"}, params={"api_key":settings.API_KEY, "method":"chart.gettopartists", "format":"json", "limit":"2"})
  result = topArtists.body
  
  # making a list of artist names from chart.getTopArtists
  for a in result["artists"]["artist"]:
    print a["name"]
    artists.append(a["name"])
#################################

def artistRelation(artists):    
  # for each artist, compile a list of tuples with their tag information, save tags to database, create combinations, calc, create TagRelation, and save TagRelation
  for a in artists:
    print "calculating relations for .... " + str(a)
    artistsTags = unirest.post(api_url, headers={"Accept":"application/json"}, params={"api_key":settings.API_KEY, "artist":a, "method":"artist.getTopTags", "format":"json"})
    tag_body = artistsTags.body

    # empty list to store tag tuples [(name, count), (name, count),..., (name, count)]
    tag_list = []
      
      
    for tag_dict in tag_body["toptags"]["tag"][:10]:
      tag_tuple = (tag_dict["name"], int(tag_dict["count"]))
      tag_list.append(tag_tuple)
      
      # add tag to database
      #new_tag, created = Tag.objects.get_or_create(name=tag_tuple[0], count=tag_tuple[1])
      new_tag, created = Tag.objects.get_or_create(name=tag_tuple[0])
      if created == False:
        print str(new_tag.name) + " already exists"
        new_tag.count =  tag_tuple[1]
      else: 
        print str(new_tag.name) + " now created"

    calcGroup(tag_list)
#################################


