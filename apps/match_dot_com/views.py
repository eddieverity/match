from django.shortcuts import render, HttpResponse, redirect, reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import re
import bcrypt
import math
from models import *
from django.db.models import Q


# Create your views here.
def index(request):
  if 'id' in request.session:
    id = request.session['id']
    context = {
      'others': User.objects.exclude(id=id),
    }
    return render (request, 'match_dot_com/index.html', context)
  return redirect ('match:login')

def survey(request):
  if request.method=='POST':
    my_id = request.session['id']

    #request.POST.get('is_private', False);

    user_gender = request.POST.get('user_gender', 'null')
    user_age = request.POST['age']
    
    user_height_total = request.POST['valueA']
    # user_height_in = request.POST['user_height_in']
    # user_height_total = (height_ft*12)+height_in
    user_body_type = request.POST['user_bodytype']
    user_relationship_status = request.POST['user_status']
    user_marriage = request.POST['user_marriage']
    user_current_kids = request.POST['user_currkids']
    user_future_kids = request.POST['user_futurekids']
    user_education = request.POST['user_edu']
    user_smoke = request.POST['user_smoke']
    user_drink = request.POST['user_drink']

    user_religion = request.POST['user_religion']
    user_salary = request.POST['user_salary']

    activity=0
    frugality=0
    pragmaticism=0
    family=0

    family+=int(user_current_kids)
    family+=int(user_future_kids)
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

    print user_height_total
    print family
    print frugality
    print activity
    print pragmaticism

    

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
      family=family,
      )

    return redirect('match:survey_seeking')
  return render(request, 'match_dot_com/survey.html')

def survey_seeking(request):
  return render(request, 'match_dot_com/survey_seeking.html')

def seeking_entry(request):
  pass
  #Select matches
  seeking_gender = request.POST['seeking_gender']

  seeking_age_min = request.POST['seeking_age_min']
  seeking_age_max = request.POST['seeking_age_max']

  seeking_height_min = request.POST['seeking_height_min']
  seeking_height_max = request.POST['seeking_height_max']

  seeking_body_type = request.POST['seeking_bodytype']
  deal_seeking_body_type = request.POST['deal_seeking_bodytype']

  seeking_relationship_status = request.POST['seeking_status']
  deal_relationship_status = request.POST['deal_seeking_status']

  seeking_current_kids = request.POST['seeking_current_kids']
  deal_seeking_current_kids = request.POST['deal_seeking_current_kids']

  seeking_future_kids = request.POST['seeking_future_kids']
  deal_seeking_future_kids = request.POST['deal_seeking_future_kids']

  seeking_education = request.POST['seeking_education']
  deal_seeking_education = request.POST['deal_seeking_education']

  seeking_smoke = request.POST['seeking_smoke']
  deal_seeking_smoke = request.POST['deal_seeking_smoke']

  seeking_drink = request.POST['seeking_drink']
  deal_seeking_drink = request.POST['deal_seeking_drink']

  seeking_religion = request.POST['seeking_religion']
  deal_seeking_religion = request.POST['deal_seeking_religion']

  seeking_salary = request.POST['seeking_salary']
  deal_seeking_salary = request.POST['deal_seeking_salary']


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
      'messages': Messages.objects.filter(recipient=id),
    }
    return render(request, 'match_dot_com/messages.html', context)
  return redirect('match:login')

def messenger(request, id):
  if 'id' in request.session:
    userid = request.session['id']
    context = {
      'others': User.objects.get(id=id),
      'pastmessages': Messages.objects.filter(Q(sender=id) | Q(recipient=id, sender=userid)),
      # need to write logic for message sent by user TO the recipient
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
    userprofile = User.objects.get(id=id)
    context = {
      'user': userprofile
    }
    return render(request, 'match_dot_com/user.html', context)
  return redirect('match:login')

def logout(request):
  request.session.clear()
  return redirect('match:login')