
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