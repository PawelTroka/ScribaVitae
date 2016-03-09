from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^kategorie/$', views.listCategories, name='listCategories'),
        url(r'^mojeUtwory/$', views.listMyLiteraryWorks, name='listMyLiteraryWorks'),

        url(r'^zaloguj/$', views.logIn, name='logIn'),
            url(r'^wyloguj/$', views.logOut, name='logOut'),
            url(r'^zarejestruj/$', views.register, name='register'),
    # ex: /kategoria/5/
    url(r'^kategoria/(?P<category_id>[0-9]+)$', views.showCategory, name='showCategory'),

    # ex: /dodajUtwor
    url(r'^dodajUtwor/$', views.addLiteraryWork, name='addLiteraryWork'),

    # ex: /utwor/5/
    url(r'^utwor/(?P<literaryWork_id>[0-9]+)$', views.showLiteraryWork, name='showLiteraryWork'),
    # ex: /utwor/5/dodajKomentarz
    url(r'^utwor/(?P<literaryWork_id>[0-9]+)/dodajKomentarz$', views.addComment, name='addComment'),


    # ex: /edytujKomentarz/5
    #url(r'^(?P<literaryWork_id>[0-9]+)/edytujKomentarz/$', views.editComment, name='editComment'),

    # ex: /usunKomentarz/5
    url(r'^usunKomentarz/(?P<comment_id>[0-9]+)$', views.removeComment, name='removeComment'),

    # ex: /utwor/5/edytuj
    url(r'^utwor/(?P<literaryWork_id>[0-9]+)/edytuj$', views.editLiteraryWork, name='editLiteraryWork'),
    # ex: /utwor/5/usun
    url(r'^utwor/(?P<literaryWork_id>[0-9]+)/usun$', views.removeLiteraryWork, name='removeLiteraryWork')

]