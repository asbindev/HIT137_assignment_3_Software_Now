# Demonstrates the required OOP concepts:
# - multiple inheritance
# - multiple decorators
# - encapsulation
# - polymorphism
# - method overriding

def uppercase_decorator(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if isinstance(res, str):
            return res.upper()
        return res
    return wrapper

def add_tag_decorator(tag):
    def decorator(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if isinstance(res, str):
                return f"<{tag}>" + res + f"</{tag}>"
            return res
        return wrapper
    return decorator

class BaseExplain:
    def __init__(self):
        self._explanations = []

    def add(self, text):
        # encapsulated storage
        self._explanations.append(text)

    def explain_all(self):
        return "\n\n".join(self._explanations)

class OOPPartA:
    @uppercase_decorator
    def explain_inheritance(self):
        return 'multiple inheritance was used to combine behaviors from two parents.'

    @add_tag_decorator('p')
    def explain_decorators(self):
        return 'decorators are used to modify function behavior dynamically.'

class OOPPartB:
    def explain_encapsulation(self):
        return 'encapsulation restricts direct access to an object\'s internals (using _private attributes).'

    def explain_polymorphism(self):
        return 'polymorphism allows objects to be treated as instances of their base type, while using overriding methods.'

# Multiple inheritance and method overriding
class OOPCombined(BaseExplain, OOPPartA, OOPPartB):
    def __init__(self):
        BaseExplain.__init__(self)

    # override a method to show method overriding
    def explain_polymorphism(self):
        return 'OVERRIDDEN: polymorphism demonstrated by method overriding in child class.'

class OOPDemo:
    def __init__(self):
        self._combined = OOPCombined()
        # gather explanations
        self._combined.add(self._combined.explain_inheritance())
        self._combined.add(self._combined.explain_decorators())
        self._combined.add(self._combined.explain_encapsulation())
        # polymorphism - child override will be used
        self._combined.add(self._combined.explain_polymorphism())

    def explain_all(self):
        header = 'OOP Concepts Used and Where:\n\n'
        return header + self._combined.explain_all()
