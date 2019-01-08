import requests
import os
import csv


def getCBSData():
    # url = r'http://cbs.wondershare.cn/index.php?module=products&submod=product_use_stat&method=track_product_stat&format=&default_chart=1&node_id=184&product_type_id=215&product_relation_id=&product_name=0&product_num=&product_manager_id=0&language_id=&brand_id=&status=1&run_platform=&combine=1&is_recursion=0&base_date=2018-01-02%20-%202019-01-08&op_type=export_csv'
    url = r'http://cbs.wondershare.cn/index.php?module=products&submod=product_use_stat&method=track_product_stat'
    headers = {
        # 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=165acb467e62d6-056e778e94157e-34677908-1aeaa0-165acb467e79d4; PHPSESSID=goeulrlqeig8aloi0oedjb1no0; _pk_ses.3.799a=*; list_track_product_stat=download_times%2Cinstall_times%2Cqty%2Camount%2Cnet_amount; _pk_id.3.799a=314ca046eb5732f3.1546911393.1.1546913416.1546911393.; ws_id=16082531; password=1af7abeb17be1378d2c753cdc84dfbef',
        'DNT': '1',
        'Referer': 'http://cbs.wondershare.cn/index.php?method=login',
        'Host': 'wps.wondershare.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # r = requests.get(url, headers=headers, allow_redirects=True)
    r = requests.get(url, headers=headers, allow_redirects=True)
    print(r.text)

    pass

def getODSData():
    url = r'http://ods.wondershare.cn/admin/index/index.html'
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=165acb467e62d6-056e778e94157e-34677908-1aeaa0-165acb467e79d4; PHPSESSID=uc432c9uqr5d4b8jsuiqjnp6c4; _pk_ses.1.2a23=*; _pk_id.1.2a23=c21dbaeee4efd5cf.1546911432.2.1546914793.1546914398.',
        'DNT': '1',
        'Host': 'ods.wondershare.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # r = requests.get(url, headers=headers, allow_redirects=True)
    r = requests.get(url, headers=headers, allow_redirects=True)
    print(r.text)
    print('\n')
    print(r.headers)


    pass

if __name__ == '__main__':
    getODSData()