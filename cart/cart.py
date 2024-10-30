from decimal import Decimal


class Cart(object):
 def __init__(self, request):
     self.session = request.session
     cart = self.session.get('session_key')
     if not cart:
         # save an empty cart in the session
         cart = self.session['session_key'] = {}
     
     #make sure cart is avilable in all pages
     self.cart = cart



def add(self, product):
     product_id = str(product.id)
     if product_id in self.cart:
        pass
     else:
         self.cart[product_id] = {'price' : str(product.price)}
     self.session.modified = True

def remove(self, product):
     product_id = str(product.id)
     if product_id in self.cart:
         del self.cart[product_id]
     self.save()


def __iter__(self, product):
     product_ids = self.cart.keys()
     # get the product objects and add them to the cart
     products = product.objects.filter(id__in=product_ids)
     cart = self.cart.copy()
     for product in products:
         cart[str(product.id)]['product'] = product
     for item in cart.values():
         item['price'] = Decimal(item['price'])
         item['total_price'] = Decimal(item['price']) * item['quantity']
         yield item

def __len__(self):
     return sum(item['quantity'] for item in self.cart.values())

def get_sub_total_price(self):
     return sum(Decimal(item['price']) * item['quantity'] for item
                in self.cart.values())

def clear(self):
     """
     Remove all items from the cart.
     """
     for key in list(self.cart.keys()):  # Use list() to create a copy of keys
         del self.cart[key]
     self.save()
