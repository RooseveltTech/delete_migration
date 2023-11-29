from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, Max
from main.models import GameBatch, GameTicket, TicketType, WinnerTable

@receiver(post_save, sender=TicketType)
def create_batch(sender, instance, created, **kwargs):

    """This function creates a batch when an item is created
    """
    if created:
        GameBatch.objects.create(
            ticket_type = instance
        )

@receiver(post_save, sender=GameTicket)
def game_decision(sender, instance, created, **kwargs):

    """This function creates a batch when an item is created
    """
    if created:
        batch_ins = GameBatch.objects.filter(ticket_type=instance.ticket, is_completed=False).last()
        game_ins = GameTicket.objects.filter(game_batch=batch_ins, is_paid=True)
        amount_paid = game_ins.aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
        if instance.ticket.ticket_draw_amount <= 0:
            pass
        else:
            if amount_paid >= instance.ticket.ticket_draw_amount:

                all_users = (
                                game_ins.order_by().values("email").distinct()
                            )
                winner = None
                winning_amount = 0.0
                for user in all_users:
                    this_winner = game_ins.filter(email=user["email"])
                    user_winning_amount = this_winner.filter(email=user["email"]).aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
                    if winner is None:
                        winner = this_winner.first()
                        winning_amount = user_winning_amount
                    else:
                        if user_winning_amount > winning_amount:
                            winner = this_winner.first()
                            winning_amount = user_winning_amount
                WinnerTable.objects.create(
                    phone_number = winner.phone_number,
                    email = winner.email,
                    game_batch = winner.game_batch,
                    first_name = winner.first_name,
                    last_name = winner.last_name,
                    game_id = winner.game_id,
                    game_pin = winner.game_pin
                )
                batch_ins.is_completed = True
                batch_ins.save()

                GameBatch.objects.create(
                    ticket_type = instance.ticket
                )
    else:
        batch_ins = GameBatch.objects.filter(ticket_type=instance.ticket, is_completed=False).last()
        game_ins = GameTicket.objects.filter(game_batch=batch_ins, is_paid=True)
        amount_paid = game_ins.aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
        if instance.ticket.ticket_draw_amount <= 0:
            pass
        else:
            if amount_paid >= instance.ticket.ticket_draw_amount:

                all_users = (
                                game_ins.order_by().values("email").distinct()
                            )
                winner = None
                winning_amount = 0.0
                for user in all_users:
                    this_winner = game_ins.filter(email=user["email"])
                    user_winning_amount = this_winner.filter(email=user["email"]).aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
                    if winner is None:
                        winner = this_winner.first()
                        winning_amount = user_winning_amount
                    else:
                        if user_winning_amount > winning_amount:
                            winner = this_winner.first()
                            winning_amount = user_winning_amount
                WinnerTable.objects.create(
                    phone_number = winner.phone_number,
                    email = winner.email,
                    game_batch = winner.game_batch,
                    first_name = winner.first_name,
                    last_name = winner.last_name,
                    game_id = winner.game_id,
                    game_pin = winner.game_pin
                )
                batch_ins.is_completed = True
                batch_ins.save()

                GameBatch.objects.create(
                    ticket_type = instance.ticket
                )

        
