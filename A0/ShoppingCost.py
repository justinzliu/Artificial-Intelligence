"""
To run this script:
	python shoppingCost.py

If you run the above script, a correct calculateShoppingCost function should return:

The final cost for our shopping cart is 35.58
"""

import csv

def calculateShoppingCost(productPrices, shoppingCart):
	finalCost = 0
	for x in shoppingCart:
            quantity = int(shoppingCart[x])
            finalCost = finalCost + float(productPrices[x])*quantity
	return finalCost


def createPricesDict(filename):
	productPrice = {}
	with open(filename,mode='r') as file:
            reader = csv.reader(file)
            productPrice = {rows[0]:rows[1] for rows in reader}
	return productPrice


if __name__ == '__main__':
	prices = createPricesDict("Grocery.csv")
	myCart = {"Bacon": 2,
		      "Homogenized milk": 1,
		      "Eggs": 5}
	print("The final cost for our shopping cart is {}".format(calculateShoppingCost(prices, myCart)))
