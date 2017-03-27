from django.shortcuts import render, HttpResponse, redirect, reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import re
import bcrypt

# Create your views here.
def index(request):
  if 'id' in request.session:
    return render (request, 'match_dot_com/index.html')
  return render (request,'match_dot_com/registration_login.html')

def survey(request):
  pass





def login(request):
  l_email=request.POST['l_email']
  try:
    curr_user=User.objects.get(email = l_email)
    l_password=request.POST['l_password'].encode(encoding="utf-8")
    if bcrypt.hashpw(l_password, curr_user.password.encode("utf-8")) == curr_user.password:
      request.session['first_name']=curr_user.first_name
      request.session['id']=curr_user.id
      return redirect('match:index')
    else:
      messages.error(request, 'password does not match registered user')
      return redirect('match:register')
  except User.DoesNotExist:
    messages.error(request, 'email does not exist in database, please register')
    return redirect('match:register')

def register(request):
  is_valid = True
  first_name = request.POST['first_name']
  last_name = request.POST['last_name']
  email = request.POST['email']
  confirm = request.POST['confirm'] 
  password = request.POST['password'].encode(encoding="utf-8")
  pw_hash=bcrypt.hashpw(password, bcrypt.gensalt())
  if ValidateEmail(email) != True:
    messages.error(request, 'email address not valid')
    is_valid = False
  if DupEmail(email):
    messages.error(request, 'email address in use')
    is_valid= False
  if len(name) < 2:
    messages.error(request, 'name must be at least 2 characters long')
    is_valid = False
  if len(password) < 8:
    messages.error(request, 'password must be at least 8 characters long')
    is_valid = False
  if password != confirm:
    messages.error(request, 'passwords do not match')
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
    return redirect('match:survey')

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
