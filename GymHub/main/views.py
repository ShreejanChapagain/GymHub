from django.shortcuts import render
from . import models
from . import forms
from django.db.models import Count
import stripe
from django.shortcuts import redirect
from django.template.loader import get_template
from django.core import serializers
from django.http import JsonResponse
from datetime import timedelta




#homepage
def home(request):
    banner = models.Banner.objects.all()
    services = models.Service.objects.all()[:3]
    gimgs = models.GalleryImage.objects.all().order_by('-id')[:9]

    return render(request, 'home.html', {'banner': banner, 'services': services, 'gimgs': gimgs})


# PageDetail
def page_detail(request,id):
	page=models.Page.objects.get(id=id)
	return render(request, 'page.html',{'page':page})
#FAQ
def faq_list(request):
	faq=models.Faq.objects.all()
	return render(request, 'faq.html',{'faq':faq})

# Enquiry
def enquiry(request):
	msg=''
	if request.method=='POST':
		form=forms.EnquiryForm(request.POST)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=forms.EnquiryForm
	return render(request, 'enquiry.html',{'form':form,'msg':msg})

# Show galleries
def gallery(request):
	gallery=models.Gallery.objects.all().order_by('-id')
	return render(request, 'gallery.html',{'gallerys':gallery})

# Show gallery photos
def gallery_detail(request,id):
	gallery=models.Gallery.objects.get(id=id)
	gallery_imgs=models.GalleryImage.objects.filter(gallery=gallery).order_by('-id')
	return render(request, 'gallery_imgs.html',{'gallery_imgs':gallery_imgs,'gallery':gallery})


# Subscription Plans
def pricing(request):
	pricing=models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
	dfeatures=models.SubPlanFeature.objects.all();
	return render(request, 'pricing.html',{'plans':pricing,'dfeatures':dfeatures})
	
# SignUp
def signup(request):
    msg = None
    if request.method == 'POST':
        form = forms.Signup(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Thank you for registering.'
    else:
        form = forms.Signup()
    return render(request, 'registration/signup.html', {'form': form, 'msg': msg})

# Checkout
def checkout(request,plan_id):
	planDetail=models.SubPlan.objects.get(pk=plan_id)
	return render(request, 'checkout.html',{'plan':planDetail})

stripe.api_key='sk_test_51OpBhNSB2N5bDLgLhf25MrdktEHKdXRI4n4prI0YajboUFWUSkO2Di262WWQX3jf8LiNY8bdQNODc5du3yfpjsuz00zIpiAVB8'
def checkout_session(request, plan_id):
    plan = models.SubPlan.objects.get(pk=plan_id)

    # Assuming each SubPlan has a corresponding PlanDiscount
    # plan_discount = models.PlanDiscount.objects.get(subplan=plan)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'npr',
                'product_data': {
                    'name': plan.title,
                },
                'unit_amount': (plan.price) * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/pay_cancel',
        client_reference_id=plan_id
    )

    return redirect(session.url, code=303)

# Success
from django.core.mail import EmailMessage

def pay_success(request):
	session = stripe.checkout.Session.retrieve(request.GET['session_id'])
	plan_id=session.client_reference_id
	plan=models.SubPlan.objects.get(pk=plan_id)
	user=request.user
	models.Subscription.objects.create(
		plan=plan,
		user=user,
		price=plan.price
	)
	subject='Order Email'
	html_content=get_template('orderemail.html').render({'title':plan.title})
	from_email='tom65803@gmail.com'

	msg = EmailMessage(subject, html_content, from_email, ['tate@gmail.com'])
	msg.content_subtype = "html"  # Main content is now text/html
	msg.send()

	return render(request, 'success.html')

def pay_cancel(request):
	return render(request, 'cancel.html')


# User Dashboard Section Start
# User Dashboard Section Start
def user_dashboard(request):
	current_plan=models.Subscription.objects.get(user=request.user)
	my_trainer=models.AssignSubscriber.objects.get(user=request.user)
	enddate=current_plan.reg_date+timedelta(days=current_plan.plan.validity_days)




	data=models.Notify.objects.all().order_by('-id')
	notifStatus=False
	jsonData=[]
	totalUnread=0
	for d in data:
		try:
			notifStatusData=models.NotifUserStatus.objects.get(user=request.user,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifUserStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1
		
	return render(request, 'user/dashboard.html',{'current_plan':current_plan, 'my_trainer':my_trainer,'total_unread':'totalUnread','enddate':enddate

	})
# Edit Form
# Edit Form
def update_profile(request):
	msg=None
	if request.method=='POST':
		form=forms.ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=forms.ProfileForm(instance=request.user)
	return render(request, 'user/update-profile.html',{'form':form,'msg':msg})


# trainer login
def trainerlogin(request):
	msg=''
	if request.method=='POST':
		username=request.POST['username']
		pwd=request.POST['pwd']
		trainer=models.Trainer.objects.filter(username=username,pwd=pwd).count()
		if trainer > 0:
			request.session['trainerLogin']=True
			return redirect('/trainer_dashboard')



			
			
		else:
			msg='Invalid!!'
	form=forms.TrainerLoginForm
	return render(request, 'trainer/login.html',{'form':form,'msg':msg})

# Trainer Logout
def trainerlogout(request):
	del request.session['trainerLogin']
	return redirect('/trainerlogin')


# Notifications
def notifs(request):
	data=models.Notify.objects.all().order_by('-id')
	return render(request, 'notifs.html',{'data':data})
	

# Get All Notifications
def get_notifs(request):
	data=models.Notify.objects.all().order_by('-id')
	notifStatus=False
	jsonData=[]
	totalUnread=0
	for d in data:
		try:
			notifStatusData=models.NotifUserStatus.objects.get(user=request.user,notif=d)
			if notifStatusData:
				notifStatus=True
		except models.NotifUserStatus.DoesNotExist:
			notifStatus=False
		if not notifStatus:
			totalUnread=totalUnread+1
		jsonData.append({
				'pk':d.id,
				'notify_detail':d.notify_detail,
				'notifStatus':notifStatus
			})
	return JsonResponse({'data':jsonData,'totalUnread':totalUnread})
# Markas Read Notification By User
# Mark Read By user
def mark_read_notif(request):
	notif=request.GET['notif']
	notif=models.Notify.objects.get(pk=notif)
	user=request.user
	models.NotifUserStatus.objects.create(notif=notif,user=user,status=True)
	return JsonResponse({'bool':True})