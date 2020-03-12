from django.contrib import admin
from .models import Category, CCY, Transactions

# Register your models here.

#admin.site.register(Transactions)
admin.site.register(CCY)
admin.site.register(Category)

class TransactionsAdmin(admin.ModelAdmin):
    """Administration object for Transactions models.
    Defines:
     - fields to be displayed in list view (list_display)
    """
    list_display = ('tr_date', 'tr_time', 'tr_direction', 'display_sum', 'CCY', 'display_category', 'Content')
    
admin.site.register(Transactions, TransactionsAdmin)