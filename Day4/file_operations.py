
with open("example.txt", "w") as file:
    file.write("Hello, world!\nThis is a text file.")

with open("example.txt", "a") as file:
    file.write("\nAdding More Content")

with open("example.txt", "r") as file:
    content = file.read()
    print(content)

with open("data.csv", "w", newline="") as file:
    inv = input("enter input here: ")
    writer = csv.writer(file)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Krish", 21])
    writer.writerow(["san", 22])

with open("data.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["Name"], row["Age"])

data = {
    "name": "Krish",
    "age": 21,
    "skills": ["table tennis", "swimming"]
}

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

with open("data.json", "r") as file:
    data = json.load(file)
    print(data)
