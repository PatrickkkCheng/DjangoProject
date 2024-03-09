from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Note
from .forms import NoteForm

# Create your views here.
def hello_world_view(request):
    return HttpResponse("<h1>Hi</h1>")

def user_profile(request):
    html_content = """
        <h1>Welcome to Codefinity's Django file system</h1>
        <p>Thanks to our file system, you can check the Django code right in the chapter.<br>
        You can also review your code as it visually demonstrates how properly written code looks and in which files this code should be.</p>
    """
    return HttpResponse(html_content)



def read_content(request):
    # Retrieving all notes from the database
    all_notes = Note.objects.all()
    return HttpResponse(all_notes)

def send_content(request):
    new_note= Note(title="Note Example")
    new_note.save()
    return HttpResponse("Note Saved")

def delete_content(request):
    all_notes = Note.objects.all()
    for i in all_notes:
        i.delete()
    return HttpResponse('Notes deleted')

def update_content(request):
    all_notes = Note.objects.all()
    for note in all_notes:
        note.title = 'LOL'
        note.save()
    return HttpResponse('Notes updated')

def special_page(request):
    return render(request, 'notes.html')

def success_page(request):
    return render(request, 'notes.html')


def your_view_function(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        print(title,content)
        return redirect('notes')

    return render(request, 'notes.html')

def index(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            # title = request.POST.get('title')
            # content = request.POST.get('content')
            # print(title, content)
            # return redirect('notes')

    notes = Note.objects.all().order_by('-id')
    return render(request, 'notes.html', {'notes': notes,'name':'hihihihi'})

def note_detail(request, note_id):
    note = Note.objects.get(pk=note_id)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            note.title = title
            note.content = content
            note.save()
            return redirect('notes')
        else:
            print("not valid")

    return render(request, 'note_detail.html', {'note': note})

def delete(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()

    notes = Note.objects.all().order_by('-id')
    render(request, 'notes.html', {'notes': notes})
    return redirect('/')