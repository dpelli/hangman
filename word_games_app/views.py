from django.shortcuts import render, redirect
from django.contrib import messages
import random
import bcrypt

from .models import *


words = ["python", 
    "jumble", 
    "easy", 
    "difficult", 
    "answer", 
    "xylophone"
]

def index(request):
    return render(request, 'index.html')

def rword(request):
    word = random.choice(words)
    request.session['word'] = word
    jumble = random.sample(word, len(word)) #return a list of letters
    jumbled_word = "".join(jumble)
    request.session['jumbled_word'] = jumbled_word
    return redirect("/word_jumble")

def word_jumble(request):
    if 'answer' not in request.session:
        request.session['answer'] = ""
    if 'jumbled_word' not in request.session:
        request.session['jumbled_word'] = " "
    context = {
        'jumbled_word': request.session['jumbled_word'],
        'answer': request.session['answer']
    }
    return render(request, 'word_jumble.html', context)

def guess(request):
    guess = request.POST['guess']
    if guess != request.session['word']:
        request.session['answer'] = "Wrong!"
    else:
        request.session['answer'] = "Correct!"
    return redirect("/word_jumble")

def start(request):
    rword(request)
    return redirect("/word_jumble")

def reset(request):
    request.session.flush()
    return redirect("/word_jumble")

def logout(request):
    request.session.flush()
    return redirect("/")


def register(request):

    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    if request.method == "POST":
    #     User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=request.POST['password'])
    # return redirect('/')

        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=hashed_pw
        )
        request.session['user_id'] = new_user.id
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email_address = request.POST['email_address'])
        request.session['user_id'] = this_user[0].id
        return redirect('/dashboard')
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = User.objects.get(id=request.session['user_id'])
    # my_jobs = Job.objects.get(id=request.session['job_id'])
    context = {
        # "all_jobs": Job.objects.all(),
        # 'user_id': user_id,
        # 'users_id': User.objects.all(),
        # "my_jobs": Job.objects.get(id=job_id)
    }
    return render(request, 'dashboard.html', context)

def hangman(request):
    return redirect("/hangman")