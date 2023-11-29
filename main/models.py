import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password, check_password

from main.helpers.func import generate_game_id, generate_game_pin, generate_otp, generate_password, generate_slip_id
from django.db.models import Count, Sum

# Create your model(s) here.
class BaseModel(models.Model):
    """Base model for reuse.
    Args:
        models (Model): Django's model class.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser, BaseModel):
    """User model."""

    username = None
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    referral_code = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=125, null=True, blank=True)
    otp_code = models.CharField(max_length=125, null=True, blank=True)
    consent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    ip_address = models.CharField(max_length=1000, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return str(self.email)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'USER PROFILE'
        verbose_name_plural = 'USER PROFILES'

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def register_user(cls,
            phone_number,
            email, 
            first_name, 
            last_name, 
            country, 
            consent,
            ip_address
            ):
        otp_code = generate_otp()
        old_user = cls.user_exist(email)
        if old_user:
            user = User.objects.filter(email=email).first()
            user.otp_code = otp_code
            user.save()
        else:
            password = generate_password()
            cls.objects.create(
                phone_number=phone_number,
                email=email, 
                first_name=first_name,
                last_name=last_name, 
                country=country,
                consent=consent,
                ip_address=ip_address,
                password=make_password(password),
                otp_code=otp_code
            )
            print("email" ,email, "\n")
            print("pass" ,password, "\n")
        
    
    @classmethod
    def user_exist(cls, email):

        user = cls.objects.filter(email=email)
        if user:
            return user
        else:
            return None
        
class TicketType(BaseModel):
    ticket_name = models.CharField(max_length=255, null=True, blank=True)
    ticket_amount = models.FloatField(null=True, blank=True, default=0.0)
    ticket_draw_amount = models.FloatField(null=True, blank=True, default=0.0)
    ticket_count = models.FloatField(null=True, blank=True, default=0)
    ticket_paid_count = models.FloatField(null=True, blank=True, default=0)
    ticket_unpaid_count = models.FloatField(null=True, blank=True, default=0)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.ticket_name}"          

    class Meta:
        verbose_name = "TICKET TYPE"
        verbose_name_plural = "TICKET TYPES"

    def save(self, *args, **kwargs):
        if self.pk:
            item_ins = GameTicket.objects.filter(ticket__id=self.id)
            total_tickets = item_ins.aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
            total_paid_tickets = item_ins.filter(is_paid=True).aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
            total_unpaid_tickets = item_ins.filter(is_paid=False).aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
        
            self.ticket_count = total_tickets
            self.ticket_paid_count = total_paid_tickets
            self.total_unpaid_tickets = total_unpaid_tickets
        super().save(*args, **kwargs)

class GameTicket(BaseModel):
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    referral_code = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=1000, null=True, blank=True)
    ticket = models.ForeignKey("main.TicketType", on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="game_ticket_type")
    game_batch = models.ForeignKey("main.GameBatch", on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="game_batch")
    consent = models.BooleanField(default=False)
    is_played = models.BooleanField(default=False)
    game_id = models.CharField(max_length=255, null=True, blank=True)
    game_pin = models.CharField(max_length=255, null=True, blank=True)
    slip_id = models.CharField(max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    amount_paid = models.FloatField(null=True, blank=True, default=0.0)
    amount = models.FloatField(null=True, blank=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def register_ticket(cls, data, 
            phone_number,
            email, 
            first_name, 
            last_name, 
            country, 
            consent, 
            ip_address
        ):
        slip_id = generate_slip_id()
        for ticket in data:
            ticket_id = ticket.get("ticket_id")
            amount = ticket.get("amount")
            ticket_count = ticket.get("ticket_count")
            
            game_batch_ins = GameBatch.objects.filter(ticket_type__id=ticket_id, is_completed=False).last()
            
            ticket_ins = TicketType.objects.filter(id=ticket_id, is_active=True).first()
                
            game_id = generate_game_id()
            game_pin = generate_game_pin()
            for i in range(0, ticket_count):
                cls.objects.create(
                    ticket=ticket_ins, 
                    phone_number=phone_number,
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name, 
                    country=country, 
                    consent=consent,
                    slip_id=slip_id,
                    amount=amount,
                    game_id=game_id,
                    game_pin=game_pin,
                    game_batch=game_batch_ins
                )
                
        User.register_user(
            phone_number,
            email, 
            first_name, 
            last_name, 
            country, 
            consent,
            ip_address
            )
        
        
            

    class Meta:
        verbose_name = "GAME TICKET"
        verbose_name_plural = "GAME TICKETS"

class GameBatch(BaseModel):
    batch_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_type = models.ForeignKey("main.TicketType", on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="batch_ticket_type")
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.batch_id}"

    class Meta:
        verbose_name = "GAME BATCH"
        verbose_name_plural = "GAME BATCHES"

class WinnerTable(BaseModel):
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    game_batch = models.ForeignKey("main.GameBatch", on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="winner_batch")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    game_id = models.CharField(max_length=255, null=True, blank=True)
    game_pin = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "WINNER TICKET"
        verbose_name_plural = "WINNER TICKETS"



