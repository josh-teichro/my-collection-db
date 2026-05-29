from datetime import datetime
import re
import mailbox
from parse_util import *
from Order import Order
from Item import Item


def import_gmail(file_path):
    emails = mailbox.mbox(file_path)
    return get_orders(emails)

def get_orders(emails):
    orders = []

    for email in emails:
        if email.get("From") == "e_support@amiami.com":
            orders.append(parse_order(email))

    orders = sorted(orders, key=lambda order: order.date) 
    return orders

def parse_order(email) -> Order:
    order = Order()

    lines = email.get_payload().splitlines()
    
    # Date
    try:
        order.date = datetime.strptime(email.get("Date"), '%a, %d %b %Y %H:%M:%S %z')
    except:
        raise Exception("Failed to parse date.")
    
    # Order Number
    try:
        m = get_line(r'^Order Number:\s?(.*)', lines)
        order.order_num = m.group(1)
    except:
        raise Exception("Failed to parse order number.")

    # Items
    m = get_line(r'^Order Number:\s?(\d*)', lines)
    item_start_idx = lines.index(m.group(0))
    i = item_start_idx + 1

    while (not lines[i].startswith("Subtotal")):
        if (not lines[i] or lines[i].isspace()):
            i += 1
            continue

        item = Item()
        item.name = lines[i]
        m = re.search(r'^Unit price (\d+) JPY x (\d+) unit\(s\) = (\d+) JPY\s?$', lines[i+1])

        if (not m):
            i += 2
            raise Exception(f"Failed to parse item.\n0:{lines[i]}\n1:{lines[i+1]}")

        item.cost = int(m.group(1))
        order.items.append(item)
        i += 2

    # Subtotal
    try:
        m = get_line(r'^Subtotal:\s?((\d|\,)+) JPY', lines)
        order.subtotal = int(m.group(1).replace(',',''))
    except:
        raise Exception(f"Failed to parse subtotal of order: {order.order_num}")
    
    # Shipping
    try:
        m = get_line(r'^Shipping:\s?((\d|\,)+) JPY', lines)
        order.shipping = int(m.group(1).replace(',',''))
    except:
        raise Exception(f"Failed to parse shipping of order: {order.order_num}")
    
    # Total
    try:
        m = get_line(r'^Grand (?:t|T)otal:\s?((\d|\,)+) JPY', lines)
        order.total = int(m.group(1).replace(',',''))
    except:
        raise Exception(f"Failed to parse total of order: {order.order_num}")

    return order
