from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Districts(models.Model):
    district_id = models.FloatField(db_column='DistrictID', blank=True, null=True)
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)
    locale = models.CharField(db_column='Locale', max_length=255, blank=True, null=True)
    pct_black_hispanic = models.FloatField(db_column='Pct_ethnicity', blank=True, null=True)
    free_reduced = models.FloatField(db_column='Free_reduced', blank=True, null=True)
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
    district_id = models.IntegerField(db_column='district_id', blank=True, null=True)
    timestamp = models.CharField(db_column='timestamp', max_length=255, blank=True, null=True)
    lp_id = models.IntegerField(db_column="lp_id", blank=True, null=True)
    pct_access = models.FloatField(db_column='pct_access', blank=True, null=True)
    engagement_index = models.FloatField(db_column='engagement_index', blank=True, null=True)

    class Meta:
        db_table = "engagement_info"


class StudentFormInfo(models.Model):
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)
    schoolgrade = models.IntegerField(db_column="Grade", blank=True, null=True)
    testscore = models.IntegerField(db_column='Testscore', blank=True, null=True)
    attendancepercentage = models.IntegerField(db_column='Attendance', blank=True, null=True)
    device = models.CharField(db_column='Device', max_length=255, blank=True, null=True)
    studentworkstatus = models.CharField(db_column='Work', max_length=255, blank=True, null=True)
    parentssalary = models.CharField(db_column='PSalary', max_length=255, blank=True, null=True)
    wifi = models.CharField(db_column='Wifi', max_length=255, blank=True, null=True)
    wificompany = models.CharField(db_column='WifiCompany', max_length=255, blank=True, null=True)
    wifispeed = models.CharField(db_column='WifiSpeed', max_length=255, blank=True, null=True)

    class Meta:
        db_table = "studentform_info"


class RatingInfo(models.Model):
    rating = models.IntegerField(db_column="Rating", blank=True, null=True)
    wifiquality = models.IntegerField(db_column="Quality", blank=True, null=True)
    name = models.CharField(db_column='Name', max_length=255, blank=True, null=True)
    placeaddress = models.CharField(db_column='Address', max_length=255, blank=True, null=True)

    class Meta:
        db_table = "ratingwifi_info"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=12)

    def __str__(self):
        return self.user.username


class CountyConnectionInfo(models.Model):
    county_code = models.IntegerField(db_column='County_code', blank=True, null=True)
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)
    county_name = models.CharField(db_column='County_name', max_length=255, blank=True, null=True)
    ratio = models.FloatField(db_column='Ratio', blank=True, null=True)

    class Meta:
        db_table = "county_connection"


# Online Activities for Total gender, 15 years and over.
# class OnlineActivities(models.Model):
#     reference_date = models.CharField(db_column='ReferenceDate', max_length=255, blank=True, null=True)
#     online_activites = models.CharField(db_column='OnlineActivities', max_length=255, blank=True, null=True)
#     gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)
#     age_group = models.CharField(db_column='Agegroup', max_length=255, blank=True, null=True)
#     percentage = models.FloatField(db_column='Percentage', blank=True, null=True)
#
#     class Meta:
#         db_table = "online_activities"
#
#
# Participation rate in education, population aged 15 to 29
class ParticipationRate(models.Model):
    reference_date = models.CharField(db_column='ReferenceDate', max_length=255, blank=True, null=True)
    age = models.CharField(db_column='Age', max_length=255, blank=True, null=True)
    type_of_institution = models.CharField(db_column='Institution', max_length=255, blank=True, null=True)
    percentage = models.FloatField(db_column='Percentage', blank=True, null=True)

    class Meta:
        db_table = "participation_rate"


# Unemployment rates of population aged 15 and over
class UnemploymentRate(models.Model):
    reference_date = models.CharField(db_column='ReferenceDate', max_length=255, blank=True, null=True)
    characteristics_of_the_population = models.CharField(db_column='Characteristics', max_length=255, blank=True,
                                                         null=True)
    educational_attainment = models.CharField(db_column='Educationalattainment', max_length=255, blank=True, null=True)
    percentage = models.FloatField(db_column='Percentage', blank=True, null=True)

    class Meta:
        db_table = "unemployment_rate"




class LabourForce(models.Model):
    reference_date = models.CharField(db_column='ReferenceDate', max_length=255, blank=True, null=True)
    age_group = models.CharField(db_column='AgeGroup', max_length=255, blank=True, null=True)
    labour_force_status = models.CharField(db_column='LabourForceStatus', max_length=255, blank=True, null=True)
    value = models.FloatField(db_column='Value', blank=True, null=True)

    class Meta:
        db_table = "labour_force"


class PostSecondaryEnrollment(models.Model):
    reference_date = models.CharField(db_column='ReferenceDate', max_length=255, blank=True, null=True)
    geo = models.CharField(db_column='GEO', max_length=255, blank=True, null=True)
    institution_type = models.CharField(db_column='InstitutionType', max_length=255, blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)
    value = models.FloatField(db_column='Value', blank=True, null=True)

    class Meta:
        db_table = "postsecondary_enrollment"


class ExpenditureColleges(models.Model):
    reference_date = models.CharField(db_column='ReferenceDate', max_length=255, blank=True, null=True)
    geo = models.CharField(db_column='Geo', max_length=255, blank=True, null=True)
    types_of_expenditure = models.CharField(db_column='Types', max_length=255, blank=True, null=True)
    value = models.FloatField(db_column='Value', blank=True, null=True)

    class Meta:
        db_table = "expenditure_colleges"


class ApprenticeshipRegistration(models.Model):
    reference_date = models.CharField(db_column='ReferenceDate', max_length=255, blank=True, null=True)
    geo = models.CharField(db_column='Geo', max_length=255, blank=True, null=True)
    age_groups = models.CharField(db_column='AgeGroups', max_length=255, blank=True, null=True)
    sex = models.CharField(db_column='Sex', max_length=255, blank=True, null=True)
    trade_groups = models.CharField(db_column='TradeGroups', max_length=255, blank=True, null=True)
    registration_status = models.CharField(db_column='RegistrationStatus', max_length=255, blank=True, null=True)
    value = models.FloatField(db_column='Value', blank=True, null=True)

    class Meta:
        db_table = "apprenticeship_registration"


class AverageTestScores(models.Model):
    reference_date = models.CharField(db_column='ReferenceDate', max_length=255, blank=True, null=True)
    domain = models.CharField(db_column='Domain', max_length=255, blank=True, null=True)
    characteristics = models.CharField(db_column='Characteristics', max_length=255, blank=True, null=True)
    gender = models.CharField(db_column='Gender', max_length=255, blank=True, null=True)
    value = models.FloatField(db_column='Value', blank=True, null=True)

    class Meta:
        db_table = "average_test_scores"
