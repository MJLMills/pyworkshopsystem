import array
import numpy as np


class LorenzSystem:
    """

    Parameters
    ----------
    x : float
        The current x-coordinate. Default starting value is 0.0.
    y : float
        The current y-coordinate. Default starting value is 1.0.
    z : float
        The current z-coordinate. Default starting value is 1.05.
    sigma : float
        Default value is 10.
    rho : float
        Default value is 28.
    beta : float
        Default value is 8/3.

    Attributes
    ----------
    x, y, z -> float
        The current coordinates.

    Methods
    -------
    take_step -> None
        Take a single step along the trajectory.
    """

    def __init__(self,
                 x=0.9,
                 y=0,
                 z=0,
                 sigma=10,
                 rho=28,
                 beta=8 / 3):

        self._x_init = x
        self._y_init = y
        self._z_init = z

        self._x = None
        self._y = None
        self._z = None
        self.reset()

        self._sigma = sigma
        self._rho = rho
        self._beta = beta

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def coordinates(self):
        return array.array('f', [self._x, self._y, self._z])

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, sigma):
        self._sigma = sigma

    @property
    def rho(self):
        return self._rho

    @rho.setter
    def rho(self, rho):
        self._rho = rho

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, beta):
        self._beta = beta

    def __compute_derivatives(self, x, y, z):
        dx_dt = self._sigma * (y - x)
        dy_dt = x * (self._rho - z) - y
        dz_dt = (x * y) - (self._beta * z)

        values = array.array('d', [dx_dt, dy_dt, dz_dt])

        return values

    def take_step(self, step_size) -> None:
        partial_derivatives = self.__compute_derivatives(self._x,
                                                         self._y,
                                                         self._z)

        self._x = self._x + (partial_derivatives[0] * step_size)
        self._y = self._y + (partial_derivatives[1] * step_size)
        self._z = self._z + (partial_derivatives[2] * step_size)

    def reset(self):
        self._x = self._x_init
        self._y = self._y_init
        self._z = self._z_init
