from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Districts(models.Model):
    district_id = models.FloatField(db_column='DistrictID', blank=True, null=True)
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)
    locale = models.CharField(db_column='Locale', max_length=255, blank=True, null=True)
    pct_black_hispanic = models.FloatField(db_column='Pct_ethnicity', blank=True, null=True)
    county_connection = models.FloatField(db_column='County_connection', blank=True, null=True)
    pp_total_raw = models.FloatField(db_column='PP_total_raw', blank=True, null=True)

    class Meta:
        db_table = "district_info"


class ProductsInfo(models.Model):
    lpid = models.IntegerField(db_column='Lpid', blank=True, null=True)
    url = models.CharField(db_column="URL", max_length=255, blank=True, null=True)
    product_name = models.CharField(db_column='Product_Name', max_length=255, blank=True, null=True)
    provider_name = models.CharField(db_column='Provider', max_length=255, blank=True, null=True)
    sector = models.CharField(db_column='Sector', max_length=255, blank=True, null=True)
    primary_essential = models.CharField(db_column='Primary_Essential_Function', max_length=255, blank=True, null=True)

    class Meta:
        db_table = "products_info"


class EngagementInfo(models.Model):
    time = models.CharField(db_column='Time',max_length=255, blank=True, null=True)
    lp_id = models.IntegerField(db_column="Lp_id",blank=True, null=True)
    pct_access = models.FloatField(db_column='Pct_access', blank=True, null=True)
    engagement_index = models.FloatField(db_column='Engagement_index', blank=True, null=True)

    class Meta:
        db_table = "engagement_info"

class StudentFormInfo(models.Model):
    province = models.CharField(db_column='Province',max_length=255,blank=True, null=True)
    schoolgrade = models.IntegerField(db_column="Grade",blank=True, null=True)
    testscore = models.IntegerField(db_column='Testscore', blank=True, null=True)
    attendancepercentage = models.IntegerField(db_column='Attendance', blank=True, null=True)
    device = models.CharField(db_column='Device',max_length=255, blank=True, null=True)
    studentworkstatus = models.CharField(db_column='Work',max_length=255, blank=True, null=True)
    parentssalary = models.CharField(db_column='PSalary',max_length=255, blank=True, null=True)
    wifi = models.CharField(db_column='Wifi',max_length=255, blank=True, null=True)
    wificompany = models.CharField(db_column='WifiCompany',max_length=255, blank=True, null=True)
    wifispeed = models.CharField(db_column='WifiSpeed',max_length=255, blank=True, null=True)

    class Meta:
        db_table = "studentform_info"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=12)

    def __str__(self):
        return self.user.username
