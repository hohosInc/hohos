from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
 

@python_2_unicode_compatible
class Activity(models.Model):
    LIKE = 'L'
    LIKE_PROFILE = 'LP' 
    WROTE_ON_PROFILE = 'WP'  # when a users write on other user's profile
    CHALLENGED = 'CHL'       # when some user challenges to other users 
    RESPOND = 'RSPND'      # when user respondes to other users challenge
    RESPOND_INDIRECT = 'RESPDIND'
    ACTIVITY_TYPES = ( 
        (LIKE, 'Like'), 
        (LIKE_PROFILE,'Like Profile'),
        (WROTE_ON_PROFILE, 'WP'),
        (CHALLENGED, 'CHL'),
        (RESPOND, 'RSPND'),
        (RESPOND_INDIRECT, 'RESPDIND'),
        )  

    user = models.ForeignKey(User)   # this is the user who performs activity
    activity_type = models.CharField(max_length=5, choices=ACTIVITY_TYPES) # type of activity
    date = models.DateTimeField(auto_now_add=True)          # time when activity occured
    feed = models.IntegerField(null=True, blank=True)       # the post involved in activity 
    profile = models.IntegerField(null=True, blank=True)   # this profile is of the user to whome the activity is made

    class Meta:  
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.activity_type


@python_2_unicode_compatible
class Notification(models.Model):
    LIKED = 'L'                 #post_likes
    LIKED_PROFILE = 'LP'        # profile_likes , substitute of follow as other sites
    COMMENTED = 'C' 
    ALSO_COMMENTED = 'S'
    #newly added
    WROTE_ON_PROFILE = 'WP'   
    CHALLENGED = 'CHL'
    RESPOND = 'RSPND'
    RESPOND_INDIRECT = 'RESPDIND'

    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (LIKED_PROFILE,'Liked Profile'),
        (COMMENTED, 'Commented'),
        (ALSO_COMMENTED, 'Also Commented'),
        (WROTE_ON_PROFILE, 'WP'), 
        (CHALLENGED, 'CHL'),
        (RESPOND, 'RSPND'),
        (RESPOND_INDIRECT, 'RESPDIND'),
        )

    #profile liked template
    _LIKED_TEMPLATE_PROFILE = '<a href="/{0}/">{1}</a> liked you, Now {1} can write on your profile, stop <a href="/{0}/">{1}</a>'  # noqa: E501
    _LIKED_TEMPLATE = '<a href="/{0}/">{1}</a> liked your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> commented on your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _ALSO_COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> also commentend on the post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501

    #wrote on your profile template
    _WROTE_ON_PROFILE_TEMPLATE = '<a href="/{0}/">{1}</a> wrote <a href="/feeds/{2}/">{3}</a> on your profile, {1} seems to like you very much!'  
    # user A -> B  A challenged to B
    _CHALLENGED_TEMPLATE = '<a href="/{0}/">{1}</a> Challenged you <a href="/feeds/{2}/">{3}</a>, If you can you do it better?'  
    # user B -> A  B responded to A
    _RESPOND_TEMPLATE = '<a href="/{0}/">{1}</a> Imitated your Style <a href="/feeds/{2}/">{3}</a>'  
    # user others -> A   Others responded to A, which was for B
    _RESPOND_INDIRECT_TEMPLATE = '<a href="/{0}/">{1}</a> Imitated a style <a href="/feeds/{2}/">{3}</a>, which was originally for you.' 

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey('feeds.Feed', null=True, blank=True)
    profile = models.ForeignKey('authentication.Profile', null=True, blank=True)
    notification_type = models.CharField(max_length=5,
                                         choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification' 
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        #wrote on profile notifications
        if self.notification_type == self.WROTE_ON_PROFILE:
            return self._WROTE_ON_PROFILE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                ) 
        #challenged notification
        elif self.notification_type == self.CHALLENGED:
            return self._CHALLENGED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        #responded notification 
        elif self.notification_type == self.RESPOND:
            return self._RESPOND_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        #responded indirectly notification         
        elif self.notification_type == self.RESPOND_INDIRECT:
            return self._RESPOND_INDIRECT_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                ) 

        #added for notifications on profiles like 
        elif self.notification_type == self.LIKED_PROFILE:
            return self._LIKED_TEMPLATE_PROFILE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                # escape(self.to_user.username),
                # self.profile.pk,
                # escape(self.get_summary(self.profile.user.username))
                )
            #end profile likes notifications
        elif self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )           
        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return '{0}...'.format(value[:summary_size])

        else:
            return value
