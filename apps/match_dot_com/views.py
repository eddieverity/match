from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import HttpResponseForbidden
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from slugify import slugify
import os
import re
import bcrypt
import math
from models import *
from django.db.models import Q
from .forms import *
from translator import translate
import requests
from urllib2 import urlopen
import json
from order_dict import *


# Create your views here.
def index(request):
  if 'id' in request.session:
    id = request.session['id']
    try:
      context = {
        'others': User.objects.exclude(id=id),
        'me': User.objects.get(id=id),
        'profiles': Profile.objects.exclude(user=id),
        'images': Images.objects.all().order_by('user'),
        'seeking': Seeking.objects.get(seeking_user=id),
      }
      return render (request, 'match_dot_com/index.html', context)
    except:
      messages.error(request, 'Finish survey to see matches.')
      return redirect('match:survey_seeking')
  return redirect ('match:login')

def survey(request):
  if request.method=='POST':
    my_id = request.session['id']

    user_gender = request.POST.get('user_gender', None)
    user_age = request.POST.get('age', None)
    user_height_total = request.POST.get('valueA', None)
    user_body_type = request.POST.get('user_bodytype', None)
    user_relationship_status = request.POST.get('user_status', None)
    user_marriage = request.POST.get('user_marriage', None)
    user_current_kids = request.POST.get('user_currkids', None)
    user_future_kids = request.POST.get('user_futurekids', None)
    user_education = request.POST.get('user_edu', None)
    user_smoke = request.POST.get('user_smoke', None)
    user_drink = request.POST.get('user_drink', None)
    user_religion = request.POST.get('user_religion', None)
    user_salary = request.POST.get('user_salary', None)
    bio = request.POST['bio']

    activity=0
    frugality=0
    pragmaticism=0
    family=0

    if type(user_current_kids) == int:
      family+=int(user_current_kids)
    if type(user_future_kids) == int:
      family+=int(user_future_kids)
    if type(user_marriage) == int:
      family+=int(user_marriage)
    
    user_interests = request.POST.getlist('user_interests')
    for interest in user_interests:
      if interest == 'book-club':
        activity -=1
        frugality -=1
      if interest == 'camping':
        activity +=1
        frugality -=1
        pragmaticism -=1
      if interest == 'coffee':
        activity -=1
        frugality -=1
      if interest == 'networking':
        pragmaticism -=1
        activity +=1
      if interest == 'cooking':
        activity -=1
        frugality -=1
        pragmaticism +=1
      if interest == 'dining-out':
        activity +=1
        frugality +=1
      if interest == 'fishing-hunting':
        activity +=1
        pragmaticism -=1
        family -=1
      if interest == 'gardening':
        frugality -=1
        pragmaticism +=1
      if interest == 'hobbies':
        pragmaticism +=1
      if interest == 'movies':
        activity -=1
        frugality -=1
      if interest == 'museums':
        activity +=1
        pragmaticism +=1
      if interest == 'music':
        pragmaticism +=1
      if interest == 'exploring':
        activity +=1
        frugality +=1
      if interest == 'nightclubs':
        activity +=1
        frugality +=1
      if interest == 'performing-arts':
        pragmaticism +=1
      if interest == 'cards':
        frugality+=1
        activity-=1
      if interest == 'playing-sports':
        activity+=1
      if interest == 'political':
        pragmaticism-=1
      if interest == 'shopping':
        frugality+=1
      if interest == 'travel':
        frugality+=1
        activity+=1
      if interest == 'video-games':
        activity-=1
      if interest == 'volunteering':
        activity+=1
        family+=1
      if interest == 'watching-sports':
        activity-=1
      if interest == 'wine':
        frugality+=1
        pragmaticism+=1   

    try:
      curr_user= Profile.objects.create(
        user_id=my_id,
        gender=user_gender,
        age=user_age,
        height=user_height_total,
        body=user_body_type,
        relationship_status=user_relationship_status,
        current_kids=user_current_kids,
        future_kids=user_future_kids,
        education=user_education,
        smoke=user_smoke,
        drink=user_drink,
        religion=user_religion,
        salary=user_salary,
        activity=activity,
        frugality=frugality,
        pragmaticism=pragmaticism,
        family=family
        )
    except:
      messages.error(request, 'Age, Gender & Height are required fields!')
      return redirect('match:survey')
    User.objects.filter(id=my_id).update(bio=bio)

    return redirect('match:survey_seeking')
  return render(request, 'match_dot_com/survey.html')

