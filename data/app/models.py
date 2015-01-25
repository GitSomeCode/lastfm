from django.db import models


class Tag(models.Model):
  name = models.CharField(max_length = 30, default = "", blank = False)
  count = models.IntegerField(default = 0, blank = False)
  
  def __unicode__(self):
    return "%s" %(self.name[:24])
  
  
