from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def books(request):
    if 'userid' not in request.session:
        messages.error(request, "Please log in first!")
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userid']),
            'all_books': Book.objects.all()
        }
        return render(request, 'books.html', context)

def addbook(request):
    if request.GET or 'userid' not in request.session:
        return redirect('/books')
    else:
        errors = Book.objects.book_validations(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            Book.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                uploaded_by=User.objects.get(id=request.session['userid'])
            )
            this_book = Book.objects.get(title=request.POST['title'])
            this_book.user_who_like.add(User.objects.get(id=request.session['userid']))
            messages.success(request, "Succesfully added a new book!")
            return redirect('/books')
    

def showbook(request, idn):
    if request.GET or 'userid' not in request.session:
        return redirect('/books')
    else:
        try:
            this_book = Book.objects.get(id=idn)
            this_user = User.objects.get(id=request.session['userid'])
            if this_user.id == this_book.uploaded_by.id:
                context={
                    'user': this_user,
                    'book': this_book
                }
                return render(request, 'editbook.html', context)
            else:
                context={
                    'user': this_user,
                    'book': this_book
                }
                return render(request, 'showbook.html', context)
        except:
            return redirect('/books')

def updatebook(request, idn):
    if request.GET or 'userid' not in request.session:
        return redirect('/books')
    else:
        try:
            this_book = Book.objects.get(id=idn)
            errors = Book.objects.book_validations(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/books/{this_book.id}')
            this_book.title = request.POST['title']
            this_book.description = request.POST['description']
            this_book.save()
            messages.success(request, f'Succesfully updated "{this_book.title}"!')
            return redirect(f'/books/{this_book.id}')
        except:
            return redirect('/books')

def deletebook(request, idn):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        this_user = User.objects.get(id=request.session['userid'])
        this_book = Book.objects.get(id=idn)
        if  this_user == this_book.uploaded_by:
            this_book.delete()
            messages.success(request, f'Succesfully deleted the book!!')
            return redirect('/books')
        else:
            messages.error(request, f'You dont have permission to do that!!')
            return redirect('/books')


def areyousure(request, idn):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userid']),
            'book': Book.objects.get(id=idn)
        }
        return render(request, 'deletebook.html', context)


def newfavorite(request):
    if request.GET or 'userid' not in request.session:
        return redirect('/books')
    else:
        this_book = Book.objects.get(id=request.POST['book'])
        this_book.user_who_like.add(User.objects.get(id=request.session['userid']))
        messages.success(request, f'Succesfully added "{this_book.title}" to favorites!')
        return redirect(f'/books/{this_book.id}')        
def unfavorite(request):
    if request.GET or 'userid' not in request.session:
        return redirect('/books')
    else:
        this_book = Book.objects.get(id=request.POST['book'])
        this_book.user_who_like.remove(User.objects.get(id=request.session['userid']))
        messages.success(request, f'Succesfully removed "{this_book.title}" from favorites!')
        return redirect(f'/books/{this_book.id}')
