def d_id(a, k):
    """
    function returning pair of vectors conatining
    indices of k-th diagonal of "a" matrix
    :param a: some 2D array
    :param k: index for which pairs of indices should be returned
    :return:
    """
    import numpy as np
    rows, cols = np.diag_indices_from(a)
    if k < 0:
        return rows[:k], cols[-k:]
    elif k > 0:
        return rows[k:], cols[:-k]
    else:
        return rows, cols