def survey_seeking(request):
  return render(request, 'match_dot_com/survey_seeking.html')

def seeking_entry(request):

  my_id = request.session['id']

  seeking_gender = request.POST.get('seeking_gender', None)

  seeking_age_min = request.POST.get('age_min', None)
  seeking_age_max = request.POST.get('age_max', None)

  seeking_height_min = request.POST.get('min_height', None)
  seeking_height_max = request.POST.get('max_height', None)

  seeking_body_type = request.POST.get('seeking_bodytype', None) 
  deal_seeking_body_type = 0
  if 'deal_seeking_body_type' in request.POST:
    deal_seeking_body_type = 1
  
  seeking_relationship_status = request.POST.get('seeking_status', None)
  deal_seeking_relationship_status = 0
  if 'deal_seeking_relationship_status' in request.POST:
    deal_seeking_relationship_status = 1

  seeking_current_kids = request.POST.get('seeking_currkids', None)
  deal_current_kids = 0
  if 'deal_current_kids' in request.POST:
    deal_current_kids = 1

  seeking_future_kids = request.POST.get('seeking_future_kids', None)
  deal_seeking_kids = 0
  if 'deal_seeking_kids' in request.POST:
    deal_seeking_kids = 1


  seeking_education = request.POST.get('seeking_education', None)
  deal_seeking_education = 0
  if 'deal_seeking_education' in request.POST:
    deal_seeking_education = 1

  seeking_smoke = request.POST.get('seeking_smoke', None)
  deal_seeking_smoke = 0
  if 'deal_seeking_smoke' in request.POST:
    deal_seeking_smoke = 1

  seeking_drink = request.POST.get('seeking_drink', None)
  deal_seeking_drink = 0
  if 'deal_seeking_drink' in request.POST:
    deal_seeking_drink = 1
  

  seeking_religion = request.POST.get('seeking_religion', None)
  deal_seeking_religion = 0
  if 'deal_seeking_religion' in request.POST:
    deal_seeking_religion = 1


  seeking_salary = request.POST.get('seeking_salary', None) 
  deal_seeking_salary = 0
  if 'deal_seeking_salary' in request.POST:
    deal_seeking_salary = 1

  try:  
    seek_user= Seeking.objects.create(
      seeking_user_id=my_id,
      gender=seeking_gender,
      age_min=seeking_age_min,
      age_max=seeking_age_max,
      height_min=seeking_height_min,
      height_max=seeking_height_max,
      body=seeking_body_type,
      deal_body=deal_seeking_body_type,
      relationship_status=seeking_relationship_status,
      deal_relationship_status=deal_seeking_relationship_status,
      current_kids=seeking_current_kids,
      deal_current_kids=deal_current_kids,
      future_kids=seeking_future_kids,
      deal_future_kids=deal_seeking_kids,
      education=seeking_education,
      deal_education=deal_seeking_education,
      smoke=seeking_smoke,
      deal_smoke=deal_seeking_smoke,
      drink=seeking_drink,
      deal_drink=deal_seeking_drink,
      religion=seeking_religion,
      deal_religion=deal_seeking_religion,
      salary=seeking_salary,
      deal_salary=deal_seeking_salary
    )
  except:
    messages.error(request, 'Age, Gender & Height are required fields!')
    return redirect('match:survey_seeking')
  return redirect('match:index')

