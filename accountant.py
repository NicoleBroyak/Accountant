from module.input import input_mode

account_values = []
account_comments = []
account_balance = 0
trade_items = dict()
operations_type = []
operations = []
inputlog = []
mode = ''
index, index_balance, index_purch, index_sell, account_balance = 0, 0, 0, 0, 0


# sciezki programu:
# 1. Saldo:
#     - jeżeli saldo mniejsze niż wypłata - "za mało pieniędzy"
# 2. Zakup:
#     - jeżeli brak towaru: - dodaj do słownika wraz z ilością sztuk
#     - jeżeli towar już jest: - zwiększ stan magazynowy
#     - jeżeli koszt zakupu większy od salda - "za mało pieniędzy"
# 3. Sprzedaż:
#     - jeżeli brak towaru lub towaru mniej niż sprzedawane: - błąd "brak towaru"
#     - jeżeli towar jest: zmniejsz stan magazynowy

def input_trade():
    item_name = input("Please type item name")
    item_price = int(input("Please type item price"))
    item_quantity = int(input("Please type item quantity"))
    return item_name, item_price, item_quantity

def input_balance():
    account_value = int(input("Please type operation value (in gr)"))
    account_comment = input("Please type operation description")
    while account_balance > account_value:
        account_value = (int(input(
                        "Please type operation value (in gr)"))
        )
        account_comment = input("Please type operation description")
    return account_value, account_comment
    

def input_check_balance(account_value = 0, account_comment = ""):
        if account_balance + account_value < 0:
            while account_balance + account_value < 0:
                account_value = (int(input(
                                "ERROR Please type operation value (in gr)")))
                account_comment = input("Please type operation description")
        return account_value, account_comment


def item_loop_purch(item_price, item_quantity, trade_items, item_name):
    while ((item_price <= 0) or (item_quantity <= 0)):
            item_price = (
            int(input("ERROR Please type correct item price"))
            )
            item_quantity = (
            int(input("ERROR Please type corect item quantity"))
            )
    return item_price, item_quantity


def item_loop_sell(item_price, item_quantity, trade_items, item_name):
    while ((item_price <= 0) or (item_quantity <= 0)
        or (trade_items[item_name] < item_quantity)):
            item_price = (
            int(input("ERROR Please type correct item price"))
            )
            item_quantity = (
            int(input("ERROR Please type corect item quantity"))
            )
    return item_price, item_quantity

def input_check_sell(item_name = "",item_price = 0, item_quantity = 0):
    while item_name not in trade_items:
        item_name = input("ERROR: Please type correct item name")
    item_price, item_quantity = item_loop_sell(item_price, item_quantity, trade_items, item_name)
    return item_name, item_price, item_quantity


def input_check_purch(item_name = "",item_price = 0, item_quantity = 0):
    item_price, item_quantity = item_loop_purch(item_price, item_quantity, trade_items, item_name)
    return item_name, item_price, item_quantity

def trade_items_check(mode, item_name):
    if mode == "zakup":
        if item_name not in trade_items:
            trade_items[item_name] = item_quantity
        else:
            trade_items[item_name] += item_quantity
    if mode == "sprzedaż":
        trade_items[item_name] -= item_quantity

def oper_append_balance(index_balance=index_balance, index=index, mode=mode):
    account_values.append(account_value)
    account_comments.append(account_comment)
    operations_type.append(mode)
    operations.append(f"Operation in mode 'saldo' number"
                        f" {str(index_balance + 1)}:"
                        f" {str(account_values[index_balance])} - "
                        f"description: {account_comments[index]}")

def oper_append_purch(index_purch=index_purch, mode=mode):
    operations_type.append(mode)
    operations.append(f"Operation in mode 'zakup'" 
                        f"number {str(index_purch + 1)}:"
                        f"Item:{item_name} purchased {item_quantity}"
                        f" pcs for price {item_price}gr")

def oper_append_sell(index_sell=index_sell, mode=mode):
    operations_type.append(mode)
    operations.append(f"Operation in mode 'sprzedaż' number"
                        f"{str(index_sell + 1)}:"
                        f"Item:{item_name} sold {item_quantity}" 
                        f" pcs for price {item_price}gr")

def inputlog_extend(mode=mode):
    if mode == "saldo":
        inputlog.extend(mode, account_values[-1], account_comments[-1])
    if mode == "zakup":
        inputlog.extend(mode, item_name, item_price, item_quantity)
    if mode == "sprzedaż":
        inputlog.extend(mode, item_name, item_price, item_quantity)
    return

ALLOWED_COMMANDS = "saldo", "sprzedaż", "zakup", "stop", "end"

with open("output.txt", mode="w") as file:
    file.write("")
mode = input_mode(ALLOWED_COMMANDS)
while mode in ALLOWED_COMMANDS:
    if mode == "saldo":
        account_value, account_comment = input_balance()
        account_value, account_comment = (
        input_check_balance(account_value, account_comment)
        )
        account_balance += account_value
        oper_append_balance(index_balance, index, mode)
        inputlog.extend([mode, account_value, account_comment])
        index_balance += 1
        index += 1
    if mode == "zakup":
        item_name, item_price, item_quantity = input_trade()
        item_name, item_price, item_quantity = (
        input_check_purch(item_name, item_price, item_quantity)
        )
        trade_items_check(mode, item_name)
        account_balance -= item_price * item_quantity
        inputlog.extend([mode, item_name, item_price, item_quantity])
        oper_append_purch()
        index_purch += 1
        index += 1
    if mode == "sprzedaż":
        item_name, item_price, item_quantity = input_trade()
        item_name, item_price, item_quantity = (
        input_check_sell(item_name, item_price, item_quantity)
        )
        trade_items_check(mode, item_name)
        account_balance += item_price * item_quantity
        inputlog.extend([mode, item_name, item_price, item_quantity])
        oper_append_sell()
        index_sell += 1
        index += 1
    if mode == "stop":
        print(f"Number of operations: {index}\n")
        index_first = int(input("Please type first operation to view:"))
        index_last = int(input("Please type last operation to view:"))
        index = 1
        with open("output.txt", mode="a") as file:
            file.write(f"\n\n\nAccount balance: {account_balance}\n")
            file.write("Items on stock:\n")
            for item_name, item_quantity in trade_items.items():
                file.write(f"{item_name}: {item_quantity} pcs\n")
            file.write("\nSummary:\n")
            for i in operations:
                if index >= index_first and index_first <= index_last:
                    file.write(f"Operation nr {index}:\nmode: "
                               f"{operations_type[index - 1]}\n{i}\n\n")
            if index == index_last:
                break
            index += 1
            file.write("\nCorrect input log:")
            for i in inputlog:
                file.write(str(i) + "\n")
        mode = "end"
        break
    mode = input_mode(ALLOWED_COMMANDS)
