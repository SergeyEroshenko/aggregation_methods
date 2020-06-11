class HitBTC:

    import json as json
    import requests

    def __init__(self):        
        self._addr = 'https://api.hitbtc.com'

    def get_currencies(self):
        currs = self.json.loads(
            self.requests.get(self._addr + '/api/2/public/currency').content
            )
        return currs
    
    def available_currencies(self):
        currs = self.get_currencies()
        return [currs[i]['id'] for i in range(len(currs))]

    def symbol_info(self, symbol):
        symbol = self.json.loads(
            self.requests.get(
                self._addr + '/api/2/public/symbol/{}'.format(symbol)
                ).content
            )
        return symbol

    def all_symbols(self):
        symbols = self.json.loads(
            self.requests.get(self._addr + '/api/2/public/symbol/').content
            )
        return symbols
    
    def get_trades(self, symbol, **kwargs):
        k = kwargs
        k = '&'.join(['{0}={1}'.format(x[0], x[1]) for x in zip(k.keys(), k.values())])
        res = self.requests.get(
                self._addr + '/api/2/public/trades/{0}?{1}'.format(symbol, k)
                )
        trades = self.json.loads(res.content)
        code = res.status_code
        
        return trades, code