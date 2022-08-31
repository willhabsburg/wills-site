"""
Views code for will
"""
# cal/views.py

from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CalEvent
from .forms import CalEventForm

def CalView(request, year = 0, month = 0):
    if year == 0:
        year = int(date.today().strftime("%Y"))
        month = int(date.today().strftime("%m"))
    daylist = ["Sunday", "Monday", "Tuesday", "Wednesday",
               "Thurday", "Friday", "Saturday"]
    begin = datetime(year, month, 1)
    prevMonth = begin - timedelta(weeks=1)
    nextMonth = begin + timedelta(weeks=5)
    fdoc = begin - timedelta(days=int(begin.strftime("%w")))
    end = fdoc + timedelta(days=41)
    calTitle = begin.strftime("%B %Y")
    
    events = CalEvent.objects.filter(date__month__gte=begin.month - 1,
                                     date__month__lte=begin.month + 1) \
                                    .order_by('date__month', 'date__day')
    numEvents = events.count()
    
    # Start adding stuff to list to pass to template
    caldays = []
    ec = 0 # event counter
    
    for count in range(0, 42):
        tempStr = fdoc.strftime("%-d") + " - "
        
        while ec < numEvents and \
            int(events[ec].date.strftime("%m%d")) == int(fdoc.strftime("%m%d")):
            
            if events[ec].isAnniv or events[ec].date.strftime("%Y%m%d") == fdoc.strftime("%Y%m%d"):
                if events[ec].owner == request.user or request.user in events[ec].group.others.all() \
                    or not events[ec].group.private:
                    if events[ec].isAnniv:
                        tempStr += events[ec].name + " (" + \
                            str(fdoc.year - events[ec].date.year) + ") - "
                    else:
                        tempStr += events[ec].name + " - "
            ec += 1
            
        tempStr = tempStr[:len(tempStr)-3]
        caldays.append({'day': tempStr, 'count': count + 1})
        fdoc += timedelta(days=1)
    
    context = {
        'daylist': daylist,
        'caldays': caldays,
        'title': calTitle,
        'prevMonth': prevMonth.strftime("%Y/%m"),
        'nextMonth': nextMonth.strftime("%Y/%m"),
    }
    return render(request, 'cal/calendar.html', context)

@login_required(login_url='login')
def addCalEvent(request):
    form = CalEventForm()
    
    if request.method == 'POST':
        form = CalEventForm(request.POST)
        if form.is_valid():
            ce = form.save(commit=False)
            ce.owner = request.user
            ce.save()
            return redirect('cal:home')
        else:
            messages.error('Something went wrong')
    
    
    context = { 'form': form }
    return render(request, 'cal/addCalEvent.html', context)
