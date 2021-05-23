from django.shortcuts import render, redirect
from django.contrib import messages
import random


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

