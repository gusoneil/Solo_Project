from django.shortcuts import render, redirect
from .models import User, UserManager, Review
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        pw = request.POST['password']
        hashed_pw = bcrypt.hashpw(pw.encode(),bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw
        )
        request.session['user_id'] = new_user.id
        return redirect('/')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        this_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/main')
    return redirect('/')

def main(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': this_user,
        'reviews': Review.objects.all()
    }
    return render(request, 'main.html', context)

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    return render(request, 'create.html')

def create(request):
    if request.method == 'POST':
        errors = Review.objects.basic_validator(request.POST)
        if len(errors) != 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/new')
        Review.objects.create(
            title = request.POST['title'],
            year_released = request.POST['year_released'],
            developer = request.POST['developer'],
            rating = request.POST['rating'],
            desc = request.POST['desc'],
            owner = User.objects.get(id = request.session['user_id'])
        )
        return redirect('/main')

def view(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_review = Review.objects.get(id=id)
    context = {
        'review': this_review
    }
    return render(request, 'view.html', context)

def edit(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_review = Review.objects.get(id=id)
    context = {
        'review': current_review
    }
    return render(request, 'edit.html', context)

def update(request, id):
    if request.method == 'POST':
        errors = Review.objects.basic_validator(request.POST)
        if len(errors) != 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/edit')
        review_update = Review.objects.get(id=id)
        review_update.title = request.POST['title']
        review_update.year_released = request.POST['year_released']
        review_update.developer = request.POST['developer']
        review_update.rating = request.POST['rating']
        review_update.desc = request.POST['desc']
        review_update.save()
        return redirect('/main')

def delete(request, id):
    to_delete = Review.objects.get(id=id)
    to_delete.delete()
    return redirect('/main')

def logout(request):
    request.session.flush()
    return redirect('/')