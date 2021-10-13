def file(fname):
  import os
  statinfo=os.stat(fname)
  return statinfo.st_size
print("The file size is: ",file("E:\\chennai1\\file handling\\venky.pdf"))
