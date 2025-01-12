from src.connect.ranged_variable import RangedVariable


def test_int_init():

    ranged_variable = RangedVariable(value=0,
                                     minimum=0,
                                     maximum=1)

    assert ranged_variable.minimum_value == 0
    assert ranged_variable.maximum_value == 1
    assert ranged_variable.value == 0

    ranged_variable.value = 1
    assert ranged_variable.value == 1

    ranged_variable.minimum_value = 1
    assert ranged_variable.minimum_value == 1

    ranged_variable.maximum_value = 2
    assert ranged_variable.maximum_value == 2


def test_float_init():

    ranged_variable = RangedVariable(value=0.0,
                                     minimum=0.0,
                                     maximum=1.0)

    assert ranged_variable.minimum_value == 0.0
    assert ranged_variable.maximum_value == 1.0
    assert ranged_variable.value == 0.0

    ranged_variable.value = 1.0
    assert ranged_variable.value == 1.0

    ranged_variable.minimum_value = 1.0
    assert ranged_variable.minimum_value == 1.0

    ranged_variable.maximum_value = 2.0
    assert ranged_variable.maximum_value == 2.0


def test_ranged_init():

    min_ranged_variable = RangedVariable(value=0,
                                         minimum=0,
                                         maximum=1)

    max_ranged_variable = RangedVariable(value=1,
                                         minimum=1,
                                         maximum=2)

    ranged_variable = RangedVariable(value=0,
                                     minimum=min_ranged_variable,
                                     maximum=max_ranged_variable)

    assert ranged_variable.minimum_value == 0
    assert ranged_variable.maximum_value == 1
    assert ranged_variable.value == 0

    ranged_variable.value = 1
    assert ranged_variable.value == 1

    ranged_variable.minimum_value = 1
    assert ranged_variable.minimum_value == 1

    ranged_variable.maximum_value = 2
    assert ranged_variable.maximum_value == 2


def test_mixed_init():
    min_ranged_variable = RangedVariable(value=0,
                                         minimum=0,
                                         maximum=1)

    max_ranged_variable = RangedVariable(value=1,
                                         minimum=1,
                                         maximum=2)

    ranged_variable = RangedVariable(value=0,
                                     minimum=min_ranged_variable,
                                     maximum=max_ranged_variable)

    assert ranged_variable.minimum_value == 0
    assert ranged_variable.maximum_value == 1
    assert ranged_variable.value == 0

    ranged_variable.value = 1
    assert ranged_variable.value == 1

    ranged_variable.minimum_value = 1
    assert ranged_variable.minimum_value == 1

    ranged_variable.maximum_value = 2
    assert ranged_variable.maximum_value == 2
