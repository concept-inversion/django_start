from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.template import loader
from .models import Question,Choice
from django.views import generic
from django.utils import timezone
from django.core.mail import send_mail
from .forms import UploadForm
from django.core.files.storage import FileSystemStorage

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'pollApp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):

        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollApp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        
        selected_choice.save()
        send_mail(
        'About Voting',
        'Voted.',
        'from@santo.com',
        ['to@users.com'],
        fail_silently=False,
        )
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('pollApp:results', args=(question.id,)))

class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollApp/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollApp/results.html'


def formupload(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadForm(request.POST)
        # check whether it's valid:
        #if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
        return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadForm()
    return render(request, 'pollApp/name.html', {'form': form})


def imageupload(request):
    if request.method == 'POST':
        
        #form = (request.POST,request.FILES)
        if request.FILES['image']:
            image = request.FILES['image']
            fs = FileSystemStorage()
            imagefile=fs.save(image.name,image)
            file_url = fs.url(imagefile)
            return render(request, 'pollApp/imageupload.html', {
            'uploaded_file_url': file_url})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadForm()
    return render(request, 'pollApp/imageupload.html')