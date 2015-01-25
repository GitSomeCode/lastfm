from django.db import models


class Quote(models.Model):
  name = models.CharField(max_length = 30, default = "", blank = False)
  text = models.CharField(max_length = 200, blank = False)
  
  def __unicode__(self):
    return "%s" %(self.name[:24])