def login(request):
  
  if request.POST:
    l_email=request.POST['l_email']

    try:
      curr_user=User.objects.get(email = l_email)
      l_password=request.POST['l_password'].encode(encoding="utf-8")
      if bcrypt.hashpw(l_password, curr_user.password.encode("utf-8")) == curr_user.password:
        request.session['first_name']=curr_user.first_name
        request.session['id']=curr_user.id
        try:
          user_survey= Profile.objects.get(user_id=curr_user.id)
          return redirect('match:index')
        except:
          return render(request, 'match_dot_com/survey.html')
        
      else:
        messages.error(request, 'Incorrect password')
        return redirect('match:register')
    except User.DoesNotExist:
      messages.error(request, 'No account with that email address. Please register')
    return redirect('match:register')
  return render(request, 'match_dot_com/registration_login.html')

def register(request):
  if request.POST:
    is_valid = True
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    confirm = request.POST['confirm'] 
    password = request.POST['password'].encode(encoding="utf-8")
    pw_hash=bcrypt.hashpw(password, bcrypt.gensalt())
    if ValidateEmail(email) != True:
      messages.warning(request, 'email address not valid')
      is_valid = False
    if DupEmail(email):
      messages.warning(request, 'email address in use')
      is_valid= False
    if len(first_name) < 2:
      messages.warning(request, 'name must be at least 2 characters long')
      is_valid = False
    if len(last_name) < 2:
      messages.warning(request, 'name must be at least 2 characters long')
      is_valid = False
    if len(password) < 8:
      messages.warning(request, 'password must be at least 8 characters long')
      is_valid = False
    if password != confirm:
      messages.warning(request, 'passwords do not match')
      is_valid = False
    if is_valid:
      curr_user= User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        zipcode=request.POST['zipcode'],
        password= pw_hash
        )
      Images.objects.create(user=curr_user, user_pic="default.png")
      request.session['first_name']=request.POST['first_name']
      request.session['id']=curr_user.id
      return redirect ('match:survey')
    else:
      return redirect('match:login')
  return redirect('match:login')

def ValidateEmail( email ):    
  try:
    validate_email( email )
    return True
  except ValidationError:
    return False

def badname_regex(name):
  reggie=re.compile(r'^[a-zA-Z]+$')
  if reggie.match(name) is None:
    return True

def DupEmail(email):
  try:
    User.objects.get(email = email)
    return True
  except User.DoesNotExist:
    return False

def matchmsg(request):
  if 'id' in request.session:
    id = request.session['id']
    context = {
      'others': User.objects.exclude(id=id),
      'messages': Messages.objects.filter(recipient=id).order_by('-created_at'),
    }
    return render(request, 'match_dot_com/messages.html', context)
  return redirect('match:login')

def messenger(request, id):
  if 'id' in request.session:
    userid = request.session['id']
    context = {
      'others': User.objects.get(id=id),
      'pastmessages': Messages.objects.filter(Q(sender=id, recipient=userid) | Q(recipient=id, sender=userid)).order_by('created_at'),
    }
    if request.method == 'POST':
      user_id = User.objects.get(id=request.session['id'])
      other_id = User.objects.get(id=id)
      message_text = request.POST['message_text']
      Messages.objects.create(sender=user_id, recipient=other_id, description=message_text)

      return render(request, 'match_dot_com/partials.html', context)

    return render(request, 'match_dot_com/messenger.html', context)
  return redirect('match:login')

