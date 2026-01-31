from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def chatbot(request):
    return render(request, 'chatbot.html')

def timetable(request):
    return render(request, 'time_table.html')

def todo_list(request):
    return render(request, 'todo_list.html')