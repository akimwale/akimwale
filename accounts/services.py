# crypto/services.py

from pycoingecko import CoinGeckoAPI

class CoinGeckoService:
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def get_price(self, ids, vs_currencies):
        return self.cg.get_price(ids=ids, vs_currencies=vs_currencies)

    def get_coins_list(self):
        return self.cg.get_coins_list()

    def get_coin_market_chart(self, id, vs_currency, days):
        return self.cg.get_coin_market_chart(id=id, vs_currency=vs_currency, days=days)
    
    def get_conversion_rate(self, from_currency, to_currency):
        return self.cg.get_price(ids=from_currency, vs_currencies=to_currency)