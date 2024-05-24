import csv

with open('test_file.csv','w',newline='') as file:
	writer = csv.writer(file)
	writer.writerow(['name','age'])
	writer.writerow(['John Doe',30])
