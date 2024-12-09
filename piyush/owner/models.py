from django.db import models

# Create your models here.
class Owenr(models.Model):
    Oname= models.CharField(max_length=100)
    Oemail = models.CharField(max_length=100)
    Ophone = models.CharField(max_length=12)
    Opassword = models.CharField(max_length=100)
   

class HostelMess(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    ownerId = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class HostelMessImage(models.Model):
    hostel_mess = models.ForeignKey(HostelMess, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='static/uploads/')

    def __str__(self):
        return f"Image for {self.hostel_mess.name}"