intNum = int(input("Enter the number to Check if It is Prime: "))
is_prime = True
for i in range(2,int(intNum**0.5) +1):
    if intNum % i == 0 or intNum <= 0:
        is_prime = False
        break

if is_prime == True:
    print("The Number is a Prime Number")
if is_prime == False:
    print("The Number is not a Prime Number")