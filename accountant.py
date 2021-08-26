import sys
account_values = []
account_comments = []
account_balance = 0
trade_items = dict()
operations_type = []
operations = []
inputlog = []
mode = sys.argv[1]
inputlog.append(mode)
index = 0
index_saldo = 0
index_zakup = 0
index_sprzedaz = 0

allowed_commands = "saldo", "sprzedaż", "zakup", "stop", "end"
if mode == "saldo":
    account_values.append(int(sys.argv[2]))
    account_comments.append(sys.argv[3])
    inputlog.append(int(sys.argv[2]))
    inputlog.append(sys.argv[3])
    operations_type.append(mode)
    operations.append(f"Operation in mode 'saldo' number {str(index_saldo + 1)}:"
                      f" {str(account_values[index_saldo])} - "
                      f"description: {account_comments[index]}")
    print(f"Operation in mode 'saldo' number {str(index_saldo + 1)}:"
          f" {str(account_values[index_saldo])} - "
          f"description: {account_comments[index]}")
    account_balance += account_values[index]
    index_saldo += 1
    index += 1
if mode == "zakup":
    inputlog.append(mode)
    item_name = sys.argv[2]
    while item_name not in trade_items:
        item_name = input("ERROR: Please type correct item name")
    item_price = int(sys.argv[3])
    item_quantity = int(sys.argv[4])
    if item_price <= 0 or item_quantity <= 0 or account_balance < item_price*item_quantity:
        while item_price <= 0 or item_quantity <= 0:
            item_price = int(input("Please type item price"))
            item_quantity = int(input("Please type item quantity"))
    account_balance -= item_price * item_quantity
    trade_items[item_name] = item_quantity
    inputlog.append(item_name)
    inputlog.append(item_price)
    inputlog.append(item_quantity)
if mode == "sprzedaż":
    inputlog.append(mode)
    item_name = sys.argv[2]
    while item_name not in trade_items:
        item_name = input("ERROR: Please type correct item name")
    item_price = int(sys.argv[3])
    item_quantity = int(sys.argv[4])
    if item_price <= 0 or item_quantity <= 0 or account_balance < item_price*item_quantity:
        while item_price <= 0 or item_quantity <= 0 or trade_items[item_name] < item_quantity:
            item_name = input("Please type item name")
            item_price = int(input("Please type item price"))
            item_quantity = int(input("Please type item quantity"))
    account_balance -= item_price * item_quantity
    trade_items[item_name] = item_quantity
    inputlog.append(item_name)
    inputlog.append(item_price)
    inputlog.append(item_quantity)
mode = input("Please type mode:")

# End of argv dependent code

while mode not in allowed_commands:
    mode = input("Please type correct mode:")
while mode in allowed_commands:
    if mode == "saldo":
        inputlog.append(mode)
        account_values.append(int(input("Please type operation value (in gr)")))
        account_comments.append(input("Please type operation description"))
        inputlog.append(account_values[-1])
        inputlog.append(account_comments[-1])
        print(f"Operation in mode 'saldo' number {str(index_saldo + 1)}:"
              f" {str(account_values[index_saldo])} - "
              f"description: {account_comments[index]}")
        account_balance += account_values[index]
        operations_type.append(mode)
        operations.append(f"Value: {account_values[index]} - "
                          f"Comment: {account_comments[index]}")
        index_saldo += 1
        index += 1
        mode = input("Please type mode:")
        while mode not in allowed_commands:
            mode = input("Please type correct mode:")
    if mode == "zakup":
        inputlog.append(mode)
        item_name = input("Please type item name")
        item_price = int(input("Please type item price"))
        item_quantity = int(input("Please type item quantity"))
        if item_price <= 0 or item_quantity <= 0 or account_balance < item_price*item_quantity:
            while item_price <= 0 or item_quantity <= 0 or account_balance < item_price*item_quantity:
                item_name = input("ERROR: Please type item name")
                item_price = int(input("Please type item price"))
                item_quantity = int(input("Please type item quantity"))
        account_balance -= item_price * item_quantity
        trade_items[item_name] = item_quantity
        inputlog.append(item_name)
        inputlog.append(item_price)
        inputlog.append(item_quantity)
        operations_type.append(mode)
        operations.append(f"Operation in mode 'zakup' number {str(index_zakup + 1)}:"
                          f"Item:{item_name} purchased {item_quantity} pcs for price {item_price}gr")
        index += 1
        index_zakup += 1
        mode = input("Please type mode:")
        while mode not in allowed_commands:
            mode = input("Please type correct mode:")
    if mode == "sprzedaż":
        inputlog.append(mode)
        item_name = input("Please type item name")
        while item_name not in trade_items:
            item_name = input("ERROR: Please type correct item name")
        item_price = int(input("Please type item price"))
        item_quantity = int(input("Please type item quantity"))
        if item_price <= 0 or item_quantity <= 0:
            while item_price <= 0 or item_quantity <= 0 or trade_items[item_name] < item_quantity:
                item_price = int(input("ERROR: Please type item price"))
                item_quantity = int(input("Please type item quantity"))
        account_balance += item_price * item_quantity
        trade_items[item_name] -= item_quantity
        inputlog.append(item_name)
        inputlog.append(item_price)
        inputlog.append(item_quantity)
        operations_type.append(mode)
        operations.append(f"Operation in mode 'sprzedaż' number {str(index_sprzedaz + 1)}:"
                          f"Item:{item_name} sold {item_quantity} pcs for price {item_price}gr")
        index += 1
        index_sprzedaz += 1
        mode = input("Please type mode:")
        while mode not in allowed_commands:
            mode = input("Please type correct mode:")
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
                print(f"Operation nr {index}:\nmode: {operations_type[index - 1]}\n{i}\n\n")
            if index == index_last:
                break
            index += 1
        print("\nCorrect input log:")
        for i in inputlog:
            print(i)
        mode = "end"
        break

