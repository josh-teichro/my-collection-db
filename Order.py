
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