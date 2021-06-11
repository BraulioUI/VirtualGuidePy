from modules.users.models import Account
from modules.places.models import TouristicPlace
from django.db import models

# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=50)
    comment_ranking = models.IntegerField()
    date = models.DateField(default="2021-08-17")
    ranking = models.IntegerField()
    touristic_place = models.ForeignKey(TouristicPlace, null=False, blank=False, default="1", on_delete=models.CASCADE)
    user = models.ForeignKey(Account, null=False, blank=False, default="1", on_delete=models.CASCADE)

class PictureReview(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=300)
    number = models.IntegerField()
    review = models.ForeignKey(Review, null=False, blank=False, default="1", on_delete=models.CASCADE)  