import pandas

d= pandas.read_csv("test.csv")

a = d.loc[1, :].values.tolist()
print(a)
