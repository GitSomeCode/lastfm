from django.db import models


class Tag(models.Model):
  name = models.CharField(max_length = 30, default = "", blank = False)
  count = models.IntegerField(default = 0, blank = False)
  relation = models.ManyToManyField("self", symmetrical=False, through='TagRelation')
  
  def __unicode__(self):
    return "%s" %(self.name[:24])
  
class TagRelation(models.Model):
  tag_to = models.ForeignKey('Tag', blank = False, related_name="tag_to")
  tag_from = models.ForeignKey('Tag', blank = False, related_name="tag_from")
  metric = models.FloatField(default = 0.0000, blank = False)
  
  class Meta:
    unique_together = ('tag_to', 'tag_from')
  
  def __unicode__(self):
    return "%s" %(self.tag_to.name + " : " + self.tag_from.name)
  