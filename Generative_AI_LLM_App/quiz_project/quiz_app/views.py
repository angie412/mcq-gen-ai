from typing import Any
from django.shortcuts import render, HttpResponse
from .service import generate_question
from django.views.generic import TemplateView
from .service import print_all_questions
import os
# Create your views here.

def home(request):

    if request.method == "POST":
        text = request.POST['text']
        questions = generate_question(text)
        context = {'questions' : questions}

        return render(request, 'base.html', context)
    return render(request, 'base.html')

def history(request):
   return render(request, 'download.html')

data = print_all_questions()

class TestListView(TemplateView):
    template_name = 'downlad.html'
    def get_context_data(self, **kwargs: Any) :
        context = super().get_context_data(**kwargs)
        context[data] = data
        return context

def download(request, test_id):
    test = None
    for t in data:
        if t[0] == test_id:
            test = t
            break

    if test:
        header = test[1]
        questions = test[2]
        filename = f'test_{test_id}.txt'
        with open(filename, 'w') as f:
            f.write(questions)

        file_path = os.path.join(os.getcwd(),filename)
        response = HttpResponse(open(file_path, 'rb'),content_type = 'text/plain')
        response['Content-Discription'] = f'attachment; filename = "{header.txt}"'
        return response
    
    else:
        return HttpResponse("Test not found")
    

    