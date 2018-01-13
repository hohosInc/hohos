# from django.db import models

# # Create your models here.


# class SignUp(models.Model):
# 	email = models.EmailField()
# 	full_name = models.CharField(max_length=120,blank=True, null=True)  # blank means required or not
# 	time_stamp = models.DateTimeField(auto_now_add=True, auto_now=False)
# 	updated = models.DateTimeField(auto_now_add=False , auto_now=True)

# 	def __unicode__(self):    # for python 3   __str__()
# 		return self.email
# 		# only strings could be returned as the name
# 		# so u can use str(time_stamp) or anything else like this

