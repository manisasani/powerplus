from django.db import models

class Muscle(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='muscles/')
    description = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle = models.ForeignKey(Muscle, on_delete=models.CASCADE, related_name='exercises')
    video = models.FileField(upload_to='exercises/')
    description = models.TextField()
    tags = models.CharField(max_length=200, blank=True)
    create_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name