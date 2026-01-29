from services.tickets import mark_ticket_paid

def handle_payment(ticket_id):
    mark_ticket_paid(ticket_id)
    return "✅ Pagamento confirmado!\nSeu ticket está em processamento."
