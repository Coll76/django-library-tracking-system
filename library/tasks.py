#tasks.py
from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from datetime import timezone, timedelta



@shared_task(max_retries=3, max_delay=300) #There are a total of 3 retries if it fails. 5min delay btwn each retry
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
        return f'Successfully booked Loan {loan_id}'
    except Loan.DoesNotExist:
        return f'Loan {loan_id} does not exist'
    except Exception as e:
        return f'Error processing return: {str(e)}'


@shared_task(max_retries=3)
def check_overdue_loans():
    today = timezone.now().date()
    overdue_loans = Loan.objects.filter(
        is_returned = False,
        return_date_lte = today
    )
    for loan in overdue_loans:
        try:
            member_email = loan.member.user.email
            member_name = loan.member.user.username
            date_due = loan.due_date
            book_title = loan.book.title
            
           
            send_mail(
                subject='Overdue Notification',
                message=f'Hello {member_name},\n\nThis is to inform you that the Loan {loan} for "{book_title}" is overdue.\nPlease return it by the due date.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[member_email],
                fail_silently=False,
            )
            return f'Successfully sent the overdue date for loan {loan}'
        except Loan.DoesNotExist:
            return f'Loan {Loan} does not exist'
            