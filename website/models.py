from django.db import models
from django.utils import timezone


class Record(models.Model):
    STATUS_CHOICES = [
        ('prospect', 'Prospect'),
        ('customer', 'Customer'),
        ('lead', 'Lead'),
        ('partner', 'Partner'),
    ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=10)
    
    # New fields
    is_active = models.BooleanField(default=True)
    customer_type = models.CharField(max_length=20, choices=STATUS_CHOICES, default='prospect')
    notes = models.TextField(blank=True, null=True)
    last_contacted = models.DateTimeField(blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")


class CallHistory(models.Model):
    CALL_TYPE_CHOICES = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('missed', 'Missed'),
    ]
    
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='call_history')
    call_type = models.CharField(max_length=20, choices=CALL_TYPE_CHOICES)
    duration_seconds = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    called_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-called_at']
    
    def __str__(self):
        return f"{self.record.first_name} - {self.get_call_type_display()} - {self.called_at.strftime('%Y-%m-%d %H:%M')}"


class Email(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='emails')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.record.first_name} - {self.subject}"


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.record.first_name} - {self.title}"