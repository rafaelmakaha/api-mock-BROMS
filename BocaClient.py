import requests
from zipfile import ZipFile


def update_files():
    url = 'http://192.81.209.191/boca/admin/report/webcast.php?webcastcode=broms'
    request = requests.get(url)
    if request and request.status_code == 200:
        open('./data/webcast.zip', 'wb').write(request.content)
        zip = ZipFile('./data/webcast.zip', 'r')
        zip.extract('./contest', './data/')
        zip.extract('./runs', './data/')
        zip.close()
    elif request:
        print(request.status_code)
    else:
        print('Response Failed')

