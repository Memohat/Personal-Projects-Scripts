#! python3
import csv
with open('email.csv') as fin:
	reader = csv.reader(fin, delimiter=':')
	with open('emails.csv', 'a') as fout:
		writer = csv.writer(fout)
		data_lst = []
		for name, data in reader:
			data_lst.append(data.strip())
		writer.writerow(data_lst)
