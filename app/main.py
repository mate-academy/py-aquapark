class IntegerRange:
    def __init__(self, min_amount, max_amount):
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner, name):
        self.protected_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        # Validação de tipo
        if not isinstance(value, int):
            raise TypeError("Value must be an integer.")
        
        # Validação de intervalo
        if not (self.min_amount <= value <= self.max_amount):
            raise ValueError(f"Value must be between {self.min_amount} and {self.max_amount}.")
        
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator:
    # Os descritores serão definidos nas subclasses
    def __init__(self, age, weight, height):
        # Atribuir aqui dispara o __set__ dos descritores nas subclasses
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name, limitation_class):
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor):
        try:
            # Tenta instanciar o validador com os dados do visitante.
            # Se algum dado estiver fora do range, o IntegerRange lançará um erro.
            self.limitation_class(
                age=visitor.age, 
                weight=visitor.weight, 
                height=visitor.height
            )
            return True
        except (TypeError, ValueError):
            return False

# --- Exemplo de Uso ---
kids_slide = Slide("Kamikaze Kids", ChildrenSlideLimitationValidator)
visitor_child = Visitor("Alice", age=10, weight=30, height=100)
visitor_adult = Visitor("Bob", age=30, weight=80, height=180)

print(f"{visitor_child.name} can access {kids_slide.name}: {kids_slide.can_access(visitor_child)}") # True
print(f"{visitor_adult.name} can access {kids_slide.name}: {kids_slide.can_access(visitor_adult)}") # False