def user(request, id):
  if 'id' in request.session:
    # try:
    userprofile = User.objects.get(id=id)
    try:
      context = {
        'user': userprofile,
        'photos': Images.objects.filter(user=userprofile),
        'profiledata': Profile.objects.get(user=userprofile),
        'gallery': Gallery.objects.filter(user=userprofile).order_by('-created_at'),
        'seekingdata': Seeking.objects.get(seeking_user=userprofile),
      }
      
      try:
        context['profiledata'].body=translate('body', context['profiledata'].body)
      except:
        context['profiledata'].body='Not Specified'

      try:  
        context['profiledata'].smoke=translate('smoke', context['profiledata'].smoke)
      except:
        context['profiledata'].smoke='Not Specified'
      try:  
        context['profiledata'].current_kids=translate('current_kids', context['profiledata'].current_kids)
      except:
        context['profiledata'].current_kids='Not Specified'
      try:
        context['profiledata'].future_kids=translate('future_kids', context['profiledata'].future_kids)
      except:
        context['profiledata'].future_kids='Not Specified'
      try:
        context['profiledata'].education=translate('education', context['profiledata'].education)
      except:
        context['profiledata'].education='Not Specified'
      try: 
        context['profiledata'].drink=translate('drink', context['profiledata'].drink)
      except:
        context['profiledata'].drink='Not Specified'
      try:
        context['profiledata'].salary=translate('salary', context['profiledata'].salary)
      except:
        context['profiledata'].salary='Not Specified'
      try:
        context['profiledata'].relationship_status=translate('relationship_status', context['profiledata'].relationship_status)
      except:
        context['profiledata'].relationship_status='Not Specified'
      try:
        context['profiledata'].religion=translate('religion', context['profiledata'].religion)
      except:
        context['profiledata'].religion='Not Specified'
      try:
        context['profiledata'].height=translate('height', context['profiledata'].height)
      except:
        context['profiledata'].height='Not Specified'

      return render(request, 'match_dot_com/user.html', context)
    except:
      return redirect('match:index')
    # except:
    #   return redirect('match:survey')
  return redirect('match:login')

def upload_pic(request):
    if request.method == 'POST':
      userid = request.session['id']
      image = request.FILES['user_pic']
      extension = os.path.splitext(image.name)[1]
      image.name = slugify(image.name) + extension
      try:
        Images.objects.create(user_id=userid, user_pic=image)
      except:
        Images.objects.filter(user_id=userid).update(user_pic=image)
      return redirect(reverse('match:user', kwargs={'id': userid}))
    return HttpResponseForbidden('allowed only via POST')

def upload_gallery(request):
    if request.method == 'POST':
      userid = request.session['id']
      image = request.FILES['gallery_pic']
      extension = os.path.splitext(image.name)[1]
      image.name = slugify(image.name) + extension
      Gallery.objects.create(user_id=userid, user_pic=image)
      return redirect(reverse('match:user', kwargs={'id': userid}))
    return HttpResponseForbidden('allowed only via POST')

def gallery(request, id):
  if 'id' in request.session:
    context= {
      'gallery': Gallery.objects.filter(user=id),
      'user': User.objects.get(id=id),
    }
    return render(request,'match_dot_com/gallery.html', context)
  return redirect('match:login')

def regional(request):
  user_id = request.session['id']
  user_prof = User.objects.get(id=user_id)
  user_zip = str(user_prof.zipcode)
  url = 'https://www.zipcodeapi.com/rest/T0rL6kxrFEJyuza4H9jsHeQVheFFxDNrDfcKzJcfnVOSvYWd7gFPvvKMJqsg4gII/radius.json/' + user_zip + '/10/mile'
  try:
    req = urlopen(url)
  except:
    messages.error(request, 'You have an invalid zip code entered, please adjust in your profile')
    return redirect('match:index')
  json_obj = json.load(req)
  locals = [ ]

  otherusers = {
    "others": User.objects.exclude(id=user_id),
  }

  for i in json_obj['zip_codes']:
    for user in otherusers.keys():
      for x in otherusers[user]:
        if int(x.zipcode) == int(i['zip_code']):
          locals.append(x)

  context = {
    'locals': locals,
    'me': User.objects.get(id=user_id),
    'profiles': Profile.objects.exclude(user=user_id).order_by('user'),
    'images': Images.objects.all().order_by('user'), 
  }

  return render(request, 'match_dot_com/regional.html', context)

