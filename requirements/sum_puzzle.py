'''
given a list of numbers and a number k, return whether any two numbers from the list add upto k.

'''
k = int(input("enter number :"))
l = [10, 15, 3, 7]
for i in range (len(l)):
	for j in range (len(l)):
		if l[i] == l[j]:
			continue
		elif l[i] + l[j] == k:
			print(l[i],'+',l[j],'=',k)
