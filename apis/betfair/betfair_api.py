import requests
import json


class BetfairAPI():

    LOGIN_API = 'https://identitysso.betfair.com.au/api/login'
    MARKET_DATA_API = 'https://ero.betfair.com.au/www/sports/exchange/readonly/v1/bymarket'
    EXCHANGE_API = 'https://scan-inbf.betfair.com.au/www/sports/navigation/facet/v1/search?_ak=nzIFcwyWhrlwYMrh&alt=json'

    DEFAULT_FILTER = {
        "marketBettingTypes": [
            "ASIAN_HANDICAP_SINGLE_LINE",
            "ASIAN_HANDICAP_DOUBLE_LINE",
            "ODDS",
            "LINE"
        ],
        "productTypes": [
            "EXCHANGE"
        ],
        "contentGroup": {
            "language": "en",
            "regionCode": "NZAUS"
        },
        "selectBy": "RANK",
        "maxResults": 0
    }
    

    @staticmethod
    def create_market_filter(
        text_query: str = None,
        event_type_ids: list = None,
        event_ids: list = None,
        competition_ids: list = None,
        market_ids: list = None,
        venues: list = None,
        bsp_only: bool = None,
        turn_in_play_enabled: bool = None,
        in_play_only: bool = None,
        market_betting_types: list = None,
        market_countries: list = None,
        market_type_codes: list = None,
        market_start_time: dict = None,
        with_orders: str = None,
        race_types: list = None,
    ) -> dict:
        '''
        Creates a market filter dictionary which is used for customising queries to the Betfair API.
        This function is modified from the betfairlightweight library.

        :param str text_query: restrict markets by text associated with it, e.g name, event, comp.
        :param list event_type_ids: filter market data to data pertaining to specific event_type ids.
        :param list event_ids: filter market data to data pertaining to specific event ids.
        :param list competition_ids: filter market data to data pertaining to specific competition ids.
        :param list market_ids: filter market data to data pertaining to specific marketIds.
        :param list venues: restrict markets by venue (only horse racing has venue at the moment)
        :param bool bsp_only: restriction on bsp, not supplied will return all.
        :param bool turn_in_play_enabled: restriction on whether market will turn in play or not, not supplied returns all.
        :param bool in_play_only: restriction to currently inplay, not supplied returns all.
        :param list market_betting_types: filter market data by market betting types.
        :param list market_countries: filter market data by country codes.
        :param list market_type_codes: filter market data to match the type of market e.g. MATCH_ODDS.
        :param dict market_start_time: filter market data by time at which it starts.
        :param str with_orders: filter market data by specified order status.
        :param list race_types: filter race types.

        :return: dict
        '''
        args = locals().copy()

        def to_camel_case(snake_str: str) -> str:
            components = snake_str.split("_")
            return components[0] + "".join(x.title() for x in components[1:])
        
        market_filter = BetfairAPI.DEFAULT_FILTER.copy()
        add_fields = {to_camel_case(k): v for k, v in args.items() if v is not None}
        market_filter.update(add_fields)
        return market_filter


    def __init__(self):
        self.session = requests.session()


    def login(self, username: str, password: str) -> bool:
        payload = {
            'product': 'exchange-eds',
            'redirectMethod': 'GET',
            'url': 'https://www.betfair.com.au/exchange/plus?loginStatus=SUCCESS',
            'submitForm': 'true',
            'username': username,
            'password': password
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        self.session.request("POST", self.LOGIN_API, headers=headers, data=payload)
        logged_in = self.is_logged_in()
        if logged_in:
            print('Login succeeded')
        else:
            print('Login failed')
        return logged_in
    

    def is_logged_in(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)["loggedIn"] == "true"
   

    def list_event_types(self) -> list[tuple]:
        payload_dict = {
            "filter": self.create_market_filter(),
            "textQuery": None,
            "facets": [
                {
                    "type": "EVENT_TYPE",
                    "maxValues": 0,
                    "skipValues": 0,
                    "applyNextTo": 0
                }
            ],
            "currencyCode": "AUD",
            "locale": "en_GB"
        }
        payload = json.dumps(payload_dict)
        headers = {
            'content-type': 'application/json',
        }
        response = self.session.request("POST", self.EXCHANGE_API, headers=headers, data=payload)
        response_dict = json.loads(response.text)
        results = [(key, result_dict['name']) for key, result_dict in response_dict['attachments']['eventTypes'].items()]
        return results
    

    def list_competitions(self, filter: dict = None) -> list[dict]:
        payload_dict = {
            "filter": self.create_market_filter(),
            "facets": [
                {
                    "type": "COMPETITION",
                    "maxValues": 0,
                    "skipValues": 0,
                    "applyNextTo": 0
                }
            ],
            "currencyCode": "AUD",
            "locale": "en_GB"
        }
        if filter is not None:
            payload_dict["filter"].update(filter)
        payload = json.dumps(payload_dict)
        headers = {
            'content-type': 'application/json',
        }
        response = self.session.request("POST", self.EXCHANGE_API, headers=headers, data=payload)
        response_dict = json.loads(response.text)

        results = []
        for result_dict in response_dict["facets"][0]["values"]:
            comp_id = str(result_dict["key"]["competitionId"])
            # cardinality = result_dict["cardinality"]
            competition_dict = response_dict["attachments"]["competitions"][comp_id]
            results.append(competition_dict)
        return results
    

    def list_events(self, filter: dict = None) -> list[dict]:
        url = "https://scan-inbf.betfair.com.au/www/sports/navigation/facet/v1/search?_ak=nzIFcwyWhrlwYMrh&alt=json"
        payload_dict = {
            "filter": self.create_market_filter(),
            "facets": [
                {
                    "type": "EVENT",
                    "maxValues": 0,
                    "skipValues": 0,
                    "applyNextTo": 0
                }
            ],
            "currencyCode": "AUD",
            "locale": "en_GB"
        }
        if filter is not None:
            payload_dict["filter"].update(filter)
        payload = json.dumps(payload_dict)
        headers = {
            'content-type': 'application/json',
        }
        response = self.session.request("POST", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)

        results = []
        for result_dict in response_dict["facets"][0]["values"]:
            event_id = str(result_dict["key"]["eventId"])
            # cardinality = result_dict["cardinality"]
            event_dict = response_dict["attachments"]["events"][event_id]
            results.append(event_dict)
        return results
    

    def list_market_types(self, filter: dict = None) -> list[str]:
        payload_dict = {
            "filter": self.create_market_filter(),
            "facets": [
                {
                    "type": "MARKET_TYPE",
                    "maxValues": 0,
                    "skipValues": 0,
                    "applyNextTo": 0
                }
            ],
            "currencyCode": "AUD",
            "locale": "en_GB"
        }
        if filter is not None:
            payload_dict["filter"].update(filter)
        payload = json.dumps(payload_dict)
        headers = {
            'content-type': 'application/json',
        }
        response = self.session.request("POST", self.EXCHANGE_API, headers=headers, data=payload)
        response_dict = json.loads(response.text)

        results = []
        for result_dict in response_dict["facets"][0]["values"]:
            market_type = result_dict["value"]
            # cardinality = result_dict["cardinality"]
            results.append(market_type)
        return results


    def list_market_catalogue(self, filter: dict = None) -> list[dict]:
        payload_dict = {
            "filter": self.create_market_filter(),
            "facets": [
                {
                    "type": "MARKET",
                    "maxValues": 0,
                    "skipValues": 0,
                    "applyNextTo": 0
                }
            ],
            "currencyCode": "AUD",
            "locale": "en_GB"
        }
        if filter is not None:
            payload_dict["filter"].update(filter)
        payload = json.dumps(payload_dict)
        headers = {
            'content-type': 'application/json',
        }
        response = self.session.request("POST", self.EXCHANGE_API, headers=headers, data=payload)
        response_dict = json.loads(response.text)

        results = []
        for result_dict in response_dict["facets"][0]["values"]:
            market_id = str(result_dict["key"]["marketId"])
            # cardinality = result_dict["cardinality"]
            market_dict = response_dict["attachments"]["markets"][market_id]
            results.append(market_dict)
        return results
    

    def get_markets(self, market_id_list: list[str], req_batch_size: int = 33) -> list[dict]:
        '''
        Gets the market data and odds for a list of markets by market_id. If not logged in, market data will be delayed.

        :param int req_batch_size: The batch size to determine how many markets are requested per API call.
                                    If this value is 0, all markets are requested in one batch.
                                    Large batch sizes aren't permitted by the API (33 seems to be the maximum).

        '''
        result_list = []
        if req_batch_size == 0:
            n_batches = 1
        else:
            n_batches = len(market_id_list)//req_batch_size + int(len(market_id_list)%req_batch_size > 0)
        for i in range(n_batches):
            market_id_batch = market_id_list[req_batch_size*i:req_batch_size*(i+1)] if i != n_batches-1 else market_id_list[req_batch_size*i:]
            params = {
                "_ak": "nzIFcwyWhrlwYMrh",
                "alt": "json",
                "currencyCode": "AUD",
                "locale": "en_GB",
                "marketIds": ','.join(market_id_batch),
                "rollupLimit": "5",
                "rollupModel": "STAKE",
                "types": "MARKET_STATE,RUNNER_STATE,RUNNER_EXCHANGE_PRICES_BEST,RUNNER_SP"
            }
            headers = {}
            response = self.session.request("GET", self.MARKET_DATA_API, headers=headers, params=params)
            response_dict = json.loads(response.text)
            market_dict = {}
            for event in response_dict["eventTypes"][0]["eventNodes"]:
                for market in event['marketNodes']:
                    market_dict[market['marketId']] = market
            result_list.extend(market_dict[market_id] for market_id in market_id_batch)
        return result_list
    

    def custom_query(self, filter: dict, facets: dict):
        raise NotImplementedError()
    

    @ staticmethod
    def _print_dict(dict, sort_keys=False):
        print(json.dumps(
            dict,
            sort_keys=sort_keys,
            indent=4,
            separators=(',', ': ')
        ))

