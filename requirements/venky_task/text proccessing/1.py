text="""
VENKY: My name is venkyy i am doing python developer
VENKAT: python developer
TAJU: he is bank employee
MOHAN: he also python
REDDY: He Automation engineer"""

def main():
  lines=text.splitlines()
  for i in lines:
    if i.find("python") != -1:
      print(i)
main()





