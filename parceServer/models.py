from django.db import models


class Aggregator(models.Model):
    name = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CarAd(models.Model):
    ad_id = models.IntegerField(unique=True)
    link = models.CharField(max_length=150)
    aggregator = models.ForeignKey(to=Aggregator, on_delete=models.CASCADE)
    brand = models.ForeignKey(to=Brand, on_delete=models.CASCADE)
    price = models.FloatField()
    model = models.ForeignKey(to=CarModel, on_delete=models.CASCADE)
    production_date = models.CharField(max_length=20)
    mileage = models.IntegerField(blank=True, null=True)
    cars_engine = models.CharField(max_length=30)
    engine_capacity = models.CharField(max_length=10)
    cars_gearbox = models.CharField(max_length=30)
    cars_type = models.CharField(max_length=30)
    cars_drive = models.CharField(max_length=30)
    condition = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    region = models.CharField(max_length=50)
    area = models.CharField(max_length=30)
    title = models.CharField(max_length=400)
    color = models.CharField(max_length=30)
    description = models.CharField(max_length=1000, blank=True, null=True)
    images = models.CharField(max_length=1000)
    edit_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def update_object(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()
