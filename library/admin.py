from django.contrib import admin
from .models import Author, Book, Member, Loan
from .tasks import send_loan_notification

""" class LoanAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        
        if is_new:
            send_loan_notification.delay(obj.id) """
            
            
""" class LoanAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        new_obj = obj.pk is None
        super().save_model(request, obj, form, change)
        if new_obj:
            send_loan_notification.delay(obj.id)
             """

class LoanAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        new_obj = obj.pk is None
        super().save_model(request, obj, form, change)  
        
        if new_obj:
              send_loan_notification.delay(obj.id)
    

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Loan, LoanAdmin)
