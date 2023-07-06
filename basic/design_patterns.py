from abc import ABCMeta, abstractmethod

# Singelton Pattern
# create only one instance of a class

class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

class Child(Singleton):
    pass

s = Singleton()
ch0 = Child()
ch1 = Child()
print(ch0 is ch1, s is ch0, s is ch1)

# Borg Pattern
# Borg is also known as monostate pattern, all of the instances are different, but they share the same data
class Borg:
    _shared_state = {}
    def __new__(cls, *args, **kwargs):
        obj = super(Borg, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj
    
    def __init__(self):
        self.__dict__ = self._shared_state

class Child(Borg):
    pass

class OtherChild(Borg):
    _shared_state = {}

borg = Borg()
child = Child()
print(borg is child)
borg.only_var = "I'm shared"
print(child.only_var)

other_child = OtherChild()
try:
    print(other_child.only_var)
except Exception as e:
    print(e)


# Factory Pattern
# - loose coupling, encapsulate the object creation
# - reuse existing object and avoid creating duplicate objects
class Pizza:
    def __init__(self):
        self.name = None
        self.dough = None
        self.sauce = None
        self.toppings = []
    
    def prepare(self):
        print(f'Preparing {self.name}')
        print('Tossing dough...')
        print('Adding sauce...')
        print('Adding toppings: ')
        for topping in self.toppings:
            print(f'    {topping}')
    
    def bake(self):
        print('Bake for 25 minutes at 350')
    
    def cut(self):
        print('Cutting the pizza into diagonal slices')
    
    def box(self):
        print('Place pizza in official PizzaStore box')
    
    def get_name(self):
        return self.name

class SimplePizzaFactory:
    def create_pizza(self, type):
        pizza = Pizza()
        pizza.name = type
        pizza.dough = 'Regular Crust'
        pizza.sauce = 'Marinara Pizza Sauce'
        pizza.toppings.append('Fresh Mozzarella')
        pizza.toppings.append('Parmesan')
        return pizza

class PizzaStore(metaclass=ABCMeta):
    
    def order_pizza(self, type):

        pizza = self.create_pizza(type)
        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()
        return pizza
    
    @abstractmethod
    def create_pizza(self, type): pass

class NYPizzaStore(PizzaStore):
    def create_pizza(self, type):
        if type == 'cheese':
            return NYStyleCheesePizza()
        else:
            raise Exception(f'No such pizza: {type}')

class ChicagoPizzaStore(PizzaStore):
    def create_pizza(self, type):
        if type == 'cheese':
            return ChicagoStyleCheesePizza()
        else:
            raise Exception(f'No such pizza: {type}')


class NYStyleCheesePizza(Pizza):
    def __init__(self):
        super().__init__()
        self.name = 'NY Style Sauce and Cheese Pizza'
        self.dough = 'Thin Crust Dough'
        self.sauce = 'Marinara Sauce'
        self.toppings.append('Grated Reggiano Cheese')

class ChicagoStyleCheesePizza(Pizza):
    def __init__(self):
        super().__init__()
        self.name = 'Chicago Style Deep Dish Cheese Pizza'
        self.dough = 'Extra Thick Crust Dough'
        self.sauce = 'Plum Tomato Sauce'
        self.toppings.append('Shredded Mozzarella Cheese')
    
    def cut(self):
        print('Cutting the pizza into square slices')

NYStore = NYPizzaStore()
ChicagoStore = ChicagoPizzaStore()
p = NYStore.order_pizza('cheese')
print('Ethan ordered a ' + p.get_name() + '\n')
p = ChicagoStore.order_pizza('cheese')
print('Joel ordered a ' + p.get_name() + '\n')

# Model View Controller
# popular in web development, such as web2py, Pyramid, Django
# - Model: data access layer
# - View: presentation layer
# - Controller: business logic layer
# Benifits:
# 1. modify the views without touching the model and business logic and vice versa



class Quackable(metaclass=ABCMeta):
    @abstractmethod
    def quack(self): pass

class QuackCounter(Quackable):
    count = 0
    def __init__(self, duck):
        self.duck = duck

    def quack(self):
        self.duck.quack()
        QuackCounter.count += 1
    
    @staticmethod
    def get_quacks():
        return QuackCounter.count


class MallardDuck(Quackable):
    def quack(self):
        print('Quack')

class RedheadDuck(Quackable):
    def quack(self):
        print('Quack')

class RubberDuck(Quackable):
    def quack(self):
        print('Squeak')

class DuckCall(Quackable):
    def quack(self):
        print('Kwak')

class Goose:
    def honk(self):
        print('Honk')

class GooseAdapter(Quackable):
    def __init__(self, goose):
        self.goose = goose
    
    def quack(self):
        self.goose.honk()

class DuckSimulator:
    def simulate(self, duck=None):
        if duck is None:
            duck = QuackCounter(MallardDuck())
            self.simulate(duck)
            duck = QuackCounter(RedheadDuck())
            self.simulate(duck)
            duck = QuackCounter(RubberDuck())
            self.simulate(duck)
            duck = QuackCounter(DuckCall())
            self.simulate(duck)
            gooseDuck = GooseAdapter(Goose())
            self.simulate(gooseDuck)

            print(f'The ducks quacked {QuackCounter.get_quacks()} times')
        else:
            duck.quack()


DuckSimulator().simulate()
