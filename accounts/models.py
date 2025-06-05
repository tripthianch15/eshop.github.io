# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.utils import timezone


def profile_pic_file_path(instance, filename):
      # Modification made on 31-08-2023
      # Added tenant prefix 
      # to partition S3 bucket
      #
    #   schema_name = connection.get_schema()
    #   tenant = settings.TENANT_PREFIX + schema_name
      
      #file_path = '{0}/{1}/{2}/{3}/{4}'.format(tenant,"users",instance.username,"profile_pic",filename)
      file_path = '{0}/{1}/{2}/{3}'.format("users",instance.user.username,"profile_pic",filename)
      #print("Profile pic path= ",file_path)
      return file_path


def user_kyc_image_path(instance, filename):
      # Modification made on 31-08-2023
      # Added tenant prefix 
      # to partition S3 bucket
      #
    #   schema_name = connection.get_schema()
    #   tenant = settings.TENANT_PREFIX + schema_name
      
      #file_path = '{0}/{1}/{2}/{3}/{4}'.format(tenant,"users",instance.username,"profile_pic",filename)
      file_path = '{0}/{1}/{2}/{3}'.format("users",instance.user.username,"user_kyc_images",filename)
      #print("Profile pic path= ",file_path)
      return file_path




ACTIVE = 'Active'
NOTACTIVE = 'Not Active'
STATUS_CHOICES = ((ACTIVE,'Active'),
                  (NOTACTIVE,'Not Active'))

APPROVED = 'Aproved'
NOTAPPROVED = 'Not Aproved'
PENDING = 'Pending'
APPROVAL_STATUS_CHOICES = ((APPROVED,'Approved'),
                   (NOTAPPROVED,'Not Approved'),
                   (PENDING,'Pending',))





class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'CustomUser'
        verbose_name_plural = 'Users'
    
    FEMALE = 'F'
    MALE = 'M'
    UNSPECIFIED = 'U'  

    GENDER_CHOICES = ((FEMALE, 'Female'),
                (MALE, 'Male'),
                (UNSPECIFIED,'Unspecified'),
            )
    VISITOR = 'visitor'
    BUYER = 'buyer'
    SELLER = 'seller'
    ADMIN = 'admin'
    STAFF = 'staff'
    OWNER = 'owner'
    USERTYPE = (
            (VISITOR,"Visitor"),
            (BUYER,"Buyer"),
            (SELLER,"Seller"),
            (ADMIN,"Admin"),
            (STAFF,"Staff"),
            )
    
    YES = 'Y'
    NO = 'N'
    YesNoChoices = ((YES, 'Yes'),
                (NO, 'No'),)
    #is_seller = models.BooleanField(default=False)
    #is_buyer = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    password_expire_date =models.DateTimeField(('Password Expire Date'), default=timezone.now)
    gender = models.CharField(max_length =1, choices=GENDER_CHOICES,default=UNSPECIFIED)

    date_of_birth = models.DateTimeField(('date of birth'), default=timezone.now)
       
    #buyer_profile_pic = models.ImageField(upload_to = profile_pic_file_path,null=True,blank=True,max_length=500)

    contact_number = models.CharField(max_length=15,default=0,blank=True)
    alternate_contact_number = models.CharField(max_length=15,default=0, null=True,blank=True)
    parent_id = models.IntegerField(default=0, blank = True, null = False)
        

    date_created = models.DateTimeField(('date created'), default=timezone.now)
    date_updated = models.DateTimeField(('date created'), default=timezone.now)

    #user_type = models.IntegerField(default=0, blank = True)
    # user_type = models.IntegerField(default=VISITOR, blank = True, 
    #                                     choices=USERTYPE,null = False,
    #                                     ) 
    user_type = models.CharField(default=BUYER, blank = True, 
                                         choices=USERTYPE,null = True,
                                         )
    otp = models.CharField(max_length=6, blank=True, null=True)
    #deleted = models.CharField(max_length=1, default='Y')  # 'Y' means deleted, 'N' means not deleted
    is_deleted = models.CharField(default=YES, blank = False, 
                                        choices=YesNoChoices,null = False,
                                        ) 
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Changed to avoid conflict
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
         )
    
    user_permissions = models.ManyToManyField(
            'auth.Permission',
            related_name='customuser_set_permissions',  # Changed to avoid conflict
            blank=True,
            help_text="Specific permissions for this user.",
            verbose_name="user permissions"
        )
    
    

    def approve_user(self):
        """ Set the user as approved and not deleted """
        self.is_deleted = self.NO
        self.is_phone_verified=True
        self.save()

    def soft_delete_user(self):
        """ Soft delete the user by setting 'deleted' flag to 'Y' """
        self.deleted = self.YES
        self.is_phone_verified=False
        self.save()

    def __str__(self):
        return f"{self.username} Email: {self.email}"

    
    @property
    def is_seller(self):
        return self.user_type == self.SELLER
                
    @property     
    def is_buyer(self):
        return self.user_type == self.BUYER
     

    @property
    def is_admin(self):
        if self.user_type == self.ADMIN:
            return True
        
    @property
    def is_owner(self):
        if self.user_type == self.OWNER:
            return True

