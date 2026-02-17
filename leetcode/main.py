# numbers = [1,2,4,6,8,9,14,15]
numbers = [2, 1, 2, 1, 2]

def meow(numbers, sum):
    left = numbers[0]
    right = numbers[len(numbers)-1] 
    sum = sum
    found = False
    # some loop
    while found == False: 
        i=0
        j=1
        
        if left + right == sum: 
            message = f"{left} and {right} add up to {sum}"
        else:
            i+=1
            j+=1
            left = numbers[0+i]
            right = numbers[len(numbers)-j]
            break
        return message
    
def main():
    # 3. We need to print the result since meow() returns a string
    result = meow(numbers, 2)
    print(result)

# 4. The standard entry point
if __name__ == "__main__":
    main()
