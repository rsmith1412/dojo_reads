from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book, Review
import bcrypt

# Create your views here.
def index(request):
    return render(request, "reads_app/index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        return redirect("/")
    else:
        name = request.POST["name"]
        alias = request.POST["alias"]
        email = request.POST["email"]
        pw = request.POST["password"]
        pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
        new_user = User.objects.create(name=name, alias=alias, email=email, password=pw_hash)
        request.session["user_id"] = new_user.id
        return redirect("/books")

def login(request):
    email = request.POST["email"]
    pw = request.POST["password_login"]
    users = User.objects.filter(email = email)
    if len(users) == 0:
        messages.error(request, "Invalid login.", extra_tags='login')
        return redirect("/")

    user = users[0]
    if bcrypt.checkpw(pw.encode(), user.password.encode()):
        request.session["user_id"] = user.id
        return redirect("/books")
    messages.error(request, "Invalid login.", extra_tags='login')
    return redirect("/")

def books(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session["user_id"])
        all_books = Book.objects.all()
        for book in all_books:
            print(book.title)
        all_reviews = Review.objects.all().order_by("-created_at")
        reviews = Review.objects.all().order_by("-created_at")
        last_three_reviews = []
        books_last_three_reviews = []
        for x in range(3):
            last_three_reviews.append(all_reviews[x])
            books_last_three_reviews.append(all_reviews[x].book_reviewed.title)
        print(books_last_three_reviews)
        books_with_reviews = [book for book in all_books if len(book.reviews.all()) > 0 and book.title not in books_last_three_reviews]
        # for book in all_books:
        #     if len(book.reviews) > 0:
        #         books_with_reviews.append(book)
        context = {
            "user" : user,
            "books" : books_with_reviews,
            "reviews" : last_three_reviews
        }
        return render(request, "reads_app/books.html", context)
    return redirect("/")

def add_book(request):
    if not 'user_id' in request.session:
        return redirect("/")
    return render(request, "reads_app/add_book.html")

def create_book(request):
    user = User.objects.get(id=request.session["user_id"])
    book_errors = Book.objects.book_validator(request.POST)
    review_errors = Review.objects.review_validator(request.POST)
    if len(book_errors) > 0 or len(review_errors) > 0:
        for key, value in book_errors.items():
            messages.error(request, value, extra_tags='book')
        for key, value in review_errors.items():
            messages.error(request, value, extra_tags='book')
        return redirect("/books/add")
    else:
        title = request.POST["title"]
        author = request.POST["author"]
        book = Book.objects.create(title=title, author=author)
        # Create rating and rating's relationship to book
        content = request.POST["content"]
        rating = request.POST["rating"]
        Review.objects.create(content=content, rating=rating, reviewer=user, book_reviewed=book)
        return redirect("/books/" + str(book.id))

def show_book(request, id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=id)
    context = {
        "book" : book,
        "user" : user
    }
    return render(request, "reads_app/show_book.html", context)

def create_review(request, id):
    user = User.objects.get(id=request.session["user_id"])
    book = Book.objects.get(id=id)
    content = request.POST["content"]
    rating = request.POST["rating"]
    Review.objects.create(content=content, rating=rating, reviewer=user, book_reviewed=book)
    return redirect("/books/" + str(book.id))

def delete_review(request, id):
    del_rev = Review.objects.get(id=id)
    book_id = str(del_rev.book_reviewed.id)
    del_rev.delete()
    return redirect("/books/" + book_id)

def show_user(request, id):
    user = User.objects.get(id=id)
    context = {
        "user" : user
    }
    return render(request, "reads_app/show_user.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")