# accounts/models.py
#Buyer model - holds buyer details
class Buyer(models.Model):
    class Meta:
        verbose_name = 'Buyer'
        verbose_name_plural = 'Buyers'

    YES = 'Y'
    NO = 'N'
    YesNoChoices = ((YES, 'Yes'),
                (NO, 'No'),)
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    is_deleted = models.CharField(default=YES, blank = False, choices=YesNoChoices,
                               null = False,)   # 'Y' means deleted, 'N' means not deleted
    buyer_profile_pic = models.ImageField(upload_to = profile_pic_file_path,null=True,blank=True,max_length=500)
    introducer = models.CharField(max_length=200,default="Unknown",blank=True)
    date_created = models.DateTimeField(('date created'), default=timezone.now)
    date_updated = models.DateTimeField(('date created'), default=timezone.now)
    is_active = models.CharField(default=YES, blank = False, choices=YesNoChoices,
                               null = False,)   # 'Y' means active, 'N' means not active
    description =models.TextField(blank=True,null=True)
    
    aadhaar_number = models.CharField(default="000000000000", max_length=12,
                                          verbose_name=("Aadhaar Number"),
                                          null=True,blank=True) # Optional

    pan = models.CharField(default="000000000000",max_length=12,
                               verbose_name=("Permanent Account Number"),null=True,blank=True) # Optional

    organization_name = models.CharField(max_length=300,default="individual",null=True,blank=True) 
    age = models.IntegerField(default=0, blank = True, null = False) 
    language = models.CharField(
       max_length=100,
        default='English',
        verbose_name=("Language"),null=True,blank=True)
    
    def __str__(self):
        return f"Profile of {self.user.username} Email: {self.user.email} (Buyer)"


    def approve_buyer(self):
        self.is_deleted = self.NO
        self.is_active=self.YES
        #self.is_phone_verified = True
        
        self.save()

class Address(models.Model):
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)     

    ADDRESS_TYPE = (("Home", "Home"),
                    ("Office", "Office"),
                    ("Other", "Other"),)
    postal_address = models.TextField(default='Not specified',blank=True,null=True)
    address_type =models.CharField(default="Home",choices=ADDRESS_TYPE,blank=True,null=True)
    district = models.CharField(default="Not Specified", max_length=200,null=True,blank=True) # Optional
    state = models.CharField(default="Not Specified", max_length=200,null=True,blank=True) # Optional
    country = models.CharField(default="India", max_length=200,null=True,blank=True) # Optional
    pin = models.IntegerField(default=000000,
                 verbose_name=("Postal Index Number"),null=True,blank=True)
    
    def __str__(self):
        return f"Address of {self.user.username}, Name: {self.user.first_name}"

