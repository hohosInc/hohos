from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models 
from django.utils.encoding import python_2_unicode_compatible 
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

import bleach 
from authentication.models import Profile
from activities.models import Activity 
   
     
@python_2_unicode_compatible     
class Feed(models.Model):  
    user = models.ForeignKey(User, related_name="from_user", null=True) 
    to_user = models.ForeignKey(User, related_name="for_user", null=True, blank=True) #respond_to_user
    challenge_to_user = models.ForeignKey(User, related_name="challenge_to_user", null=True, blank=True)
    profile_pk = models.IntegerField(default=None, null=True, blank=True)
    is_product_feed = models.BooleanField(default=False)   #product_profile_feeds atleast one user or to_user is product for such feeds
    is_challenge = models.BooleanField(default=False)
    response_for = models.IntegerField(default=None, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)
    post_pic = models.ImageField(null=True, blank=True, 
            height_field="height_field",
            width_field="width_field")    
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)  
    parent = models.ForeignKey('Feed', null=True, blank=True)   
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
  
    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
        ordering = ('-date',)

    def __str__(self):
        return self.post 

    # def optimize_image(self):
        

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            feeds = Feed.objects.filter(parent=None, id__lte=from_feed)
        else:
            feeds = Feed.objects.filter(parent=None)
        return feeds

    @staticmethod
    def get_feeds_after(feed):
        feeds = Feed.objects.filter(parent=None, id__gt=feed)
        return feeds

    def get_comments(self):
        return Feed.objects.filter(parent=self).order_by('-date')

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE,
                                        feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE,
                                        feed=self.pk)
        return likes

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers
  
    def calculate_comments(self):
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return self.comments

    def comment(self, user, post):
        feed_comment = Feed(user=user, post=post, parent=self)
        feed_comment.save()
        self.comments = Feed.objects.filter(parent=self).count()
        self.save()
        return feed_comment

    def linkfy_post(self):
        return bleach.linkify(escape(self.post))  

class Photo(models.Model):
    file = models.FileField(upload_to='photos/')


