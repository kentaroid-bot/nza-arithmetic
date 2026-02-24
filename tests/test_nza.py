import pytest
import math
import numpy as np
from nza import NZA

def test_init_and_repr():
    zero = NZA(0)
    assert zero.local == 0.0
    assert "0_local + ∞_universe" in repr(zero)
    
    pos = NZA(5)
    assert pos.local == 5.0
    assert "5_local + ∞_universe" in repr(pos)
    
    neg = NZA(-3)
    assert neg.local == -3.0
    assert "-3_local + ∞_universe" in repr(neg)
    
    inf_div = NZA(1) / NZA(0)
    assert "∞_density + ∞_universe" in repr(inf_div)

def test_addition():
    a = NZA(2)
    b = NZA(3)
    result = a + b
    assert result.local == 5.0
    assert math.isinf(result.total)

def test_subtraction():
    a = NZA(5)
    b = NZA(3)
    result = a - b
    assert result.local == 2.0
    
    result_neg = b - a
    assert result_neg.local == -1.0

def test_multiplication():
    a = NZA(4)
    b = NZA(2)
    result = a * b
    assert result.local == 8.0

def test_division():
    a = NZA(10)
    b = NZA(2)
    result = a / b
    assert result.local == 5.0
    
    div_zero = NZA(42) / NZA(0)
    assert math.isinf(div_zero.local)

def test_conservation():
    a = NZA(5)
    zeroish = a - a
    assert zeroish.local == 0.0
    assert math.isinf(zeroish.total)

def test_no_annihilation():
    five = NZA(5)
    minus_five = -five
    sum_ = five + minus_five
    assert sum_.local == 0.0
    assert "∞_universe" in repr(sum_)

def test_numpy_array_support():
    arr = np.array([1,2,3])
    nza_arr = NZA(arr)
    assert np.all(nza_arr.local == arr)
    
    result = nza_arr + NZA(1)
    assert np.all(result.local == [2,3,4])

def test_eq():
    a = NZA(1.000001)
    b = NZA(1)
    assert a == b

def test_div_zero_array():
    arr = NZA(np.array([1,0,3]))
    div_zero = arr / NZA(0)
    assert np.all(np.isinf(div_zero.local))