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


# Abstract Factory Pattern
class AbstactFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_dough(self): pass

    @abstractmethod
    def create_sauce(self): pass

    @abstractmethod
    def create_cheese(self): pass

# Facade Pattern
# - provide a unified interface to a set of interfaces in a subsystem
# - define a higher-level interface that makes the subsystem easier to use
class HomeTheaterFacade:
    def __init__(self, amp, tuner, dvd, cd, projector, lights, screen, popper):
        self.amp = amp
        self.tuner = tuner
        self.dvd = dvd
        self.cd = cd
        self.projector = projector
        self.lights = lights
        self.screen = screen
        self.popper = popper
    
    def watch_movie(self, movie):
        print('Get ready to watch a movie...')
        self.popper.on()
        self.popper.pop()
        self.lights.dim(10)
        self.screen.down()
        self.projector.on()
        self.projector.wide_screen_mode()
        self.amp.on()
        self.amp.set_dvd(self.dvd)
        self.amp.set_surround_sound()
        self.amp.set_volume(5)
        self.dvd.on()
        self.dvd.play(movie)
    
    def end_movie(self):
        print('Shutting movie theater down...')
        self.popper.off()
        self.lights.on()
        self.screen.up()
        self.projector.off()
        self.amp.off()
        self.dvd.stop()
        self.dvd.eject()
        self.dvd.off()

# Proxy Pattern
# - provide a surrogate or placeholder for another object to control access to it
# - use an extra level of indirection to support distributed, controlled, or intelligent access
import random
import gc
class AbstactSubject(metaclass=ABCMeta):
    @abstractmethod
    def sort(self): pass

class RealSubject(AbstactSubject):
    def __init__(self):
        self.digits = []
        for _ in range(10000000):
            self.digits.append(random.random())
    
    def sort(self, reverse=False):
        self.digits.sort()
        if reverse:
            self.digits.reverse()

class Proxy(AbstactSubject):
    reference_count = 0
    def __init__(self):
        if not getattr(self.__class__, 'cached_object', None):
            self.__class__.cached_object = RealSubject()
            print('Created new object')
        else:
            print('Using cached object')
        self.__class__.reference_count += 1
        print(f'Count of references = {self.__class__.reference_count}')
    
    def sort(self, reverse=False):
        print('Called sort method of proxy')
        self.__class__.cached_object.sort(reverse=reverse)
    
    def __del__(self):
        self.__class__.reference_count -= 1

        if self.__class__.reference_count == 0:
            print('Number of reference_count is 0. Deleting cached object...')
            del self.__class__.cached_object
        print(f'Count of references = {self.__class__.reference_count}')

proxy = Proxy()
proxy2 = Proxy()
proxy.sort(reverse=True)
del proxy
del proxy2
gc.collect() # del not work in pypy3 interpreter without this line

# Observer Pattern
# - when one object changes state, all its dependents are notified and updated automatically
import time, datetime
class Subject():
    def __init__(self):
        self.observers = []
        self.cur_time = None
    
    def register_observer(self, observer):
        if observer in self.observers:
            print(observer, 'already in subscribed observers')
        else:
            self.observers.append(observer)
    
    def unregister_observer(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print('No such observer in subject')
    
    def notify_observers(self):
        self.cur_time = time.time()
        for observer in self.observers:
            observer.notify(self.cur_time)

class Observer(metaclass=ABCMeta):
    @abstractmethod
    def notify(self, unix_timestamp): pass

class USATimeObserver(Observer):
    def __init__(self, name):
        self.name = name
    
    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d %I:%M:%S%p')
        print(f'Observer {self.name} says: {time}')

class EUTimeObserver(Observer):
    def __init__(self, name):
        self.name = name
    
    def notify(self, unix_timestamp):
        time = datetime.datetime.fromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        print(f'Observer {self.name} says: {time}')


subject = Subject()
observer1 = USATimeObserver('USATimeObserver')
subject.register_observer(observer1)
subject.notify_observers()
time.sleep(2)
observer2 = EUTimeObserver('EUATimeObserver')
subject.register_observer(observer2)
subject.notify_observers()
time.sleep(2)
subject.unregister_observer(observer2)
subject.notify_observers()


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
