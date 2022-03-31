from django import dispatch
from django.db import models
from user.models import User


class Dispatch(models.Model):
    #FK
    order = models.OneToOneField('DispatchOrder', on_delete=models.CASCADE,primary_key=True)
    selected_estimate = models.OneToOneField('DispatchEstimate', on_delete=models.CASCADE, blank=True, null=True)
    regularly = models.OneToOneField('RegularlyOrder', on_delete=models.CASCADE, blank=True, null=True) #셔틀 DB는 추후 반영
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    order_time = models.DateTimeField(auto_now_add=True)# 주문 신청 시간
    estimate_time = models.DateTimeField(blank=True, null=True)# 견적 신청 시간?
    selected_time = models.DateTimeField(blank=True, null=True)# 선택 완료 시간
    confirmed_time = models.DateTimeField(blank=True, null=True)# 결제 완료 시간
    finished_time = models.DateTimeField(blank=True, null=True)# 운행 완료 시간
    
    dispatch_status = models.CharField(max_length=1,default='0')# 배차진행상태
    # 0: 알수없음, 1: 대기중, 2: 선택완료, 3: 결제완료, 4: 운행완료?

    class Meta:
        db_table = 'kingbus_dispatch'
    # def __str__(self) -> str:
    #     return str(self.dispatch)


class DispatchOrder(models.Model):
    #왕복(lt), 편도(st), 셔틀(ro)?
    way = models.CharField(max_length=2)
    purpose = models.CharField(max_length=100)
    reference = models.TextField(blank=True)
    departure = models.CharField(max_length=255)
    departure_short = models.CharField(max_length=64)
    arrival = models.CharField(max_length=255)
    arrival_short = models.CharField(max_length=64)
    stopover = models.TextField(blank=True)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    comeback_date = models.DateField(blank=True, null=True)
    comeback_time = models.TimeField(blank=True, null=True)
    total_number = models.CharField(max_length=10)
    convenience = models.TextField(blank=True)
    is_driver = models.BooleanField(default=False)
    driver_schedule = models.TextField(blank=True)
    total_distance = models.CharField(max_length=4, null=True, blank=True)

    # 견적 확정시 반영 부분
    # price = models.CharField(max_length=10, blank=True)
    # bus_cnt = models.CharField(max_length=5, blank=True)
    # bus_type = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = 'kingbus_dispatch_order'
    # def __str__(self) -> str:
    #     return self.way
    


#셔틀 DB는 추후 반영
class RegularlyOrder(models.Model):
    week = models.CharField(max_length=1)
    term_begin = models.DateField()
    term_end = models.DateField()
    
    class Meta:
        db_table = 'kingbus_regulary_order'
    # def __str__(self) -> str:
    #     return super().__str__()



class DispatchEstimate(models.Model):
    #FK
    order = models.ForeignKey(DispatchOrder, on_delete=models.CASCADE)
    driverorcompany = models.ForeignKey(User, on_delete=models.CASCADE)

    price = models.CharField(max_length=10)
    pricebycar = models.CharField(max_length=10)
    bus_cnt = models.CharField(max_length=5)
    bus_type = models.CharField(max_length=64)

    is_tollgate = models.BooleanField(default=False)# 톨비
    is_parking = models.BooleanField(default=False)# 주차비
    is_accomodation = models.BooleanField(default=False)# 숙박비
    is_meal = models.BooleanField(default=False)# 식사비
    is_convenience = models.BooleanField(default=False)# 편의시설

    class Meta:
        db_table = 'kingbus_estimate'
    # def __str__(self) -> str:
    #     return str(self.driverorcompany)

