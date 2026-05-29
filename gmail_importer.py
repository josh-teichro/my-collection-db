from datetime import datetime
import re
import pkgutil
import os
import encodings
import mailbox

partial_data_file_path = "C:\\Users\\josh\\Downloads\\takeout-20260507T001500Z-3-001\\Takeout\\Mail\\Receipt-Figure Collection.mbox"
full_data_file_path = "C:\\Users\\josh\\Downloads\\takeout-20260522T015007Z-3-001\\Takeout\\Mail\\All mail Including Spam and Trash.mbox"


def main():
    with open(partial_data_file_path, 'r') as f_in:
        content = f_in.read()
        orders = parse_orders(content)

        #print_orders(orders)

        items = find_items(["Frieren", "blu", "ray"], FindMode.ALL, orders)
        print_items(items)

    #with open(partial_data_file_path, 'r', encoding='utf_8') as f_in:
    #    content = f_in.read(1000000)
    #    emails = get_blocks(content, start=r"(?s)(?=.*^Message-Id:.*$)(?=.*^From:\s?(.*?@.*?)$)(?=.*^Date:\s?(.*?)$).+?(?=\n\n)", num_blocks=1)
    #    print_emails(emails)

    #emails = mailbox.mbox(partial_data_file_path)
    #emails = [email for email in emails if email.get("From") == "e_support@amiami.com"]
#
    #for email in emails:
    #    if (email.get("From") == "e_support@amiami.com"):
    #        print("===============================================================")
    #        print(email.get_payload())
    #        print("===============================================================")
    #        input("...")


class FindMode:
    ANY = "ANY"
    ALL = "ALL"

def find_items(terms, mode, orders):
    found_items = []

    for order in orders:
        for item in order.items:
            if (mode == FindMode.ANY):
                for term in terms:
                    if term.lower() in item.name.lower():
                        found_items.append(item)
                        break;
            elif (mode == FindMode.ALL):
                fail = False

                for term in terms:
                    if term.lower() not in item.name.lower():
                        fail = True
                        break;
                
                if not fail:
                    found_items.append(item)
            else:
                raise Exception(f"Invalid find mode: '{mode}'");


    return found_items

def print_emails(emails):
    for email in emails:
        print("===============================================================")
        if len(email) > 100:
            print(email[:100] + "...")
        else:
            print(email)
        print("===============================================================")

def print_orders(orders):
    for order in orders:
        print(order)
        print()

    print("===============================================================")
    print(f"# of orders: {len(orders)}")
    print(f"Subtotal of all orders: {sum([order.subtotal for order in orders])}")
    print(f"Shipping of all orders: {sum([order.shipping for order in orders])}")
    print(f"Total of all orders: {sum([order.total for order in orders])}")
    print("===============================================================")

def print_items(items):
    for item in items:
        print(item)

    print("===============================================================")
    print(f"# of items: {len(items)}")
    print(f"Total of all items: {sum([item.cost for item in items])}")
    print("===============================================================")

def parse_orders(content):
    emails = get_blocks(content, start="Delivered-To: josh.teichro@gmail.com")
    
    orders = [parse_order(email) for email in emails]
    orders = sorted(orders, key=lambda order: order.date) 

    return orders

def get_blocks(content, start, num_blocks = -1):
    blocks = []
    
    count = 0
    cur = re.search(start, content)

    while cur and (count < num_blocks or num_blocks < 0):
        next_content = content[cur.span()[1]:]
        next = re.search(start, next_content)

        if next:
            blocks.append(content[cur.span()[0]:cur.span()[1] + next.span()[0]])
        else:
            blocks.append(content[cur.span()[0]:])

        cur = next
        content = next_content
        count += 1

    return blocks

class Order:
    def __init__(self):
        self.order_num = 0
        self.date = None
        self.date_str = "Not Set"
        self.items = []
        self.subtotal = 0
        self.shipping = 0
        self.total = 0

    def __str__(self):
        return f"[Order: {self.order_num}, Date: {self.date.astimezone().strftime('%Y/%m/%d %H:%M:%S')}, Subtotal: {self.subtotal} JPY, Shipping: {self.shipping} JPY, TOTAL: {self.total} JPY]" \
            + '\n\t' + '\n\t'.join([str(i) for i in self.items ])
    
class Item:
    def __init__(self):
        self.name = ""
        self.cost = 0

    def __str__(self):
        return f"[Item: {self.name}, Cost: {self.cost}]"

def parse_order(email: str) -> Order:
    order = Order()

    lines = email.splitlines()
    #m = re.search(r'Date: (\N*)', lines)
    # Date
    try:
        m = get_line(r'^Date:\s?(.*)', lines)
        order.date = datetime.strptime(m.group(1), '%a, %d %b %Y %H:%M:%S %z')
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

def get_line(regex, lines):
    for line in lines:
        m = re.search(regex, line)

        if (m):
            return m
    
    return None

main()