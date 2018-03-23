from __future__ import unicode_literals

import hashlib 
import os.path 
import urllib   
     
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models 
from django.db.models.signals import post_save 
from django.utils.encoding import python_2_unicode_compatible
# from imagekit.models import ProcessedImageField
from activities.models import Notification 
from activities.models import Activity

from django.core.cache import cache 
import datetime


        
@python_2_unicode_compatible      
class Profile(models.Model):     
    user = models.OneToOneField(User)  
    status = models.CharField(max_length=200, null=True, blank=True) 
    about = models.TextField(max_length=250, null=True, blank=True)

    #hohos_digest  
    hohos_digest = models.BooleanField(default=True)

    is_product = models.BooleanField(default=False)
    company = models.CharField(max_length=100, null=True, blank=True)
    facebook = models.CharField(max_length=150, null=True, blank=True)
    quora = models.CharField(max_length=150, null=True, blank=True)
    twitter = models.CharField(max_length=150, null=True, blank=True)
    linkedin = models.CharField(max_length=150, null=True, blank=True)
 
    likes = models.IntegerField(default=1)
    likes_to = models.IntegerField(default=1)
    home = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    job = models.CharField(verbose_name="what are you doing now?", max_length=100, null=True, blank=True) 
    institute = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True) # launch_date for product
    gender = models.CharField(max_length=10, null=True, blank=True)
    want_to_do = models.CharField(verbose_name="what do you want to do?", max_length=200, null=True, blank=True)
    likes_most = models.CharField(verbose_name="who do you like most?", max_length=150, null=True, blank=True)
    likes_not = models.CharField(verbose_name="who do you like not at all?", max_length=150, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pictures',
                                # format='JPEG',
                                # options={ 'quality': 100},
                                null=True,
                                blank=True,
            height_field="height_field",
            width_field="width_field")
    height_field = models.IntegerField(default=450)
    width_field = models.IntegerField(default=350)

    class Meta: 
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username

    def get_website(self):
        url = self.website
        if "http://" not in self.website and "https://" not in self.website and len(self.website) > 0:  # noqa: E501
            url = "http://" + str(self.website)
        return url

    def get_facebook(self):
        url = self.facebook
        if "http://" not in self.facebook and "https://" not in self.facebook and len(self.facebook) > 0:  # noqa: E501
            url = "http://" + str(self.facebook)
        return url

    def get_quora(self):
        url = self.quora
        if "http://" not in self.quora and "https://" not in self.quora and len(self.quora) > 0:  # noqa: E501
            url = "http://" + str(self.quora)
        return url

    def get_twitter(self):
        url = self.twitter
        if "http://" not in self.twitter and "https://" not in self.website and len(self.twitter) > 0:  # noqa: E501
            url = "http://" + str(self.twitter)
        return url

    def get_linkedin(self):
        url = self.linkedin
        if "http://" not in self.linkedin and "https://" not in self.linkedin and len(self.linkedin) > 0:  # noqa: E501
            url = "http://" + str(self.linkedin)
        return url

    def get_picture(self):
        #print('settings.MEDIA_URL,self.image',settings.MEDIA_URL,self.image)
        no_picture = settings.MEDIA_URL + 'profile_pictures/' + 'no_picture.png'
        gender = self.gender
        if self.image:
            return settings.MEDIA_URL+str(self.image)
        elif gender:
            if gender.lower() == 'male':
                return settings.MEDIA_URL + 'profile_pictures/' + 'male.png'
            elif gender.lower() == 'female': 
                return settings.MEDIA_URL + 'profile_pictures/' + 'female.png'
            elif gender == 'Gender':
                return no_picture
        else:
            return no_picture

    def get_screen_name(self): 
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    #profile like secion
    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE_PROFILE,
                                        profile=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE_PROFILE,
                                        profile=self.pk)
        return likes

    def calculate_likes_to(self):
        users = User.objects.all()
        likes_to = 1
        for user in users:
            if self.user in user.profile.get_likers():
                likes_to+=1
        self.likes_to = likes_to
        self.save()
        return likes_to

    def get_likes_to_users(self):
        users = User.objects.all()
        likes_to_users = []
        try:
            for user in users:
                if self.user in user.profile.get_likers():
                    likes_to_users.append(user)
        except:
            likes_to_users = likes_to_users
        return likes_to_users

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers

    # profile like notifications 
    def notify_liked_profile(self, profile):
        if self.user != profile.user:
            Notification(notification_type=Notification.LIKED_PROFILE,
                         from_user=self.user, to_user=profile.user,
                         profile=profile).save()

    def unotify_liked_profile(self, profile):
        if self.user != profile.user:
            Notification.objects.filter(notification_type=Notification.LIKED_PROFILE,
                                        from_user=self.user, to_user=profile.user,
                                        profile=profile).delete()

    # end profile like section

    # wrote on profile section _made_on_18_08_2017

    def notify_wrote_on_profile(self,profile,feed):
        if self.user!= profile.user:
            Notification(notification_type=Notification.WROTE_ON_PROFILE,
                         from_user=self.user, to_user=profile.user,
                         profile=profile, feed=feed,
                        ).save()

    #No need of un notifying(deleting the post manually on deletion of that post), 
    #because the notification already get deleted on deleting the post
    # end profile writing section

    def notifyChallenged(self,profile,feed):
        if self.user!=profile.user:
            Notification(notification_type=Notification.CHALLENGED,
                         from_user=self.user, to_user=profile.user,
                         profile=profile, feed=feed,
                        ).save()

    def notifyResponded(self,profile,feed):
        if self.user!=profile.user:
            Notification(notification_type=Notification.RESPOND,
                         from_user=self.user, to_user=profile.user,
                         profile=profile, feed=feed,
                        ).save()

    def notifyRespondedIndirect(self,profile,feed):
        if self.user!=profile.user:
            Notification(notification_type=Notification.RESPOND_INDIRECT,
                         from_user=self.user, to_user=profile.user,
                         profile=profile, feed=feed,
                        ).save()

    #end of object creation for challenge and response related notifications

    def notify_liked(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.LIKED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def unotify_liked(self, feed):
        if self.user != feed.user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                                        from_user=self.user, to_user=feed.user,
                                        feed=feed).delete()

    def notify_commented(self, feed):  
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)

        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                         from_user=self.user,
                         to_user=User(id=user), feed=feed).save()


    #checking active users 
    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
            



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()

#post_save.connect(create_user_profile, sender=User)
#post_save.connect(save_user_profile, sender=User)



   




       # def unotify_wrote_on_profile(self,profile,feed):
    #     if self.user!= profile.user:
    #         Notification.objects.filter(notification_type=Notification.WROTE_ON_PROFILE,
    #                      from_user=self.user, to_user=profile.user,
    #                      profile=profile, feed=feed,
    #                     ).delete()
