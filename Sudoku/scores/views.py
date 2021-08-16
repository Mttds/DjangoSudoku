from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)
from .models import Score
from .forms import ScoreForm, RawScoreForm

# Create your views here.
def scores_view(*args, **kwargs):
    request = args[0]
    user = request.user
    print("User: {0}".format(user))
    # context keys can be used in the rendered template to
    # display the value assigned to the key put between {{}}
    queryset = Score.objects.all() # list of objects
    context = {
        "objects": queryset
    }
    return render(request, "score/scores.html", context)

#def score_create_view(request, *args, **kwargs):
#    print(request.GET)
#    print(request.POST)
#    if(request.method == "POST"):
#        title = request.POST.get('title')
#        print(title)
#    context = {}
#    return render(request, "score/create.html", context)

#def score_create_view(request, *args, **kwargs):
#    form = RawScoreForm() # rendered for the request.GET method passed as default
#    if(request.method == "POST"):
#        form = RawScoreForm(request.POST)
#        if form.is_valid():
#            print(form.cleaned_data) # can save the data
#            Score.objects.create(**form.cleaned_data) # save to database
#        else:
#            print(form.errors)
#    context = {'form': form}
#    return render(request, "score/create.html", context)

def score_create_view(request, *args, **kwargs):
    form = ScoreForm(request.POST or None)
    if form.is_valid():
        form.save() # save to database
        form = ScoreForm() # re-render the form after saving an object

    context = {
        'form': form
    }
    return render(request, "score/create.html", context)

def dynamic_lookup_view(request, i_id):
    #obj = Score.objects.get(id=i_id)
    #obj = get_object_or_404(Score, id=i_id) # to handle a request for an id that is not present in the db
    try: # same thing as above but with a try block
        obj = Score.objects.get(id=i_id)
    except Score.DoesNotExist:
        raise Http404
    context = {
        "obj": obj
    }
    return render(request, "score/detail.html", context)

def score_update_view(request, i_id):
    obj = get_object_or_404(Score, id=i_id)
    form = ScoreForm(request.POST or None, instance=obj)
    if form.is_valid() and request.method == "POST":
        form.save() # save to database
        return redirect('../..')
    context = {
        'form': form
    }
    return render(request, "score/update.html", context)

def score_delete_view(request, i_id):
    obj = get_object_or_404(Score, id=i_id)
    if(request.method == "POST"):
        obj.delete() # confirm deletion
        return redirect('../..')
    context = {
        "obj": obj
    }
    return render(request, "score/delete.html", context)

# class based view of function scores_view
class ScoreListView(ListView):
    # looks for template <app>/<model>_list.html (scores/score_list.html)
    # override it by specifying the template_name var
    template_name = 'score/list.html'

    def get(self, request, *args, **kwargs):
        queryset = Score.objects.all() # list of objects
        return render(request, self.template_name, {'queryset':queryset})

# class based view of function dynamic_lookup_view
class ScoreDetailView(DetailView):
    template_name = 'score/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            obj = Score.objects.get(id=kwargs['i_id'])
        except Score.DoesNotExist:
            raise Http404
        return render(request, self.template_name, {'obj':obj})

# class based view for function score_create_view
class ScoreCreateView(CreateView):
    template_name = 'score/create.html'
    form_class = ScoreForm
    queryset = Score.objects.all() # list of objects

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return '/scores'

# class based view for function score_update_view
class ScoreUpdateView(UpdateView):
    template_name = 'score/update.html'
    form_class = ScoreForm
    queryset = Score.objects.all() # list of objects

    def get_object(self): # similar to ScoreDetailView.get()
        return get_object_or_404(Score, id=self.kwargs['i_id'])

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return '/scores'

# class base view for function score_delete_view
class ScoreDeleteView(DeleteView):
    template_name = 'score/delete.html'

    def get(self, request, *args, **kwargs):
        try:
            obj = Score.objects.get(id=kwargs['i_id'])
        except Score.DoesNotExist:
            raise Http404
        return render(request, self.template_name, {'obj':obj})

    def get_object(self): # similar to ScoreDetailView.get()
        return get_object_or_404(Score, id=self.kwargs['i_id'])

    def get_success_url(self):
        return reverse('scores:scores')