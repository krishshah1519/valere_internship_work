def add(name):
    marks.update({name: {
        "Maths": int(input("Enter Maths Marks here: ")),
        "English": int(input("Enter English Marks here: ")),
        "Hindi": int(input("Enter Hindi Marks here: "))
        }})
    print("New Student Marks Created Succesfully")


def update(name):
    subject = int(input("Select Subject to Update Marks : \n 1).Maths \n "
                        "2).English \n 3).Hindi \n 4).All Subjects"))

    if choice == 1:
        subject = "Maths"
        marks[name][subject] == int(input("Enter Maths Marks to Update"))
        print("Marks of Maths Updated Successfully")
    if choice == 2:
        subject = "English"
        marks[name][subject] == int(input("Enter English Marks to Update"))
        print("Marks of English Updated Successfully")
    if choice == 3:
        subject = "Hindi"
        marks[name][subject] == int(input("Enter Hindi Marks to Update"))
        print("Marks of Hindi Updated Successfully")
    if choice == 4:
        subject = "Maths"
        marks[name][subject] == int(input("Enter Maths Marks to Update"))
        subject = "English"
        marks[name][subject] == int(input("Enter English Marks to Update"))
        subject = "Hindi"
        marks[name][subject] == int(input("Enter Hindi Marks to Update"))


def view():
    for student, subject in marks.items():
        print(f"{student}:")
    for subject, mark in subject.items():
        print(f" {subject} : {mark}")


def deleteAll():
    marks.clear()


def delete():
    name = input("Enter the Name of student whose record you want to delete")
    if name in marks:
        marks[name].pop()


marks = {
    "Student 1": {"Maths": 87, "English": 90, "Hindi": 98},
    "Student 2": {"Maths": 56, "English": 49, "Hindi": 68}
    }

while True:
    choice = int(input(
        "\nPlease select a operation \n"
        "1).Add new data \n"
        "2).Update data \n"
        "3).Delete all data \n"
        "4).Delete a particular entry \n"
        "5).view \n"
        "6).Exit"
        ))

    if choice == 1:
        name = input("Enter name: ")
        add(name)
    if choice == 2:
        name = input("enter name: ")
        if name in marks:
            update(name)
        else:
            print("Error!!! Please Enter a valid name/n")
    if choice == 3:
        deleteAll()
    if choice == 4:
        delete()
    if choice == 5:
        view()
    if choice == 6:
        print("Exiting Program")
        break
