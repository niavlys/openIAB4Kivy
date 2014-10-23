import kivy
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.properties import *
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from kivy import Logger

__version__ = "0.0.4"

import oiabilling

"""
from jnius import autoclass
Environnement = autoclass('android.os.Environment')
Context = autoclass('android.content.Context')
Activity = autoclass('android.app.Activity')
PythonActivity = autoclass('org.renpy.android.PythonActivity')
activity = PythonActivity.mActivity

OpenIabHelper = autoclass('org.onepf.oms.OpenIabHelper')
Config = autoclass('org.onepf.trivialdrivegame.Config')

"""

class BuyButton(Button):
    sku = StringProperty(None)
    name = StringProperty(None)
    def __init__(self, sku,**kwargs):
        self.sku=sku
        self.name=sku.split('.')[-1]
        kwargs.setdefault('text',self.name)
        super(BuyButton, self).__init__(**kwargs)
        billing.bind(consumed=self.checkPurchase)
        self.checkPurchase()
        
    def on_press(self,*args):
        if billing.isConsumable(self.sku) and billing.consumed.has_key(self.sku) and billing.consumed[self.sku]:
            billing.consume(self.sku)
        else:
            billing.purchase(self.sku)

    def checkPurchase(self,*args):
        if billing.consumed.has_key(self.sku) and billing.consumed[self.sku]:
            if not billing.isConsumable(self.sku):
                self.text='already bought %s'%self.name
                self.disabled=True
            else:
                self.text="Consume %s"%self.name
                self.disabled=False
        else:
                self.text=self.name
                self.disabled=False

class OpenIABTestApp(App):
    billing=ObjectProperty(None)
    
    def build(self):
        global billing
        self.billing = billing = oiabilling.Billing(["fr.alborini.openiab4kivy.premium","fr.alborini.openiab4kivy.infinitegas","fr.alborini.openiab4kivy.gas"],
                                                    'fr.alborini.openiab4kivytest.Config')
        self.billing.setConsumable("fr.alborini.openiab4kivy.gas")
        bl=BoxLayout()
        for i in self.billing.skus:
            p = BuyButton(sku=i)
            bl.add_widget(p)
        return bl

    def on_pause(self):
        return True
        
    def on_resume(self):
        pass

       
if __name__=='__main__':
    OpenIABTestApp().run()
