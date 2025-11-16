from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.username

    # This should actually be a normal instance method, just wanted to demonstrate that I know the difference
    # def to_dms(self, lat_or_lon="lat"):
    #   if lat_or_lon == "lat":
    #       value = self.latitude
    #   else:
    #       value = self.longitudue
    #   ...

    @staticmethod
    def to_dms(value, lat_or_lon="lat"):
        """
        Convert a decimal latitude or longitude value to Degrees, Minutes, Seconds (DMS) format.
        """
        degrees = int(abs(value))
        minutes_float = (abs(value) - degrees) * 60
        minutes = int(minutes_float)
        seconds = round((minutes_float - minutes) * 60)

        direction = ""
        if lat_or_lon == "lat":
            direction = "N" if value >= 0 else "S"
        else:
            direction = "E" if value >= 0 else "W"

        return f"{degrees}°{minutes}'{seconds}\"{direction}"

    @property
    def position(self):
        """
        Return formatted DMS coordinates, or None if missing.
        """
        if not all([self.latitude, self.longitude]):
            return None
        lat_dms = self.to_dms(self.latitude)
        lon_dms = self.to_dms(self.longitude, lat_or_lon="lon")
        return f"{lat_dms} {lon_dms}"
