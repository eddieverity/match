from django.shortcuts import render, HttpResponse, redirect, reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import re
import bcrypt
from models import *

# Create your views here.
def index(request):
  if 'id' in request.session:
    return render (request, 'match_dot_com/index.html')
  return redirect ('match:login')

def survey(request):
  id = request.session['id']

  pass
  user_gender = request.POST['user_gender']
  user_age = request.POST['user_age']
  
  user_height_ft = request.POST['user_height_ft']
  user_height_in = request.POST['user_height_in']
  user_height_total = (height_ft*12)+height_in
  user_body_type = request.POST['user_body_type']
  user_relationship_status = request.POST['user_relationship_status']
  user_current_kids = request.POST['user_current_kids']
  user_future_kids = request.POST['user_future_kids']
  user_education = request.POST['user_education']
  user_smoke = request.POST['user_smoke']
  user_drink = request.POST['user_drink']

  user_religion = request.POST['user_religion']
  user_salary = request.POST['user_salary']
  user_interests = request.POST['user_interests']
  #calculate Activity, Spending, Artistic, Family scales



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
        return redirect('match:index')
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
        password= pw_hash
        )
      request.session['first_name']=request.POST['first_name']
      request.session['id']=curr_user.id
      return redirect('match:index')
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

def logout(request):
  request.session.clear()
  return redirect('match:login')