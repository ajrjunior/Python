# Exemplo que cria um arquivo bla.zip,
# contendo um arquivo "numbers.txt" compactado
# com 10000 vezes a sequencia de caracteres "1234567890"

import zipfile
from datetime import datetime

myfile = open("TEST_BKP.zip", "wb")
zip = zipfile.ZipFile(myfile, mode="w")
info = zipfile.ZipInfo()
info.filename="BKP_b'105.112.11.115'-2018-06-01-12-47-58.txt"
info.compress_type = zipfile.ZIP_DEFLATED
#info.external_attr = (0644 << 16)
info.date_time = datetime.now().timetuple()
zip.writestr(info, "1234567890" * 10000)
zip.close()
myfile.close()
