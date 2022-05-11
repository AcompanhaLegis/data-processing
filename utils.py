import requests
import multiprocessing

session = None


def set_global_session():
    global session
    if not session:
        session = requests.Session()

def get_data(url):
    with session.get(url) as r:
        name = multiprocessing.current_process().name
        return r.json()

def get_info_deputados_recursive(url, info_arr=[]):
    data = get_data(url)
    if data.get('dados'):
        info_arr += data['dados']
        next_link = next((link['href'] for link in data['links'] if link['rel'] == 'next'), None)
        if next_link:
            return get_info_deputados_recursive(next_link, info_arr)
        return info_arr
    else:
        print('Error data: {}, [url={}]'.format(data, url))
        return info_arr
