from django.contrib.auth import get_user_model
from import_export import resources

from main.models import GameBatch, GameTicket, TicketType, WinnerTable

User = get_user_model()


class UserResource(resources.ModelResource):
    class Meta:
        model = User

class GameTicketResource(resources.ModelResource):
    class Meta:
        model = GameTicket

class TicketTypeResource(resources.ModelResource):
    class Meta:
        model = TicketType

class GameBatchResource(resources.ModelResource):
    class Meta:
        model = GameBatch

class WinnerTableResource(resources.ModelResource):
    class Meta:
        model = WinnerTable