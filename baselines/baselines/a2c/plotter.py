import matplotlib.pyplot as plt
import csv

value_loss=[]
with open('progress.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    
    for row in reader:
        print row[0] 
        print type(row[0])
        try:
            value_loss.append(float(row[0]))
        except ValueError:
            pass
plt.plot(value_loss)
plt.ylabel('some numbers')
plt.show()