def editprofile(request, id):
  if 'id' in request.session:
    userid = request.session['id']
    if int(id) == userid:
      context = {
        'user': User.objects.get(id=id),
        'profile': Profile.objects.get(user=id),
        }
      if request.method == 'POST':
        bio = request.POST['bio']
        age = request.POST['age']
        zipcode = request.POST['zipcode']
        height = request.POST['valueA']
        body = request.POST['user_bodytype']
        relationship_status = request.POST['user_status']
        current_kids = request.POST['user_currkids']
        future_kids = request.POST['user_futurekids']
        education = request.POST['user_edu']
        smoke = request.POST['user_smoke']
        drink = request.POST['user_drink']
        religion = request.POST['user_religion']
        salary = request.POST['user_salary']
        Profile.objects.filter(user_id=id).update(
          age=age, 
          height=height, 
          body=body, 
          relationship_status=relationship_status,
          current_kids=current_kids,
          future_kids=future_kids,
          education=education,
          smoke=smoke,
          drink=drink,
          religion=religion,
          salary=salary
          )
        User.objects.filter(id=id).update(bio=bio, zipcode=zipcode)
        return redirect(reverse('match:user', kwargs={'id': userid}))
      return render(request, 'match_dot_com/editprofile.html', context)
    return redirect(reverse('match:user', kwargs={'id': userid}))
  return redirect('match:login')

def editseeking(request, id):
  if 'id' in request.session:
    userid = request.session['id']
    if int(id) == userid:
      try:
        context = {
          'user': User.objects.get(id=id),
          'profile': Seeking.objects.get(seeking_user=id),
          }
        if request.method == 'POST':
          seeking_body_type = request.POST.get('seeking_bodytype', None) 
          deal_seeking_body_type = 0
          if 'deal_seeking_body_type' in request.POST:
            deal_seeking_body_type = 1
          
          seeking_relationship_status = request.POST.get('seeking_status', None)
          deal_seeking_relationship_status = 0
          if 'deal_seeking_relationship_status' in request.POST:
            deal_seeking_relationship_status = 1

          seeking_current_kids = request.POST.get('seeking_current_kids', None)
          deal_current_kids = 0
          if 'deal_current_kids' in request.POST:
            deal_current_kids = 1

          seeking_future_kids = request.POST.get('seeking_future_kids', None)
          deal_seeking_kids = 0
          if 'deal_seeking_kids' in request.POST:
            deal_seeking_kids = 1


          seeking_education = request.POST.get('seeking_education', None)
          deal_seeking_education = 0
          if 'deal_seeking_education' in request.POST:
            deal_seeking_education = 1

          seeking_smoke = request.POST.get('seeking_smoke', None)
          deal_seeking_smoke = 0
          if 'deal_seeking_smoke' in request.POST:
            deal_seeking_smoke = 1

          seeking_drink = request.POST.get('seeking_drink', None)
          deal_seeking_drink = 0
          if 'deal_seeking_drink' in request.POST:
            deal_seeking_drink = 1
          

          seeking_religion = request.POST.get('seeking_religion', None)
          deal_seeking_religion = 0
          if 'deal_seeking_religion' in request.POST:
            deal_seeking_religion = 1


          seeking_salary = request.POST.get('seeking_salary', None) 
          deal_seeking_salary = 0
          if 'deal_seeking_salary' in request.POST:
            deal_seeking_salary = 1
          age_min = request.POST['age_min']
          age_max = request.POST['age_max']
          seeking_gender = request.POST['seeking_gender']
          min_height = request.POST['min_height']
          max_height = request.POST['max_height']
          body = request.POST['seeking_bodytype']
          relationship_status = request.POST['seeking_status']
          current_kids = request.POST['seeking_currkids']
          future_kids = request.POST['seeking_future_kids']
          education = request.POST['seeking_edu']
          smoke = request.POST['seeking_smoke']
          drink = request.POST['seeking_drink']
          religion = request.POST['seeking_religion']
          salary = request.POST['seeking_salary']
          Seeking.objects.filter(seeking_user=id).update(
            age_min=age_min,
            age_max=age_max,
            gender=seeking_gender,
            height_min=min_height, 
            height_max=max_height, 
            body=body, 
            relationship_status=relationship_status,
            current_kids=current_kids,
            future_kids=future_kids,
            education=education,
            smoke=smoke,
            drink=drink,
            religion=religion,
            salary=salary,
            deal_body=deal_seeking_body_type,
            deal_relationship_status=deal_seeking_relationship_status,
            deal_current_kids=deal_current_kids,
            deal_future_kids=deal_seeking_kids,
            deal_education=deal_seeking_education,
            deal_smoke=deal_seeking_smoke,
            deal_drink=deal_seeking_drink,
            deal_religion=deal_seeking_religion,
            deal_salary=deal_seeking_salary,
            )
          return redirect(reverse('match:user', kwargs={'id': userid}))
        return render(request, 'match_dot_com/editseeking.html', context)
      except:
        messages.error(request, 'Please fill out age/gender/height')
        return redirect('match:index')
    return redirect(reverse('match:user', kwargs={'id': userid}))
  return redirect('match:login')


