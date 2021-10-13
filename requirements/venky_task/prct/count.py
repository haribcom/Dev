def list_count_4(nums):
  count = 0  
  for num in nums:
    if num == 4:
      count = count + 1

      return count

s=input("enter: ")
print(list_count_4(s))
"""print(list_count_4([1, 4, 6, 4, 7, 4]))"""
