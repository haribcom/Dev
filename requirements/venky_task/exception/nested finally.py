try:
    print("in try1")
    try:
        print("try 2")
    except:
        print("in except1")
    finally:
        print("in finally1")

except:
    print("in except2")
    try:
        print("in try 3")
    except:
        print("in except3")
    finally:
        print("in finally2")

finally:
    print("in finally3")
    try:
        print("in try4")
    except:
        print("in except")
    finally:
        print("in finally4")




        
