import os
import requests
import time

def getDataSize(url):
   r = requests.head(url)
   # headers = r.headers
   headers = r.headers

   print(headers)
   print('\n')
   print("MT",headers['Last-Modified'])
   print("FS",headers['Content-Length'])

def getFileSize(path):
   mt = os.path.getmtime(path)
   fs = os.path.getsize(path)
   print("MT", mt)
   print("FS", fs)
   # ttt =time.strftime("%a %b %d %H:%M:%S %Y", float(mt))
   # print(ttt)

if __name__ == '__main__':
   # url = 'http://download.wondershare.com/filmorapro_full4622.msi'
   # url = 'http://download.wondershare.com/filmorapro_full4623.pkg'
   url = 'http://cbs.wondershare.com/go.php?track=download_start&name=filmorapro_full4623&pid=4623&back_url=http%3A%2F%2Fdownload.wondershare.com%2Fcbs_down%2Ffilmorapro_full4623.pkg'

   # path = "D:\Filmora Pro\OEM\Build\FilmoraPro_1.0.0131.pkg"
   path = r"C:\Users\ws\Downloads\FilmoraPro_1.0.0131.pkg"


   # url = r'http://www.sherwinleehao.com/vpn.zip'
   # path = r'C:\Users\ws\Downloads\vpn (1).zip'

   getDataSize(url)
   getFileSize(path)


# 287665278 HK
# 287665278 JP

