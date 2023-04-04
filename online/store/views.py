from django.shortcuts import render, reverse
from .models import Game, Category
from .forms import GameSearchForm, DateSearchForm
from django.shortcuts import get_object_or_404
# Create your views here.
from django.core.paginator import Paginator
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Comment
from django.contrib.auth.decorators import login_required
import time


from django.views.decorators.cache import cache_page
# @cache_page(60 * 15)
def index(request):
    order = request.GET.get('order_by')
    field, direction = '', ''
    
    games = Game.objects.filter(is_active=True)
    if order:
        field, direction = order.split(":")
        flow = '' if direction == 'asc' else '-'
        sorting = f"{flow}{field}"
        games = games.order_by(sorting)
    paginator = Paginator(games, 3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    response = render(request, 'store/index.html', context={'page_obj': page_obj, 'field': field, 'direction': direction})
    return response

def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories': categories})


def category_products(request, categoty_slug):
    category = get_object_or_404(Category, slug=categoty_slug)
    games = Game.objects.filter(is_active=True, category=category)
    print(category.game_set.filter(release_date__gt=date(2020,1,1)).all())
    context = {
        'category': category,
        'games': games
    }
    return render(request, 'store/category_products.html', context) 
from django.db.models import Field

# @login_required(login_url=reverse_lazy("users:login"))
def game_detail(request, game_slug):
    import datetime
    import logging
    logging.info('In game detail')
    game = get_object_or_404(Game, slug=game_slug)
    ([print(getattr(game,f.name)) for f in game._meta.get_fields() if isinstance(f, Field)])
    print([getattr(game,field.name) for field in game._meta.get_fields() if isinstance(field, Field)])
    last_visited = request.COOKIES.get(game_slug)
    comments = game.comment_set.all()
    context = {
        'game': game,
        'comments': comments,
        'last_visited': last_visited
    }
    response = render(request, 'store/detail.html', context)
    visit_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response.set_cookie(game_slug, visit_time, max_age=datetime.timedelta(days=20))
    return response

# from store.tasks import replace_text_with_censored
from django.core import serializers

class CommentCreateView(CreateView):
    model = Comment
    fields = ["text", "rating"]
    
    def get_success_url(self):
        print(self.object)
        return reverse("store:game-detail", kwargs={'game_slug': self.object.game.slug})
    
    def form_valid(self, form):
        form.instance.game = Game.objects.get(slug=self.kwargs['game_slug'])
        self.object = form.save()
        print(Game.objects.get(slug=self.kwargs['game_slug']))
        # replace_text_with_censored.delay(serializers.serialize('json', [self.object]))
        return HttpResponseRedirect(self.get_success_url())
        # return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ["text", "rating"]


class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy("store:index")


# def form_practice(request):
    # if request.method == 'POST':
    #     print(request.POST)
    # return render(request, 'store/practice.html')


# def form_practice(request):
#     if request.method == 'POST':
#         form = GameSearchForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data['game_name'].title())
#             searched_game = Game.objects.get(name=form.cleaned_data['game_name'].title())
#             return HttpResponseRedirect(reverse('store:game-detail', kwargs={'game_slug': searched_game.slug}))
#     else:
#         form = GameSearchForm()
#     return render(request, 'store/practice.html', {'form': form})

# def form_practice(request):
#     if request.method == 'POST':
#         form = DateSearchForm(request.POST)
#         if form.is_valid():
#             ...
#     else:
#         form = DateSearchForm()
#     return render(request, 'store/practice.html', {'form': form})




