from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Banner(models.Model):
    img = models.ImageField(upload_to="banners/")
    alt_text = models.CharField(max_length=150)

    def __str__(self):
        return self.alt_text

    def image_tag(self):
        return mark_safe('<img src="%s" width="80" />' % (self.img.url))
class Service(models.Model):
	title=models.CharField(max_length=150)
	detail=models.TextField()
	img=models.ImageField(upload_to="services/",null=True)

	def __str__(self):
		return self.title

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))

    
#pages
class Page(models.Model):
      title=models.CharField(max_length=200)
      detail=models.TextField()

      def __str__(self):
            return self.title

class Faq(models.Model):
      quest=models.TextField()
      ans=models.TextField()

      def __str__(self):
            return self.quest
      # Enquiry Model
class Enquiry(models.Model):
	full_name=models.CharField(max_length=150)
	email=models.CharField(max_length=150)
	detail=models.TextField()
	send_time=models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.full_name
      

# Gallery Model
class Gallery(models.Model):
	title=models.CharField(max_length=150)
	detail=models.TextField()
	img=models.ImageField(upload_to="gallery/",null=True)

	def __str__(self):
		return self.title

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))
	# Gallery Images
class GalleryImage(models.Model):
	gallery=models.ForeignKey(Gallery, on_delete=models.CASCADE,null=True)
	alt_text=models.CharField(max_length=150)
	img=models.ImageField(upload_to="gallery_imgs/",null=True)

	def __str__(self):
		return self.alt_text

	def image_tag(self):
		return mark_safe('<img src="%s" width="80" />' % (self.img.url))
	# Subscription Plans
class SubPlan(models.Model):
	title=models.CharField(max_length=150)
	price=models.IntegerField()
	max_member=models.IntegerField(null=True)
	validity_days=models.IntegerField(null=True)

	highlight_status=models.BooleanField(default=False, null=True) 

	def __str__(self):
		return self.title

# Subscription Plans Features
class SubPlanFeature(models.Model):
	##subplan=models.ForeignKey(SubPlan, on_delete=models.CASCADE)
	subplan=models.ManyToManyField(SubPlan)
	title=models.CharField(max_length=150)

	def __str__(self):
		return self.title
	
	# Package Discounts
class PlanDiscount(models.Model):
	subplan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
	total_months=models.IntegerField()
	total_discount=models.IntegerField()

	def __str__(self):
		return str(self.total_months)
	

# Subscriber
class Subscriber(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	mobile=models.CharField(max_length=20)
	address=models.TextField()
	img=models.ImageField(upload_to="subs/",null=True)

	def __str__(self):
		return str(self.user)

	def image_tag(self):
		if self.img:
			return mark_safe('<img src="%s" width="80" />' % (self.img.url))
		else:
			return 'no-image'

@receiver(post_save,sender=User)
def create_subscriber(sender,instance,created,**kwrags):
	if created:
		Subscriber.objects.create(user=instance)

	 

    # Subscription
class Subscription(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	plan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
	price=models.CharField(max_length=50)
	reg_date=models.DateField(auto_now_add=True,null=True)

class Trainer(models.Model):
	full_name=models.CharField(max_length=100)
	username=models.CharField(max_length=100,null=True)
	pwd=models.CharField(max_length=50,null=True)
	mobile=models.CharField(max_length=100)
	address=models.TextField()
	is_active=models.BooleanField(default=False)
	detail=models.TextField()
	img=models.ImageField(upload_to="trainers/")
	def __str__(self):
		return str(self.full_name)

	def image_tag(self):
		if self.img:
			return mark_safe('<img src="%s" width="80" />' % (self.img.url))
		else:
			return 'no-image'

	
# Notifications Json Response Via Ajax
class Notify(models.Model):
	notify_detail=models.TextField()
	read_by_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
	read_by_trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return str(self.notify_detail)
	
# Markas Read Notification By User
class NotifUserStatus(models.Model):
	notif=models.ForeignKey(Notify, on_delete=models.CASCADE)
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	status=models.BooleanField(default=False)

	class Meta:
		verbose_name_plural='Notification Status'


	
# Assign Subscriber to Trainer
class AssignSubscriber(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	trainer=models.ForeignKey(Trainer, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user)


