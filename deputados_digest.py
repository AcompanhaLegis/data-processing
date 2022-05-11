import json
import multiprocessing
import os
import requests

SRC_FOLDER = 'deputados_data'
EXPENSES_FOLDER = 'deputados_expenses_data'
OUT_FOLDER = 'deputados_data_digest'

def proposicoes_by_year(deputado_id, data_dict = dict()):
    if not os.path.isfile('{}/dep_{}.json'.format(SRC_FOLDER, deputado_id)):
        print('File not found: {}/dep_{}.json'.format(SRC_FOLDER, deputado_id))
    with open('{}/dep_{}.json'.format(SRC_FOLDER, deputado_id), 'r') as f:
        deputado = json.load(f)
        data_dict['proposicoes_by_year'] = {}
        for proposicao in deputado['proposicoes']:
            types = data_dict['proposicoes_by_year'].get(proposicao['ano'], {}).get('types', {})
            types[proposicao['siglaTipo']] = types.get(proposicao['siglaTipo'], 0) + 1
            data_dict['proposicoes_by_year'][proposicao['ano']] = {
                'amount': data_dict['proposicoes_by_year'].get(proposicao['ano'], {}).get('amount', 0) + 1,
                'types': types
            }
            with open('{}/dep_{}.json'.format(OUT_FOLDER, deputado_id), 'w+') as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)


def expenses_by_year_month(deputado_id, data_dict = dict()):
    if not os.path.isfile('{}/dep_{}.json'.format(EXPENSES_FOLDER, deputado_id)):
        print('File not found: {}/dep_{}.json'.format(EXPENSES_FOLDER, deputado_id))
        return
    with open('{}/dep_{}.json'.format(EXPENSES_FOLDER, deputado_id), 'r') as f:
        deputado_expenses = json.load(f)
        data_dict['expenses_by_year_month'] = {}
        for expense in deputado_expenses:
            year = expense['ano']
            month = expense['mes']
            amount = data_dict['expenses_by_year_month'].get(year, {}).get(month, 0) + expense['valorLiquido']
            data_dict['expenses_by_year_month'][year] = data_dict['expenses_by_year_month'].get(year, {})
            data_dict['expenses_by_year_month'][year][month] = round(data_dict['expenses_by_year_month'][year].get(month, 0) + expense['valorLiquido'], 2)
            with open('{}/dep_{}_expenses.json'.format(OUT_FOLDER, deputado_id), 'w+') as f:
                json.dump(data_dict, f, indent=4, ensure_ascii=False)
            


def main():
    if not os.path.isfile('{}/deputados.json'.format(SRC_FOLDER)):
        raise Exception('File not found: {}/deputados.json'.format(SRC_FOLDER))
    with open('{}/deputados.json'.format(SRC_FOLDER), 'r') as f:
        deputados = json.load(f)
    ids = [deputado['id'] for deputado in deputados]
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(proposicoes_by_year, ids)
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(expenses_by_year_month, ids)

if __name__ == '__main__':
    main()