def matchsort(request):


  if 'id' in request.session:
    id = request.session['id']
    active_user=Seeking.objects.get(seeking_user_id=request.session['id'])
    filtertron={}
    
    filtertron['gender'] = active_user.gender

  
    if active_user.deal_body == 1:
      filtertron['body'] = active_user.seeking_body
    if active_user.deal_relationship_status == 1:
      filtertron['relationship_status'] = active_user.relationship_status
    if active_user.deal_current_kids == 1:
      filtertron['current_kids'] = active_user.current_kids
    if active_user.deal_future_kids == 1:
      filtertron['future_kids']= active_user.future_kids
    if active_user.deal_education == 1:
      filtertron['education'] = active_user.education
    if active_user.deal_smoke == 1:
      filtertron['smoke'] = active_user.smoke
    if active_user.deal_drink == 1:
      filtertron['drink']=active_user.drink
    if active_user.deal_religion == 1:
      filtertron['religion']=active_user.religion
    if active_user.deal_salary == 1:
      filtertron['salary'] = active_user.salary
    
    bulk_match=Profile.objects.filter(**filtertron)
    

      


    delta_arr=[]
    id_arr=[]
    total_delta=0
    for keys in bulk_match:
      try:
        body_delta = abs(active_user.body - keys.body)
      except:
        pass
      try:
        relationship_status_delta = abs(active_user.relationship_status - keys.relationship_status)
        total_delta+=relationship_status_delta
      except:
        pass
      try:
        current_kids_delta = abs(active_user.current_kids - keys.current_kids)
        total_delta+=current_kids_delta
      except:
        pass
      try:
        future_kids_delta = abs(active_user.future_kids - keys.future_kids)
        total_delta+=future_kids_delta
      except:
        pass
      try:
        education_delta = abs(active_user.education - keys.education)
        total_delta+=education_delta
      except:
        pass
      try:
        smoke_delta = abs(active_user.smoke - keys.smoke)
        total_delta+=smoke_delta
      except:
        pass
      try:
        drink_delta = abs(active_user.drink - keys.drink)
        total_delta+=drink_delta
      except:
        pass
      try:
        religion_delta = abs(active_user.religion - keys.religion)
        total_delta+=religion_delta
      except:
        pass
      try:
        salary_delta = abs(active_user.salary - keys.salary)
        total_delta+=salary_delta
      except:
        pass
      try:      
        activity_delta = abs(active_user.activity - keys.activity)
        total_delta+=activity_delta
      except:
        pass
      try:
        frugality_delta = abs(active_user.frugality - keys.frugality)
        total_delta+=frugality_delta
      except:
        pass
      try:
        pragmaticism_delta = abs(active_user.pragmaticism - keys.pragmaticism)
        total_delta+=pragmaticism_delta
      except:
        pass
      try:
        family_delta = abs(active_user.family - keys.family)
        total_delta+=family_delta*5
      except:
        pass

      delta_arr.append(total_delta)
      id_arr.append(keys.user_id)

    #sorts mirrored arrays
    looping=True
    while looping:
      looping=False
      i=1  
      while i<len(delta_arr):
        if delta_arr[i-1]>delta_arr[i]:
          #sort based on lowest delta
          temp=delta_arr[i]
          delta_arr[i]=delta_arr[i-1]
          delta_arr[i-1]=temp
          #sort mirrored id_arr to match indices of delta_arr
          temp=id_arr[i]
          id_arr[i]=id_arr[i-1]
          id_arr[i-1]=temp
          looping=True        
        i+=1
    

    
    percent_arr=[]
    m=0
    while m<len(delta_arr):
      testvar=100-delta_arr[m]
      percent_arr.append(testvar)
      m+=1


    # matches= OrderedDictionary()
    # k=0
    # while k<len(id_arr):
    #   matches.put(percent_arr[k], User.objects.get(id=id_arr[k]))
    #   k+=1
    matches=[]
    k=0
    while k<len(id_arr):
      try:
        matchipus=User.objects.get(id=id_arr[k])
        matchipus.percent= percent_arr[k]

        matches.append(matchipus)
        k+=1
      except:
        errormsg = 'No Results Found: Try widening your net to catch more fish!'
        messages.error(request, errormsg)
        return render(request, 'match_dot_com/matches.html')
      
    percent_obj=[]
    l=0
    while l<len(percent_arr):
      percent_obj.append({percent_arr[l]})
      l+=1


    context = {
      'percent_obj' : percent_obj,
      'matches': matches,
      'me': User.objects.get(id=id),
      'profiles': Profile.objects.exclude(user=id).order_by('user'),
      'images': Images.objects.all().order_by('user'),
    }
    return render(request, 'match_dot_com/matches.html', context)   
    #return HttpResponse(context['matches'])
    
    

    

  return redirect ('match:login')

  # if 'id' in request.session:
  #   id = request.session['id']
  #   context = {
  #     'others': User.objects.exclude(id=id),
  #     'me': User.objects.get(id=id),
  #     'profiles': Profile.objects.exclude(user=id).order_by('user'),
  #     'images': Images.objects.all().order_by('user'),
  #   }
  #   return render (request, 'match_dot_com/index.html', context)



def wink(request, id):
  if 'id' in request.session:
    sender_id = request.session['id']
    recipient_id = id
    Wink.objects.create(sender_id=sender_id, recipient_id=recipient_id)

    messages.error(request, 'Wink sent! ;)')
     #WINK MESSAGE GOES HERE
    return redirect(reverse('match:user', kwargs={'id': id}))
  return redirect('match:login')

def winks(request):
  if 'id' in request.session:
    id = request.session['id']
    context = {
      'users': User.objects.all(),
      'mywinks': Wink.objects.filter(sender_id=id),
      'winksatme': Wink.objects.filter(recipient_id=id),
    }
    return render(request, 'match_dot_com/winks.html', context)
  return redirect('match:login')

def delete(request, id):
  if 'id' in request.session:
    myid= request.session['id']
    if int(id) == myid:
      if request.method == "POST":
        if 'delete' in request.POST:
          User.objects.get(id=id).delete()
          return redirect('match:login')
        if 'keepaccount' in request.POST:
          return redirect('match:index')
      return render(request, 'match_dot_com/accountdelete.html')
    return redirect('match:index')
  return redirect('match:login')

def logout(request):
  request.session.clear()
  return redirect('match:login')