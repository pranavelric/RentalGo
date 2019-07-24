from django.contrib import admin
from .models import Product, Order, BuyOrder, Contact


# Register your models here.
def save_model(self, request, obj, form, change):
    # associating the current logged in user to the client_id
    obj.owner = request.user
    super().save_model(request, obj, form, change)

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(BuyOrder)
admin.site.register(Contact)