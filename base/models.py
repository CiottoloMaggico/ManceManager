import datetime

from django.db import models
from django.db.models import Model

class Client(Model):
    business_name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.business_name

    def total_of_parcels(self):
        total = 0
        for parcel in self.parcels.all():
            total += parcel.total_price
        return total

    def get_hours(self, queryset=None):
        if queryset is None:
            queryset = self.activities.all()
        seconds = 0
        for activity in queryset:
            seconds += activity.duration.seconds

        days = (seconds // 3600) // 24
        hours = (seconds // 3600) % 24
        minutes = seconds % 3600

        return (days, hours, minutes)

    @staticmethod
    def global_price_hour_rate():
        clients = Client.objects.all()
        total_price = 0
        total_hours = 0
        for client in clients:
            total_price += client.total_of_parcels()
            activities = client.activities.all()
            for activity in activities:
                total_hours += activity.duration.seconds // 3600

        if total_hours == 0:
            return 0
        return total_price/total_hours


class Category(Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

class Activity(Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='activities',
        related_query_name='activity'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='activities',
        null=True,
    )
    date = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.category}, {self.date}"

    @property
    def duration(self):
        tmp_start = datetime.datetime.combine(self.date, self.start_hour)
        tmp_end = datetime.datetime.combine(self.date, self.end_hour)
        return (tmp_end - tmp_start)

class Year(Model):
    year = models.PositiveBigIntegerField()

class Quarter(Model):
    year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        related_name='quarters'
    )

class Month(Model):
    quarter = models.ForeignKey(
        Quarter,
        on_delete=models.CASCADE,
        related_name='months'
    )
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

class Parcel(Year):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='parcels',
        related_query_name='parcel'
    )

    def __str__(self):
        return f'Parcella {self.year} - {self.client}'

    @property
    def total_price(self):
        total_price = 0
        for quarter in self.quarters.all():
            months = quarter.months.all()
            for month in months:
                total_price += month.total_price
        return total_price

    def price_hour_rate(self):
        activities = self.client.activities.filter(
            date__year=self.year
        )
        total_hours = 0
        for activity in activities:
            total_hours += activity.duration.seconds // 3600

        if total_hours == 0:
            return 0
        return self.total_price / total_hours





