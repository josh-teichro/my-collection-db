from gmail_importer import import_gmail
from core import *

partial_data_file_path = "C:\\Users\\josh\\Downloads\\takeout-20260507T001500Z-3-001\\Takeout\\Mail\\Receipt-Figure Collection.mbox"
full_data_file_path = "C:\\Users\\josh\\Downloads\\takeout-20260522T015007Z-3-001\\Takeout\\Mail\\All mail Including Spam and Trash.mbox"

def main():
    orders = import_gmail(partial_data_file_path)

    #print_orders(orders)

    items = find_items(["Frieren", "blu", "ray"], FindMode.ALL, orders)
    print_items(items)

main()