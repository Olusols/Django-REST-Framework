from django.db import models
from django.utils import timezone

class TestApp(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=60, editable=False, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'TestApp'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        self.slug = slugify(self.name)
        
        super(TestApp, self).save(*args, **kwargs)
        

    
class Relate(models.Model):
    relation = models.ForeignKey(TestApp, related_name='test', on_delete=models.CASCADE, null=True)
    scor = models.IntegerField()
    alive = models.BooleanField()   
    
    def __str__(self):
        return self.relation.name


########### POLLS ############
from django.contrib.auth.models import User

class Poll(models.Model):
   question = models.CharField(max_length=100)
   created_by = models.ForeignKey(User, on_delete=models.CASCADE)
   pub_date = models.DateTimeField(auto_now=True)
   def __str__(self):
       return self.question
   
   
class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    
    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
       unique_together = ("poll", "voted_by")

