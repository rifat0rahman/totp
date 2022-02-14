from django.db import models
import pyotp
# Create your models here.
class Device(models.Model):
    location_ID = models.AutoField(primary_key=True)
    seed = models.CharField(max_length=50,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    otp = models.CharField(max_length=50,default=00,null=True,blank=True)

    def save(self,*args, **kwargs):
        if not self.seed:
            self.seed = pyotp.random_base32()
        
        return super(Device,self).save(*args, **kwargs)

    
    def __str__(self) -> str:
        display = f'{self.seed}'
        return display


class Authenticate(models.Model):
    location_ID = models.AutoField(primary_key=True)
    totp = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self) -> str:
        display = f'{self.location_ID} + {self.totp} + {self.created}'
        return display


class TOTP(models.Model):
    totp = models.CharField(max_length=50)
    seed = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        display = f'{self.totp} + {self.seed}'
        return display