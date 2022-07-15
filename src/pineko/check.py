# -*- coding: utf-8 -*-
"""Tools to check compatibility of EKO and grid."""
import numpy as np


def islepton(el):
    """Return True if el is a lepton PID, otherwise return False."""
    if 10 < abs(el) < 17:
        return True
    return False


def in1d(a, b, rtol=1e-05, atol=1e-08):
    """Improved version of np.in1d.

    Thanks: https://github.com/numpy/numpy/issues/7784#issuecomment-848036186

    Parameters
    ----------
    a : list
        needle
    b : list
        haystack
    rtol : float
        allowed relative error
    atol : float
        allowed absolute error

    Returns
    -------
    list
        mask of found elements
    """
    if len(a) == 1:
        for be in b:
            if np.isclose(be, a[0], rtol=rtol, atol=atol):
                return [True]
        return [False]
    ss = np.searchsorted(a[1:-1], b, side="left")
    return np.isclose(a[ss], b, rtol=rtol, atol=atol) | np.isclose(
        a[ss + 1], b, rtol=rtol, atol=atol
    )


def check_grid_and_eko_compatible(pineappl_grid, operators, xif):
    """Check whether the EKO operators and the PineAPPL grid are compatible.

    Parameters
    ----------
    pineappl_grid : pineappl.grid.Grid
        grid
    operators : eko.output.Output
        operators
    xif : float
        factorization scale variation

    Raises
    ------
    ValueError
        If the operators and the grid are not compatible.
    """
    x_grid, _pids, _mur2_grid, muf2_grid = pineappl_grid.axes()
    # Q2 grid
    if not np.all(
        in1d(
            np.unique(list(operators["Q2grid"].keys())), xif * xif * np.array(muf2_grid)
        )
    ):
        raise ValueError(
            "Q2 grid in pineappl grid and eko operator are NOT compatible!"
        )
    # x-grid
    if not np.all(in1d(np.unique(operators["targetgrid"]), np.array(x_grid))):
        raise ValueError("x grid in pineappl grid and eko operator are NOT compatible!")


def is_fonll_b(fns, lumi):
    """Check if the fktable we are computing is a DIS FONLL-B fktable.

    Parameters
    ----------
        fns : str
            flavor number scheme (from the theory card)
        lumi : list(list(tuple))
            luminosity info

    Returns
    -------
            : bool
            true if the fktable is a FONLL-B DIS fktable
    """
    for lists in lumi:
        for el in lists:
            if (not islepton(el[0])) and (not islepton(el[1])):
                # in this case we are sure it is not DIS so for sure it is not FONLL-B
                return False
    if fns == "FONLL-B":
        return True
    return False


def contains_fact(grid):
    """Check whether factorization scale-variations are available in the pineappl grid.

    Parameters
    ----------
        grid: pineappl.grid.Grid
            Pineappl grid
    """
    order_list = [order.as_tuple() for order in grid.orders()]
    as_orders = []
    for order in order_list:
        as_orders.append(order[0])
    min_as = min(as_orders)
    order_is_present = False
    for order in order_list:
        # fact sv starts at NLO with respect to the first non zero order
        if order[0] == min_as + 1:
            order_is_present = True
            if order[-1] != 0:
                return
    if not order_is_present:
        return
    raise ValueError("Factorization scale variations are not available for this grid")


def contains_ren(grid):
    """Check whether renormalization scale-variations are available in the pineappl grid.

    Parameters
    ----------
        grid: pineappl.grid.Grid
            Pineappl grid
    """
    order_list = [order.as_tuple() for order in grid.orders()]
    as_orders = []
    for order in order_list:
        as_orders.append(order[0])
    # ren sv starts one order after the first order with as
    min_as = 1 if min(as_orders) == 0 else min(as_orders)
    order_is_present = False
    for order in order_list:
        if order[0] == min_as + 1:
            order_is_present = True
            if order[-2] != 0:
                return
    if not order_is_present:
        return
    raise ValueError("Renormalization scale variations are not available for this grid")
