import sys

account_values = []
account_comments = []
account_balance = 0
trade_items = dict()
operations_type = []
operations = []
inputlog = []
mode = sys.argv[1]
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

def acc_input(mode):
    if mode == "zakup" or mode == "sprzedaż":
        item_name = input("Please type item name")
        item_price = int(input("Please type item price"))
        item_quantity = int(input("Please type item quantity"))
        return mode, item_name, item_price, item_quantity
    if mode == "saldo":
        account_value = int(input("Please type operation value (in gr)"))
        account_comment = input("Please type operation description")
        if account_balance < account_value:
            while account_balance < account_value:
                account_value = (int(input(
                                "Please type operation value (in gr)"))
                )
                account_comment = input("Please type operation description")
        return mode, account_value, account_comment
    

def input_check(mode,item_name = "",item_price = \
    0, item_quantity = 0, account_value = 0, account_comment = ""):
    if mode == "saldo":
        if account_balance + account_value < 0:
            while account_balance + account_value < 0:
                account_value = (int(input(
                                "ERROR Please type operation value (in gr)")))
                account_comment = input("Please type operation description")
        return account_value, account_comment
    if mode == "sprzedaż":
        if item_name not in trade_items:
            while item_name not in trade_items:
                item_name = input("ERROR: Please type correct item name")
        if (
        (item_price <= 0) or (item_quantity <= 0)
        or (trade_items[item_name] < item_quantity)
        ):
            while ((item_price <= 0) or (item_quantity <= 0)
            or (trade_items[item_name] < item_quantity)):
                item_price = (
                int(input("ERROR Please type correct item price"))
                )
                item_quantity = (
                int(input("ERROR Please type corect item quantity"))
                )
        return item_name, item_price, item_quantity
    if mode == "zakup":  
        if ((item_price <= 0) or (item_quantity <= 0)
        or (account_balance < item_price*item_quantity)
        ):
            while ((item_price <= 0) or (item_quantity <= 0)
            or (account_balance < item_price*item_quantity)):
                item_price = (int(input(
                "ERROR Please type correct item price")))
                item_quantity = (int(input(
                "ERROR Please type corect item quantity")))
        return item_name, item_price, item_quantity

def trade_items_check(mode):
    if mode == "zakup":
        if item_name not in trade_items:
            trade_items[item_name] = item_quantity
        else:
            trade_items[item_name] += item_quantity
    if mode == "sprzedaż":
        trade_items[item_name] -= item_quantity
    return

def oper_append(index_mode, index, mode):
    if mode == "saldo":
        account_values.append(account_value)
        account_comments.append(account_comment)
        operations_type.append(mode)
        operations.append(f"Operation in mode 'saldo' number"
                          f" {str(index_mode + 1)}:"
                          f" {str(account_values[index_mode])} - "
                          f"description: {account_comments[index]}")
        return
    if mode == "zakup":
        operations_type.append(mode)
        operations.append(f"Operation in mode 'zakup'" 
                          f"number {str(index_mode + 1)}:"
                          f"Item:{item_name} purchased {item_quantity}"
                          f" pcs for price {item_price}gr")
        return
    if mode == "sprzedaż":
        operations_type.append(mode)
        operations.append(f"Operation in mode 'sprzedaż' number"
                          f"{str(index_mode + 1)}:"
                          f"Item:{item_name} sold {item_quantity}" 
                          f" pcs for price {item_price}gr")
        return

def inputlog_extend(mode):
    if mode == "saldo":
        inputlog.extend(mode, account_values[-1], account_comments[-1])
    if mode == "zakup":
        inputlog.extend(mode, item_name, item_price, item_quantity)
    if mode == "sprzedaż":
        inputlog.extend(mode, item_name, item_price, item_quantity)
    return

def input_mode():
    mode = input("Please type mode:")
    while mode not in allowed_commands:
        mode = input("Please type mode:")
    return mode

allowed_commands = "saldo", "sprzedaż", "zakup", "stop", "end"
if mode == "saldo":
    account_value = int(sys.argv[2])
    account_comment = sys.argv[3]
    account_value, account_comment = \
    input_check(mode, 0, 0, 0, account_value, account_comment)
    account_balance += account_value
    oper_append(index_balance, index, mode)
    inputlog.extend([mode, account_value, account_comment])
    index_balance += 1
    index += 1
if mode == "zakup":
    item_name = sys.argv[2]
    item_price = int(sys.argv[3])
    item_quantity = int(sys.argv[4])
    item_name, item_price, item_quantity = \
    input_check(mode, item_name, item_price, item_quantity)
    trade_items_check(mode)
    inputlog.extend(mode, item_name, item_price, item_quantity)
    account_balance -= item_price * item_quantity
    index_purch += 1
    index += 1
if mode == "sprzedaż":
    item_name = sys.argv[2]
    item_price = int(sys.argv[3])
    item_quantity = int(sys.argv[4])
    item_name, item_price, item_quantity = \
    input_check(mode, item_name, item_price, item_quantity)
    trade_items_check(mode)
    inputlog.extend(mode, item_name, item_price, item_quantity)
    account_balance += item_price * item_quantity
    index_sell += 1
    index += 1

# End of argv dependent code
mode = input_mode()
while mode in allowed_commands:
    if mode == "saldo":
        mode, account_value, account_comment = acc_input(mode)
        account_value, account_comment = \
        input_check(mode, 0, 0, 0, account_value, account_comment)
        account_balance += account_value
        oper_append(index_balance, index, mode)
        inputlog.extend([mode, account_value, account_comment])
        index_balance += 1
        index += 1
    if mode == "zakup":
        mode, item_name, item_price, item_quantity = acc_input(mode)
        item_name, item_price, item_quantity = \
        input_check(mode, item_name, item_price, item_quantity)
        trade_items_check(mode)
        account_balance -= item_price * item_quantity
        inputlog.extend([mode, item_name, item_price, item_quantity])
        oper_append(index_purch, index, mode)
        index_purch += 1
        index += 1
    if mode == "sprzedaż":
        mode, item_name, item_price, item_quantity = acc_input(mode)
        item_name, item_price, item_quantity = \
        input_check(mode, item_name, item_price, item_quantity)
        trade_items_check(mode)
        account_balance += item_price * item_quantity
        inputlog.extend([mode, item_name, item_price, item_quantity])
        oper_append(index_sell, index, mode)
        index_sell += 1
        index += 1
    if mode == "stop":
        print(f"Number of operations: {index}\n")
        index_first = int(input("Please type first operation to view:"))
        index_last = int(input("Please type last operation to view:"))
        index = 1
        print(f"\n\n\nAccount balance: {account_balance}\n")
        print("Items on stock:\n")
        for item_name, item_quantity in trade_items.items():
            print(f"{item_name}: {item_quantity} pcs")
        print("\nSummary:\n")
        for i in operations:
            if index >= index_first and index_first <= index_last:
                print(f"Operation nr {index}:\nmode: "
                      f"{operations_type[index - 1]}\n{i}\n\n")
            if index == index_last:
                break
            index += 1
        print("\nCorrect input log:")
        for i in inputlog:
            print(i)
        mode = "end"
        break
    mode = input_mode()

