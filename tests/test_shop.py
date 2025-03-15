PRODUCTS_TO_BUY_SUCCESS = 500
DIGIT_FOR_BUYING = 5
"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def second_product():
    return Product("smth", 150, "This is awesome", 500)

@pytest.fixture()
def cart():
    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(product.quantity - 1)
        assert product.check_quantity(product.quantity)
        assert product.check_quantity(product.quantity + 1) is False

    def test_product_buy(self, product):
        shop_have_products = product.quantity
        assert product.buy(PRODUCTS_TO_BUY_SUCCESS) == shop_have_products-PRODUCTS_TO_BUY_SUCCESS

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)



class TestCart:

    def test_add_product_without_product(self, product, cart):
        cart.add_product(product=product)
        assert cart.products[product] == 1

    def test_add_product_two_times(self, product, cart):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        assert cart.products[product] == 5
        cart.add_product(product=product, buy_count=10)
        assert cart.products[product] == 15

    def test_remove_product_success(self, product, cart):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.remove_product(product=product, remove_count=3)
        assert cart.products[product] == 2

    def test_remove_product_without_remove_count(self, product,cart):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.remove_product(product=product)
        assert product not in cart.products

    def test_remove_product_with_remove_count_is_null(self, product, cart):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.remove_product(product=product, remove_count=0)
        assert cart.products[product] == DIGIT_FOR_BUYING

    def test_remove_product_with_remove_count_equal_product_count(self, product, cart):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.remove_product(product=product, remove_count=DIGIT_FOR_BUYING)
        assert product not in cart.products

    def test_remove_product_with_two_added_products(self, product, second_product, cart):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.add_product(product=second_product, buy_count=DIGIT_FOR_BUYING)
        cart.remove_product(product=product, remove_count=DIGIT_FOR_BUYING)
        assert product not in cart.products
        assert cart.products[second_product] == DIGIT_FOR_BUYING

    def test_remove_product_incorrect_digit(self, product, cart):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        with pytest.raises(ValueError):
            cart.remove_product(product=product, remove_count=-5)

    def test_remove_product_that_not_in_cart(self, product,cart, second_product):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        with pytest.raises(ValueError, match="Нет такого продукта в корзине"):
            cart.remove_product(product=second_product)


    def test_clear(self, product, cart, second_product):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.add_product(product=second_product, buy_count=DIGIT_FOR_BUYING)
        cart.clear()
        assert cart.products == {}

    def test_get_price(self, product,cart):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        assert cart.get_total_price() == product.price*DIGIT_FOR_BUYING

    def test_get_price_for_two_products(self, product, cart, second_product):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.add_product(product=second_product)
        assert cart.get_total_price() == product.price*DIGIT_FOR_BUYING+second_product.price

    def test_get_price_without_products_in_cart(self, cart):
        with pytest.raises(ValueError, match="Нет продуктов"):
            cart.get_total_price()

    def test_buy_product(self, cart, product):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.buy()

    def test_buy_product_with_empty_cart(self,cart):
        with pytest.raises(ValueError, match="Нет товаров в корзине"):
            cart.buy()

    def test_buy_product_without_quantity_in_shop(self,cart,product):
        cart.add_product(product=product, buy_count=10000)
        with pytest.raises(ValueError, match="Нет столько товара"):
            cart.buy()

    def test_buy_products(self,cart, product, second_product):
        cart.add_product(product=product, buy_count=DIGIT_FOR_BUYING)
        cart.add_product(product=second_product, buy_count=DIGIT_FOR_BUYING)
        cart.buy()


    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """