from django.db import models

#events -- event, price,
#delegate -- name, college, semester, prp,

class Events(models.Model):
    event_name = models.TextField()
    fees = models.DecimalField(max_digits=10, decimal_places=2) #make maxdigit = 10

    def __str__(self) -> str:
        return f"{self.event_name}"


class Delegates(models.Model):
    name = models.CharField(max_length=350)
    semester = models.CharField(max_length=2)
    ktu_id = models.CharField(max_length=25, unique=True)
    gmail = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #make maxdigit = 10
    
    def __str__(self) -> str:
        return f"{self.name}: {self.ktu_id}"


class DelegateEvent(models.Model):
    delegate = models.ForeignKey(Delegates, on_delete=models.CASCADE, related_name='events')
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Entertainment(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='games')
    game_name = models.TextField()

    def __str__(self) -> str:
        return f"{self.game_name}"
    

class DelegateEntertainment(models.Model):
    delegate = models.ForeignKey(Delegates, on_delete=models.CASCADE, related_name='entertainment')
    entertainment = models.ForeignKey(Entertainment, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
 