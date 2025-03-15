from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        if quantity <= 0:
            raise ValueError("Должно быть положительное число")
        return self.quantity >= quantity

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity):
            bought = self.quantity - quantity
            return bought
        else:
            raise ValueError("Нет столько товара")

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        self.products[product] = self.products.get(product, 0) + buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product not in self.products:
            raise ValueError("Нет такого продукта в корзине")
        if remove_count is None or remove_count >= self.products.get(product):
            self.products.pop(product)

        elif remove_count < 0:
            raise ValueError("Отрицательное количество удаляемого товара")
        else:
            self.products[product] -= remove_count

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        if self.products == {}:
            raise ValueError("Нет продуктов")
        total_price = 0
        for product, quantity in self.products.items():
            total_price += product.price*self.products[product]
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        if not self.products:
            raise ValueError("Нет товаров в корзине")
        for product, quantity in self.products.items():
            product.buy(self.products[product])

