from collections import namedtuple
from decimal import Decimal, getcontext

getcontext().prec = 30

Order = namedtuple('Order', 'id items')
Item = namedtuple('Item', 'type description amount quantity')

MAX_PAYMENT_LIMIT = Decimal('1e6')

def validorder(order: Order):
    net = Decimal(0.0)
    total_product_amount = Decimal(0.0)
    tolerance = Decimal('1e-16')

    for item in order.items:
        item_amount = Decimal(str(item.amount))
        item_quantity = Decimal(str(item.quantity))
        
        if item_quantity != item.quantity or item_quantity <= 0:
            return "Invalid item quantity: %s" % item.quantity
        
        if item.type == 'payment':
            net += item_amount
        elif item.type == 'product':
            total_product_amount += item_amount * item_quantity
            net -= item_amount * item_quantity
        else:
            return "Invalid item type: %s" % item.type

    # Check if total product amount exceeds the maximum limit
    if total_product_amount > MAX_PAYMENT_LIMIT:
        return "Total amount payable for an order exceeded"

    # Check if net is effectively zero within the tolerance range
    if abs(net) < tolerance:
        return "Order ID: %s - Full payment received!" % order.id
    else:
        return "Order ID: %s - Payment imbalance: $%0.2f" % (order.id, net)
