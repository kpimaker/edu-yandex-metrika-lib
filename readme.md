# Учебный пример библиотеки для отчетности на основе Яндекс Метрики

## Быстрый старт
В своем аккаунте @yandex.ru создайте приложение и предоставьте ему права на чтение данных статистики нужных вам счетчиков. Используйте [раздел "Отладочный токен"](https://yandex.ru/dev/metrika/doc/api2/intro/authorization-docpage/). Укажите полученный токен в файле config.yaml в строчке token:
```
metrika:
  token: Ag...
  owner: username (optional)
```

Получение отчета (в текущей версии есть отчет по соцсетям social_networks и технический мониторинг tech_monitoring, 44147844 - тестовый счетчик Я.Метрики):
```python
from yandex_metrika_lib import MetrikaReports

mr = MetrikaReports()
mr.social_networks('2019-08-20', '2019-08-31', '44147844')
```

Результат:
```
{  
   'data':[  
      {  
         'dimensions':[  
            {  
               'favicon':'facebook.com',
               'id':'facebook',
               'name':'Facebook'
            }
         ],
         'metrics':[  
            27.0,
            28.0,
            45.0
         ]
      },
      {  
         'dimensions':[  
            {  
               'favicon':'vk.com',
               'id':'vkontakte',
               'name':'VKontakte'
            }
         ],
         'metrics':[  
            1.0,
            1.0,
            3.0
         ]
      }
   ],
   'data_lag':69,
   'max':[  
      27.0,
      28.0,
      45.0
   ],
   'min':[  
      1.0,
      1.0,
      3.0
   ],
   'query':{  
      'adfox_event_id':'0',
      'attribution':'Last',
      'auto_group_size':'1',
      'currency':'RUB',
      'date1':'2019-08-20',
      'date2':'2019-08-31',
      'dimensions':[  
         'ym:s:lastSocialNetwork'
      ],
      'group':'Week',
      'ids':[  
         44147844
      ],
      'limit':100,
      'metrics':[  
         'ym:s:users',
         'ym:s:visits',
         'ym:s:pageviews'
      ],
      'offline_window':'21',
      'offset':1,
      'quantile':'50',
      'sort':[  
         '-ym:s:users'
      ]
   },
   'sample_share':1.0,
   'sample_size':9290,
   'sample_space':9290,
   'sampled':False,
   'total_rows':2,
   'total_rows_rounded':False,
   'totals':[  
      28.0,
      29.0,
      48.0
   ]
}
```