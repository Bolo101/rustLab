people = {}
with open("./sandbox/file.txt") as f:
    for line in f:
        name,age = line.rstrip().split(",")
        people[name] = int(age)
    
for name in sorted(people.items(), key= lambda age: age[1], reverse=True):
    print(f"{name[0]} is {age}")