"""
To run this script:
	python EvenOdd.py

In order to pass the autograder your function should
return a list of even numbers given any list of integers.
If you run the above script, a correct function should return:

Even numbers are [2, 4]

FEEDBACK
- 1.5 hours spent (mostly on researching numpy and python functions/formatting)
- algorithms in class are the most difficult part in class to understand
- I'm looking forward to everything!

"""

def getEvenNumbers(numbers):
	evens = []
	for x in numbers:
        	if x%2 == 0:
            		evens.append(x)
	return evens


if __name__ == '__main__':
	myList = [1, 2, 3, 4, 5]
	print("Even numbers are {}".format(getEvenNumbers(myList)))