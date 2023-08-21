from bs4 import BeautifulSoup
import csv

with open("CSGO-rep.com.htm", encoding="utf8") as fp:
    s = BeautifulSoup(fp, 'html.parser')
    ids = s.findAll('a', attrs={'class': 'nickname'})
    steamid = [str(i)[str(i).find("profile") + len("profile/"):str(i).find('">')] for i in ids]

    name = [str(i)[str(i).find('">') + len('">'):-4] for i in ids]

    content = s.findAll('div', attrs={'class': 'content'})
    transaction_type = [str(i)[str(i).find("Transaction:") + len("Transaction:</strong>"):str(i).find('<span class=') - 10].strip() for i in content]
    amount = [str(i)[str(i).find('">$') + len('">$'):str(i).find('</span>')].replace(" ", "") for i in content]
    amount = [i if len(i) < 10 else "NONE" for i in amount]
    method = s.findAll('span', attrs={'class': 'price-green'})
    new_method = []
    for i in method:
        if "$" not in str(i):
            new_method.append(str(i)[str(i).find('n">') + len('n">'):str(i).find('</span>')])
    method = new_method

    message = [str(i)[str(i).find('<p>') + len('<p>'):str(i).find('</p>')].replace("\n", "") for i in content]

data = list(zip(name, steamid, transaction_type, amount, method, message))

with open('data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    field = ["name", "steamid", "transaction type", "amount", "method", "message"]

    writer.writerow(field)

    for i in data:
        writer.writerow([i[0], i[1], i[2], i[3], i[4], i[5]])