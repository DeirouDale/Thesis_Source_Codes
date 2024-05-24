import pandas as pd
data = {
	'name': ['isa','dale'],
	'age': [22,22]
}
df = pd.DataFrame(data)
df.to_csv('file.csv',index=False)
