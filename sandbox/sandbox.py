nums = [f for f in range(1,21)]
mult3 = [n for n in nums if n%3 ==0]
print(mult3)
squares = {n : n*n for n in mult3}
print(squares)
odds = {n for n in nums if n%2 ==1}
print(odds)