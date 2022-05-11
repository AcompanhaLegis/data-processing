import json
import multiprocessing
import os
import requests

from utils import get_data, get_info_deputados_recursive, set_global_session

FOLDER = 'deputados_data'


def get_deputados():
    url = 'https://dadosabertos.camara.leg.br/api/v2/deputados?ordem=ASC&ordenarPor=nome&itens=1000'
    res = requests.get(url)
    deputados = res.json()['dados']
    with open('{}/deputados.json'.format(FOLDER), 'w+') as f:
        json.dump(deputados, f, indent=4, ensure_ascii=False)
        f.close()
    return deputados

def get_proposicoes_deputado(deputado, update=False):
    print('Requesting data for {}'.format(deputado['nome']))
    file_name = '{}/dep_{}.json'.format(FOLDER, deputado['id'])
    if not os.path.isfile(file_name) or update:
        url = 'https://dadosabertos.camara.leg.br/api/v2/proposicoes?ordem=ASC&ordenarPor=id&idDeputadoAutor={}&itens=100'.format(deputado['id'])
        deputado['proposicoes'] = get_info_deputados_recursive(url, [])
        print(deputado['nome'], len(deputado['proposicoes']))
        with open(file_name, 'w+') as f:
            print('Writing data for deputado'.format(deputado['nome']))
            json.dump(deputado, f, indent=4, ensure_ascii=False)
            f.close()
    else:
        print('Already have data for {}'.format(deputado['nome']))

def main():
    if not os.path.isfile('{}/deputados.json'.format(FOLDER)):
        deputados = get_deputados()
    else:
        with open('{}/deputados.json'.format(FOLDER), 'r') as f:
            deputados = json.load(f)
    with multiprocessing.Pool(initializer=set_global_session, processes=8) as pool:
        pool.map(get_proposicoes_deputado, deputados)

if __name__ == '__main__':
    main()
