a=input("enter a string :")
b=input("enter a string :")
def anagram(a,b):
  if sorted(a.lower())== sorted(b.lower()):
    print(a," and ",b," anagrams")
  else:
    print("not anagrams:")

anagram(a,b)
