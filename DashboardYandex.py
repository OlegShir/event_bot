'''Класс будет расширяться по мере необходимости'''
import requests

def get_json(url, api_cabinet):
    headers = {'X-Auth-Key': api_cabinet}
    r = requests.get(url, headers = headers)
    
    return r.json()

class DashboardYandex:
    def __init__(self, api_cabinet='5c1a9786-84a9-4f2e-80d1-d66945f9bc2e'):
        self.api_cabinet = api_cabinet
        self.host_cabinet = 'https://api-developer.tech.yandex.net'
    
    def get_projects_param(self):
        '''Запрос позволяет получить названия и идентификаторы всех проектов, 
           которые создал пользователь Кабинета разработчика'''

        get_url = self.host_cabinet + '/projects'
        projects_param = get_json(get_url, self.api_cabinet)

        return projects_param

    def get_services(self, project = 0):
        '''Запрос позволяет получить названия и идентификаторы всех сервисов,
           которые подключены к проекту пользователя'''

        projects_param = self.get_projects_param()
        project_id = projects_param['projects'][project]['id']

        get_url = self.host_cabinet + f'/projects/{project_id}/services'
        services_param = get_json(get_url, self.api_cabinet)

        return services_param

    def get_limit_apimaps(self, project_id = '4f3f4985-5169-4ce6-bb83-dc8fbcc5a205', service_id = 'apimaps', geocoder = True):
        '''Запрос позволяет получить информацию о запросах к API сервисов Яндекса. 
           Тело ответа содержит данные количестве запросов, которые пользователь отправил за сутки'''

        get_url = self.host_cabinet + f'/projects/{project_id}/services/{service_id}/limits'
        limits_json = get_json(get_url, self.api_cabinet)

        limits = limits_json['limits']
        
        if geocoder: value_limit = limits['apimaps_http_geocoder_daily']['value']
        else: value_limit = limits['apimaps_total_daily']['value']

        return value_limit

# ТЕСТ
'''
dev = DashboardYandex()
print(dev.get_limit_apimaps())
'''
