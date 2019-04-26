import numpy as np
from cppimport import import_hook
from sicdock.geom import primitive_test
from sicdock.geom import miniball


def test_geom_sphere():
    assert primitive_test.TEST_geom_primitive_sphere()


def test_geom_welzl_sphere():
    assert primitive_test.TEST_geom_primitive_welzl_bounding_sphere()


def test_miniball():
    assert miniball.test_miniball(10_000, 7, False)
    assert miniball.test_miniball(10_000, 12, False)


def test_miniball_py():
    crd = np.random.randn(10_000, 7)
    sph = miniball.miniball(crd)
    rad, *cen = sph
    d = np.linalg.norm(crd - cen, axis=1)
    print(np.min(d), np.max(d))
    assert np.max(d) <= rad + 0.00000001


if __name__ == "__main__":
    # test_geom_sphere()
    # test_geom_welzl_sphere()
    test_miniball()
    test_miniball_py()
