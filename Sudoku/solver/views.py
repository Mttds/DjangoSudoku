from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .solver import solve, display

# Create your views here.
# the first param passed is the request
# we can put a param before *args in our function
# to capture it directly and not have to parse *args to retrieve it
def home_view(*args, **kwargs):
    request = args[0]
    user = request.user
    print("User: {0}".format(user))
    #out = solve('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
    #display(out)
    return render(request, "home.html", {})

# class based view for function home_view
class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        post_dict = request.POST.copy() # GET and POST QueryDict are immutable so we need to make a copy
        post_dict.pop('csrfmiddlewaretoken')
        input_string = ""
        for k, v in post_dict.items():
            if v == '':
                v = '.'
            input_string = input_string + v
        solution = solve(input_string)
        #print(input_string)
        #display(out)
        context = {
            "solution": solution
        }
        return render(request, self.template_name, context)

    def get_success_url(self):
        return '/'