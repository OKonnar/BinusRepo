# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 17:38:46 2024

@author: Loic_
"""

GroceryList = []


while(1):
    print('Choose an option')
    print('1. Add an item')
    print('2. View the list')
    print('3. Remove an item')
    print('4. Exit')
    ipt = int(input('Enter your choice: '))
    
    match ipt:
        case 1:
            Item = input('Enter the item to add:')
            GroceryList.append(Item)
            print('Item \'' + Item + '\' added to the grocery list.')
        case 2:
            print(GroceryList)
        case 3:
            ItemName = input('Enter the item to delete:')
            GroceryList.remove(ItemName)
        case 4:
            print('Bye')
            break
        case _:
            print('Invalid option !')
        
    
    
    
