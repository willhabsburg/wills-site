from django.db import models
from django.contrib.auth.models import User

class EventGroup(models.Model):
    """
    Grouping for CalEvent so users can choose what to display
    """
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    others = models.ManyToManyField(User, related_name='groupUsers',
                                    blank=True)
    private = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class CalEvent(models.Model):
    """
    Represents an event on a calendar
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    isAnniv = models.BooleanField(default=False,
                                  help_text='Will show the # of years since event.')
    group = models.ForeignKey(EventGroup, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name
    
class ToDoEvent(models.Model):
    """
    Represents a to-do list item
    """
    HOURS = 'hours'
    DAYS = 'days'
    WEEKS = 'weeks'
    MONTHS = 'months'
    REPEAT_CHOICES = [
        (HOURS, 'Hours'),
        (DAYS, 'Days'),
        (WEEKS, 'Weeks'),
        (MONTHS, 'Months')
    ]
    parent = models.ForeignKey('ToDoEvent', on_delete=models.CASCADE, null=True)
    children = models.ManyToManyField('ToDoEvent', related_name='childs',
                                      blank=True)
    name = models.CharField(max_length=255)
    duedate = models.DateField()
    duetime = models.TimeField(null=True)
    isdone = models.BooleanField(default=False)
    repeatOnDone = models.BooleanField(default=False)
    repeatFreq = models.IntegerField(default=0)
    repeatType = models.CharField(max_length=10, choices=REPEAT_CHOICES,
                                  default=DAYS)
    
    class Meta:
        ordering = ['duedate', 'duetime']
        
    def __str__(self):
        return self.name
