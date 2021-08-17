from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .solver import solve, display, grid_values
from scores.models import Score
import datetime

# Create your views here.
# the first param passed is the request
# we can put a param before *args in our function
# to capture it directly and not have to parse *args to retrieve it
def home_view(*args, **kwargs):
    request = args[0]
    user = request.user
    print("User: {0}".format(user))
    return render(request, "home.html", {})

# class based view for function home_view
class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        post_dict = request.POST.copy() # GET and POST QueryDicts are immutable so we need to make a copy
        post_dict.pop('csrfmiddlewaretoken')
        input_string = ""
        output_string = ""
        for k, v in post_dict.items():
            if v == '':
                v = '.'
            input_string = input_string + v
        
        input_as_dict = grid_values(input_string)
        solution = solve(input_string)
        if(not(solution)):
            Score.objects.create(sudoku=input_string, solution="", solved=False, run_date=datetime.datetime.now()) # save to database
            return render(request, "unsolved.html", {"sudoku": input_string})

        for k, v in solution.items():
            if v == '' or v == '123456789':
                v = '.'
            output_string = output_string + v

        # display on server side the input and the solution as a text grid
        display(input_as_dict)
        display(solution)
        solution_A = {k: solution[k] for k in ('A1','A2','A3','A4','A5','A6','A7','A8','A9')}
        solution_B = {k: solution[k] for k in ('B1','B2','B3','B4','B5','B6','B7','B8','B9')}
        solution_C = {k: solution[k] for k in ('C1','C2','C3','C4','C5','C6','C7','C8','C9')}
        solution_D = {k: solution[k] for k in ('D1','D2','D3','D4','D5','D6','D7','D8','D9')}
        solution_E = {k: solution[k] for k in ('E1','E2','E3','E4','E5','E6','E7','E8','E9')}
        solution_F = {k: solution[k] for k in ('F1','F2','F3','F4','F5','F6','F7','F8','F9')}
        solution_G = {k: solution[k] for k in ('G1','G2','G3','G4','G5','G6','G7','G8','G9')}
        solution_H = {k: solution[k] for k in ('H1','H2','H3','H4','H5','H6','H7','H8','H9')}
        solution_I = {k: solution[k] for k in ('I1','I2','I3','I4','I5','I6','I7','I8','I9')}
        context = {
            "solution_A": solution_A,
            "solution_B": solution_B,
            "solution_C": solution_C,
            "solution_D": solution_D,
            "solution_E": solution_E,
            "solution_F": solution_F,
            "solution_G": solution_G,
            "solution_H": solution_H,
            "solution_I": solution_I
        },
        Score.objects.create(sudoku=input_string, solution=output_string, solved=True, run_date=datetime.datetime.now()) # save to database
        return render(request, self.template_name, context[0]) # context is a tuple, we want just the first element which is a dict of dictionaries

    #def get_success_url(self):
    #    return '/'