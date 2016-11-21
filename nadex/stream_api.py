from .lightstreamer import LSClient, Subscription


class NadexStreamApi(object):

    def __init__(self, account_id, xst, endpoint):
        self.ls_client = LSClient(endpoint,
                                  adapter_set="InVisionProvider",
                                  user=account_id,
                                  password='XST-{}'.format(xst))
        self.ls_client_keys = []
        
    def connect(self):
        self.ls_client_keys = []
        self.ls_client.connect()
        self.subscribe_account_update()

    def disconnect(self):
        for key in self.ls_client_keys:
            self.unsubscribe(key)
        self.ls_client.disconnect()
        

    def subscribe_account_update(self):
        s = Subscription(
                mode="MERGE",
                items=['V2-AD-AC_AVAILABLE_BALANCE'],
                fields=["ACC"],
        )
        s.addlistener(self.on_account_update)
        self.ls_client_keys.append(self.ls_client.subscribe(s))

    def subscribe_price_update(self, epic):
        s = Subscription(
                mode="MERGE",
                items=['V2-F-HIG,CPC,UBS,AS1,CBS,BS1,AK1,CPT,LOW,CSP,UTM,BD1|{epic}'.format(epic=epic)],
                fields=["HIG", "CPC", "UBS", "AS1", "CBS", "BS1", "AK1", "CPT", "LOW", "CSP", "UTM", "BD1"],
        )
        s.addlistener(self.on_prices_update)
        self.ls_client_keys.append(self.ls_client.subscribe(s))

    def ubsubscribe(self, key):
        self.ls_client.unsubscribe(key)

        
        
    # A simple function acting as a Subscription listener
    def on_prices_update(self, item_update):
        name = item_update.get('name','').split('|')[1]
        print(name, item_update.get('values'))

    def on_account_update(self, balance_update):
        print("balance: %s " % balance_update)
        
