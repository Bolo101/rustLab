count = {}
with open("./sandbox/file.txt", "w+") as f:
    for i in range(22):
        f.write(f"line added {i}\n")
    f.seek(0)
    for line in f :
        for word in line.split():
            count[word] = count.get(word,0) + 1
    sorted_count = sorted(count.items(),key = lambda value:value[1], reverse=True)
    print('\n'.join(f"Key: {k}, Value: {v}" for k, v in sorted_count))