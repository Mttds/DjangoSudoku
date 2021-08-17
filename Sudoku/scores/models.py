from django.db import models
from django.urls import reverse
import datetime

# Create your models here.
class Score(models.Model): # inherit from Django's Model class
    sudoku     = models.CharField(max_length=81) # initial sudoku as string
    #num_moves  = models.IntegerField(blank=True,null=True)
    solution   = models.CharField(max_length=81) # solved (or attempted) sudoku as string
    solved     = models.BooleanField(default=False,blank=True)
    #solve_time = models.DurationField() # in microseconds
    run_date   = models.DateTimeField(null=True,default=datetime.datetime.now())

    def get_absolute_url(self):
        #return "/scores/{0}/".format(self.id)
        # <app_name> defined in urls.py of this module
        # plus the name of the url defined as argument for path
        return reverse("scores:score-detail", kwargs={"i_id": self.id})

    def get_delete_url(self):
        return reverse("scores:score-delete", kwargs={"i_id": self.id})

    def get_update_url(self):
        return reverse("scores:score-update", kwargs={"i_id": self.id})