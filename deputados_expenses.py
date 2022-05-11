import json
import os
import multiprocessing

from utils import get_data, get_info_deputados_recursive, set_global_session

SRC_FOLDER = 'deputados_data'
FOLDER = 'deputados_expenses_data'

def get_expenses_deputado(deputado, update=False):
    print('Requesting data for {}'.format(deputado['nome']))
    file_name = '{}/dep_{}.json'.format(FOLDER, deputado['id'])
    if not os.path.isfile(file_name) or update:
        url = 'https://dadosabertos.camara.leg.br/api/v2/deputados/{}/despesas?ordem=ASC&ordenarPor=ano&itens=100'.format(deputado['id'])
        expenses = get_info_deputados_recursive(url, [])
        print(deputado['nome'], len(expenses))
        with open(file_name, 'w+') as f:
            print('Writing data for deputado'.format(deputado['nome']))
            json.dump(expenses, f, indent=4, ensure_ascii=False)
            f.close()
    else:
        print('Already have data for {}'.format(deputado['nome']))


def main():
    if not os.path.isfile('{}/deputados.json'.format(SRC_FOLDER)):
        raise Exception('File not found: {}/deputados.json'.format(SRC_FOLDER))
    with open('{}/deputados.json'.format(SRC_FOLDER), 'r') as f:
        deputados = json.load(f)
    with multiprocessing.Pool(initializer=set_global_session, processes=8) as pool:
        pool.map(get_expenses_deputado, deputados)

if __name__ == '__main__':
    main()

