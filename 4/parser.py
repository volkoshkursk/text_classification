import lxml.html
import lxml
import lxml.etree
import requests
import numpy as np
import sqlite3


def get(link):
    response_inner = requests.get(link)
    if response_inner.status_code == 200:
        tree_inner = lxml.html.fromstring(response_inner.text)
        len_of_table = len(tree.xpath('//table[@style="width:100%;border-color:#000000"]/'
                                      '/nobr[contains(text(), "УИК")]//text()'))
        table = np.array(tree_inner.xpath('//table[@style="width:100%;border-color:#000000"]//td[@width="90%"]//tr/'
                                          '/nobr//text()'))
        table.reshape((15, len_of_table))
        return np.concatenate((np.array([tree.xpath('//td[contains(text(), "Территориальная '
                                                    'избирательная комиссия")]/text()')
                                         for _ in range(len_of_table)]), table), axis=1)
    else:
        raise RuntimeError('status code is ' + str(response_inner.status_code) + ' in link ' + link)


def save(table):
    sqlite3.connect('collection.db')



if __name__ == '__main__':
    response = requests.get('http://www.st-petersburg.vybory.izbirkom.ru/region/region/st-petersburg?action=show&root=1'
                            '&tvd=27820001217417&vrn=27820001217413&region=78&global=null&sub_region=78&prver=0&'
                            'pronetvd=null&vibid=27820001217417&type=222')
    if response.status_code == 200:
        tree = lxml.html.fromstring(response.text)
        objects = tree.xpath('//tr[@bgcolor="#FFFFFF"]//a/@href')
        for object_ in objects:
            get(object_)
    else:
        raise RuntimeError('status code is ' + str(response.status_code))
