import bs4 as bs
import pandas as pd
import requests
import json

def extract_data(url='https://infogram.com/covid-2019-ins-colombia-1hnq41zg9ord63z'):
    
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    assert response.status_code == 200
    
    soup = bs.BeautifulSoup(response.content, 'html.parser')
    
    json_tree = soup.find_all('script')[7].text[23:]
    json_tree = json_tree[:-1]
    
    dict_tree = json.loads(json_tree)

    relevant_key = list(dict_tree['elements']['content']['content']['entities'].keys())[6]
    data = dict_tree['elements']['content']['content']['entities'][relevant_key]['props']['chartData']['data']
    
    a = []
    for idx, row_i in enumerate(data[0]):
        a.append(pd.DataFrame([idx] + row_i))
        
    data_df = (pd.concat(a, axis=1, ignore_index=True)
             .melt(id_vars=0)
             .rename(columns={0:'index_col'})
             .pivot_table(values='value',index='variable',columns='index_col', aggfunc=lambda x: x[0])
             .reset_index()
             .loc[:, ['ID de caso', 'Ciudad de ubicación', 'Fecha de diagnóstico ','Femenino',
                      'Asociado', 'Atención', 'Importado', 'Masculino', 
                      '0 a 9', '10 a 19', '20 a 29', '30 a 39', 
                      '40 a 49', '50 a 59', '60 a 69', '70 a 79',
                      '80 a 89','90 o más'
             ]]
            )
    
    return data_df

casos_df = extract_data()
casos_df.to_csv('casos_col.csv', index=False)