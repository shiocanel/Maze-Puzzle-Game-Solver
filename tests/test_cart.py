from snacky_dash.engine.cart import Cart
from snacky_dash.engine.color import Color


def test_cart():
    cart = Cart(Color.RED, (2, 2), (5, 3))

    assert cart.free_spaces() == 9
    assert not cart.is_full()

    assert cart.is_position_part_of_cart((2, 2))
    assert cart.is_position_part_of_cart((3, 3))
    assert cart.is_position_part_of_cart((4, 4))
    assert cart.is_position_part_of_cart((2, 4))
    assert cart.is_position_part_of_cart((4, 2))

    assert not cart.is_position_part_of_cart((5, 5))
    assert not cart.is_position_part_of_cart((1, 2))
    assert not cart.is_position_part_of_cart((5, 3))

    assert cart.is_position_delivery((5, 3))

    cart_01 = cart.load(5)

    assert cart_01.free_spaces() == 4
    assert not cart_01.is_full()

    cart_02 = cart_01.load(3)

    assert cart_02.free_spaces() == 1
    assert not cart_02.is_full()

    cart_03 = cart_02.load(4)

    assert cart_03.free_spaces() == 0
    assert cart_03.is_full()

    cart_04 = cart_03.load(7)

    assert cart_04.free_spaces() == 0
    assert cart_04.is_full()

    assert cart.free_spaces() == 9
    assert not cart.is_full()