# accounts/models.py
# Seller model - holds seller details
class Seller(models.Model):
    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'

    YES = 'Y'
    NO = 'N'
    YesNoChoices = ((YES, 'Yes'),
                (NO, 'No'),)
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_deleted = models.CharField(default=YES, blank = False,choices=YesNoChoices,
                               null = False,)   # 'Y' means deleted, 'N' means not deleted
    introducer = models.CharField(max_length=200,default=0,blank=True)
    date_created = models.DateTimeField(('date created'), default=timezone.now)
    date_updated = models.DateTimeField(('date created'), default=timezone.now)
    is_active = models.CharField(default=YES, blank = False, choices=YesNoChoices,
                               null = False,)   # 'Y' means active, 'N' means not active
    is_approved = models.CharField(default=YES, blank = False, choices=YesNoChoices,
                               null = False,)   # 'Y' means active, 'N' means not active
    approval_status = models.CharField(max_length=200,default="Pending",blank=True)
    approved_by = models.CharField(max_length=200,default='Unknown',blank=True)
    approved_date = models.DateTimeField(('date created'), default=timezone.now)
    store_name = models.CharField(max_length=255)
    store_description = models.TextField()
    store_approved = models.BooleanField(default=False)
    store_address = models.TextField()
    
    bank_name =models.CharField(max_length=200)
    bank_branch =models.CharField(max_length=200)
    account_no =models.CharField(max_length=100)
    ifsc = models.CharField(max_length=100)
    seller_profile_pic = models.ImageField(upload_to = profile_pic_file_path,null=True,blank=True,max_length=500)
    status = models.CharField(max_length=100,choices=STATUS_CHOICES,default=ACTIVE)
    description =models.TextField()
    postal_address = models.TextField(default='Not specified',blank=True,null=True)
    branch =models.CharField(max_length=100)
    district = models.CharField(default="Not Specified", max_length=200,null=True,blank=True) # Optional
    state = models.CharField(default="Not Specified", max_length=200,null=True,blank=True) # Optional
    country = models.CharField(default="India", max_length=200,null=True,blank=True) # Optional
    pin = models.IntegerField(default=000000,
                 verbose_name=("Postal Index Number"),null=True,blank=True)
    aadhaar_number = models.CharField(default="000000000000", max_length=12,
                                          verbose_name=("Aadhaar Number"),
                                          null=True,blank=True) # Optional

    pan = models.CharField(default="000000000000",max_length=12,
                               verbose_name=("Permanent Account Number"),null=True,blank=True) # Optional

    gstn = models.CharField(default="0000000000",max_length=100,
                               verbose_name=("GST Number"),null=True,blank=True) # Optional

    organization_name = models.CharField(max_length=300,default="individual",null=True,blank=True) 
    age = models.IntegerField(default=0, blank = True, null = False) 
    language = models.CharField(
       max_length=100,
        default='English',
        verbose_name=("Language"),null=True,blank=True)


    def __str__(self):
        return f"Store {self.store_name} owned by {self.user.username}, Email {self.user.email}"

    def approve_seller(self):
        self.approval_status="Approved"
        self.is_deleted = self.NO
        self.is_active=self.YES
        self.is_approved=self.YES
        self.save()

class UserKYC(models.Model):
    class Meta:
        verbose_name = 'UserKYC'
        verbose_name_plural = 'KYCDocs'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)     
    profile_image = models.ImageField(upload_to = user_kyc_image_path,null=True,blank=True,max_length=500)
    aadhaar_image = models.ImageField(upload_to = user_kyc_image_path,null=True,blank=True,max_length=500)
    pan_image = models.ImageField(upload_to = user_kyc_image_path,null=True,blank=True,max_length=500)
    bankstatement_image = models.ImageField(upload_to = user_kyc_image_path,null=True,blank=True,max_length=500)
    affidavit_image = models.ImageField(upload_to = user_kyc_image_path,null=True,blank=True,max_length=500)
    gst_image = models.ImageField(upload_to = user_kyc_image_path,null=True,blank=True,max_length=500)\
    
    def __str__(self):
        return f"KYC of {self.user.username} - {self.user.first_name}"

     
     
     