from django.db import models
from django.urls import reverse
import datetime

# Create your models here.
class Score(models.Model): # inherit from Django's Model class
    sudoku     = models.TextField() # initial sudoku as string
    num_moves  = models.IntegerField(blank=True,null=True)
    solution   = models.TextField() # solved (or attempted) sudoku as string
    solved     = models.BooleanField(default=False)
    solve_time = models.DurationField() # in microseconds
    run_date   = models.DateTimeField(null=True,default=datetime.datetime.now())

    def get_absolute_url(self):
        #return "/scores/{0}/".format(self.id)
        # <app_name> defined in urls.py of this module
        # plus the name of the url defined as argument for path
        return reverse("scores:score-detail", kwargs={"i_id": self.id})