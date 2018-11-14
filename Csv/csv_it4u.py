import CSV
With open(‘some.csv’, ‘rb’) as f:
reader = csv.reader(f)
for row in reader:
print row
