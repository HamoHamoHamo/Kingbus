from django.db import models
from user.models import CompanyAcc, DriverAcc, User

# Create your models here.

class Dispatch(models.Model):
    #왕복(lt), 편도(st)
    way = models.CharField(max_length=2, blank=True)
    purpose = models.CharField(max_length=100)
    reference = models.TextField(blank=True)
    departure = models.CharField(max_length=255)
    arrival = models.CharField(max_length=255)
    stopover = models.TextField(blank=True)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField(blank=True)
    arrival_time = models.TimeField(blank=True)
    is_driver = models.BooleanField(default=False)
    total_number = models.CharField(max_length=10)
    convenience = models.TextField()

    # 견적 확정시 반영 부분
    bus_type = models.CharField(max_length=30, blank=True)
    price = models.CharField(max_length=10, blank=True)
    bus_cnt = models.CharField(max_length=5, blank=True)

    def __str__(self) -> str:
        return self.way
#셔틀 DB는 추후 반영
class Regularly_order(models.Model):
    week = models.CharField(max_length=1)
    term_begin = models.DateField()
    term_end = models.DateField()
    
    def __str__(self) -> str:
        return super().__str__()

class Estimate(models.Model):
    is_toll_gate = models.BooleanField(default=False)
    is_parking = models.BooleanField(default=False)
    is_accomodation = models.BooleanField(default=False)
    is_meal = models.BooleanField(default=False)
    is_convenience = models.BooleanField(default=False)

    price = models.CharField(max_length=10, blank=True)
    bus_type = models.CharField(max_length=30, blank=True)
    bus_cnt = models.CharField(max_length=5, blank=True)
    #FK
    order = models.ForeignKey(Dispatch, on_delete=models.CASCADE)
    driver = models.ForeignKey(DriverAcc, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyAcc, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.order.way

class Dispatch_order(models.Model):
    #주문 신청 시간
    order_time = models.TimeField()
    #견적 확정 시간
    estimate_confirmed_time = models.TimeField(blank=True)
    #견적 신청 시간
    estimate_order_time = models.TimeField(blank=True)
    #예약 확정 여부
    reservation_confirmed = models.BooleanField(default=False)
    #FK
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE)
    regularly = models.ForeignKey(Regularly_order, on_delete=models.CASCADE) #셔틀 DB는 추후 반영
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.userid