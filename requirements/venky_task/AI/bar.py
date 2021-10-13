import matplotlib.pyplot
import pandas as pd
venky1={"venky":["1","2","3"],
        "venkat":["he"," is Artficial"," Intelgence"]}
df=pd.DataFrame(venky1)
print(df)
cols=df.shape
print(cols)
print(df.columns)
print(df.venky)
