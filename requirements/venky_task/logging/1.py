import logging
import datetime 
d=datetime.datetime.now()
logging.basicConfig(filename="logfile.txt",level=logging.INFO)
print(d,"It's Running Succesfully...")

logging.debug("This is DEBUG message...,"+str(d)+"... ")
logging.warning("This is WARNING message...")
logging.critical("This is CRITICAL message...")
logging.error("This is ERROR message...")

logging.info("This is INFO message...")

try:
  a=int(input("enter a first number: "))
  b=int(input("enter a second  number: "))
  c=a/b
  print(c)
except ZeroDivisionError as msg:
  print("the error ouccured...")
  logging.exception(msg)

