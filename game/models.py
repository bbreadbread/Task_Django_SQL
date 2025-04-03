from django.db import models

class Users(models.Model):
    Name = models.CharField(max_length=50, unique=True)
    DateOfVisit = models.DateTimeField(auto_now=True)  
    class Meta:
        ordering = ['-DateOfVisit']
        db_table = "Users" 

    def __str__(self):
        return self.Name

class Records(models.Model):
    user = models.ForeignKey(
        Users,
        to_field='Name',
        db_column='user_name',
        on_delete=models.CASCADE
    )
    NumberOfAttempts = models.IntegerField()

    class Meta:
        db_table = 'Records'
