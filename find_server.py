import socket

print("=" * 50)

computer_name = socket.gethostname()

print("Computer Name:")
print(computer_name)

print("\nSQL Server Name:")
print(f"{computer_name}\\SQLEXPRESS")

print("\nLocal IP Address:")
print(socket.gethostbyname(computer_name))

print("=" * 50)