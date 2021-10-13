import emp,pickle

with open("venkypick.txt","rb") as f:
  

  while True:
    try:
      obj=pickle.load(f)
      if obj.eno==2:
        obj.display()
    except:
      print("that's over")
      break
