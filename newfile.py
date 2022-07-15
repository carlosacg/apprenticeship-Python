# currencies = {'Euro':'€', 'Dollar':'$', 'Yen':'¥'}

# option = input("Inserte una divisa: ")

# if option not in currencies:
#     print("No se encuentra esta divisa")
# else:
#     print(currencies[option])


# name = input("Write your name: ")
# age = int(input("Write your age: "))
# phone_number = input("Write your phone number: ")

# user_data = {}
# user_data['name'] = name
# user_data['age'] = age
# user_data['phone_number'] = phone_number

# result = f'{user_data["name"]} tiene {user_data["age"]} años y su número de teléfono es {user_data["phone_number"]}.'
# print(result)


number = "10441204"
max_number = 0
for i, _ in enumerate(number):
    if i > 0:
        new_number = int(number[:i-1]+number[i:])
        if new_number > max_number:
            max_number = new_number

print(max_number)
print(id(number))