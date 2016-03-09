from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from ScribaVitae.models import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.http import *
from django.contrib.auth.decorators import *
from datetime import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
import re

# Create your views here.

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


@require_POST
def logIn(request):
    if not request.user.is_authenticated():
        username = request.POST['login']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('index'))

            else:
                # Return a 'disabled account' error message
                return render(request,'index.html',{'error':"Konto jest nieaktywne"})
        else:
            # Return an 'invalid login' error message.
            return render(request,'index.html',{'error':"Podane hasło jest niepoprawne lub użytkownik nie istnieje"})
        ##################
        #return showLiteraryWork(request, literaryWork_id)
        #return HttpResponseRedirect(reverse('showLiteraryWork', args=(literaryWork_id,)))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_GET
@login_required
def logOut(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        email = request.POST['email']

        errorMessage=""

        if not password or not username or not email:
            errorMessage+="Żadne pole nie może być puste!\n"

        if rpassword!=password:
            errorMessage+="Podane hasła nie są identyczne\n"
            password = ""

        if len(password)<6:
            errorMessage+="Podane hasło jest za krótkie\n"

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errorMessage+="To nie jest poprawny e-mail!\n"

        if User.objects.all().filter(username=username).exists():
            errorMessage+="Użytkownik o podanej nazwie już istnieje!\n"

        if User.objects.all().filter(email=email).exists():
            errorMessage+="Użytkownik o podanym e-mailu już istnieje!\n"

        user = User(username=username,email=email,password=password)

        if errorMessage:
            return render(request,'register.html',{'errors':errorMessage, 'nuser':user})

        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    if (request.method=="GET"):
        return render(request,'register.html')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_GET
def index(request):
    literaryWorks = LiteraryWork.objects.order_by('-dateAdded')
    return render(request,'index.html',{'literaryWorks' : literaryWorks})

@require_GET
@login_required
def listMyLiteraryWorks(request):
    if request.user.is_authenticated():
        literaryWorks = LiteraryWork.objects.filter(author_id=request.user.id).order_by('-dateAdded')
        return render(request,'listMyLiteraryWorks.html',{'literaryWorks' : literaryWorks})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@require_GET
def showLiteraryWork(request, literaryWork_id):
    literaryWork = get_object_or_404(LiteraryWork,pk=literaryWork_id)
    return render(request,'showLiteraryWork.html',{'literaryWork' : literaryWork, 'user' : request.user})
    #return HttpResponse("You're looking at question %s." % literaryWork_id)

class LiteraryWorkDetail(DetailView):
    model = LiteraryWork

@login_required
@require_http_methods(["GET", "POST"])
def addLiteraryWork(request):
    categories = Category.objects.all()
    if request.user.is_authenticated():
        if request.method == "POST":
            category = request.POST['category']
            content = request.POST['content']
            title = request.POST['title']
            errorMessage=""

            if not category or not content or not title:
                errorMessage+="Żadne pole nie może być puste!\n"

            if not Category.objects.filter(name=category).exists():
                errorMessage+="Podana kategoria nie istnieje\n"
                cat = None
            else:
                cat = get_object_or_404(Category,name=category)

            literaryWork = LiteraryWork(category=cat,content=content, title=title)
            if errorMessage:
                return render(request,'addLiteraryWork.html',{'errors':errorMessage, 'literaryWork':literaryWork,'categories' : categories})

            literaryWork = LiteraryWork.objects.create(category=get_object_or_404(Category,name=category),content=content,author=request.user, dateAdded=datetime.now(),title=title)
            literaryWork.save()
            return HttpResponseRedirect(reverse('showLiteraryWork', args=(literaryWork.id,)))
        if (request.method=="GET"):
            return render(request,'addLiteraryWork.html',{'user':request.user,'categories' : categories})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_http_methods(["GET", "POST"])
def editLiteraryWork(request, literaryWork_id):
    literaryWork = get_object_or_404(LiteraryWork,pk=literaryWork_id)
    if request.user.id == literaryWork.author_id or request.user.is_staff:
        return render(request,'editLiteraryWork.html',{'literaryWork':literaryWork})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_GET
def removeLiteraryWork(request, literaryWork_id):
    literaryWork = get_object_or_404(LiteraryWork,pk=literaryWork_id)
    if request.user.id == literaryWork.author_id or request.user.is_staff:
        categoryId = literaryWork.category_id
        literaryWork.delete()
        #return HttpResponseRedirect(showCategory(request,categoryId))#showCategory(request,categoryId)
        return HttpResponseRedirect(reverse('showCategory', args=(categoryId,)))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #return render(request,'removeLiteraryWork.html',{'literaryWork':literaryWork})

@login_required
@require_POST
def addComment(request, literaryWork_id):
    if request.user.is_authenticated():
        #TODO: add comment here
        #try:
        comment = request.POST['comment']
        #except (KeyError, Choice.DoesNotExist):
        if(comment):
            newComment = Comment(content=comment,author_id=request.user.id, literaryWork_id=literaryWork_id, dateAdded=datetime.now())
            newComment.save()
        # Redisplay the question voting form.
        ##################
        #return showLiteraryWork(request, literaryWork_id)
            return HttpResponseRedirect(reverse('showLiteraryWork', args=(literaryWork_id,)))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



#def editComment(request, comment_id):
 #   comment = get_object_or_404(Comment,pk=comment_id)
  #  if request.user.id == comment.author_id or request.user.is_staff:
   #     return render(request,'editComment.html',{'comment':comment})
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required
@require_GET
def removeComment(request, comment_id):
    comment = get_object_or_404(Comment,pk=comment_id)
    if request.user.id == comment.author_id or request.user.is_staff:
        literaryWorkId = comment.literaryWork_id
        comment.delete()
        return HttpResponseRedirect(reverse('showLiteraryWork', args=(literaryWorkId,)))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #return render(request,'removeComment.html',{'comment':comment})



@require_GET
def showCategory(request, category_id):
    category = get_object_or_404(Category,pk=category_id)
    literaryWorks = LiteraryWork.objects.filter(category=category).order_by('-dateAdded')
    return render(request,'showCategory.html',{'literaryWorks' : literaryWorks,
                                                   'category' : category})


@require_GET
def listCategories(request):
    categories = Category.objects.all()
    return render(request,'listCategories.html',{'categories' : categories})
