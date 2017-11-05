def create_id_mat(dim):
    """
    Create a dim x dim identity matrix
    Returns a nested list
    """
    return [[0 if row != col else 1 for col in range(dim)] for row in range(dim)]


def multiply_mats(mat1, mat2):
    """
    Multiply mat1 by mat2
    Returns a nested list
    """
    assert len(mat1[0]) == len(mat2), "unsuitable dimensions"
    res_mat = list()
    for row in range(len(mat1)):
        new_row = list()
        for col in range(len(mat2[0])):
            new_entry = 0
            for num in range(len(mat2)):
                new_entry += mat1[row][num] * mat2[num][col]
            new_row.append(new_entry)
        res_mat.append(new_row)
    return res_mat


def get_power_mat(mat, power):
    """
    Raise matrix mat to the given power
    Returns a nested list
    """
    if power == 0:
        return create_id_mat(len(mat))
    res = mat[:]
    for _ in range(1, power):
        res = multiply_mats(res, mat)
    return res


def get_printable_mat(mat):
    """
    Make matrix mat readable
    Returns a string
    """
    res = ''
    for row in mat:
        res += (str(row) + '\n')
    return res


if __name__ == '__main__':
    # m1 = [[1, 0, 4],
    #       [2, 1, 1],
    #       [3, 1, 0],
    #       [0, 2, 2]]
    #
    # m2 = [[2, 4],
    #       [1, 1],
    #       [3, 0]]
    #
    # m_new = multiply_mats(m1, m2)
    # print get_printable_mat(m_new)
    #
    # m3 = [[1, 2], [3, 4]]
    # print get_printable_mat(m3)
    # m3_pow2_mech = multiply_mats(m3, m3)
    # print get_printable_mat(m3_pow2_mech)
    # m3_pow2_aut = get_power_mat(m3, 2)
    # print get_printable_mat(m3_pow2_aut)
    # m3_pow3_mech = multiply_mats(m3_pow2_mech, m3)
    # print get_printable_mat(m3_pow3_mech)
    # m3_pow3_aut = get_power_mat(m3, 3)
    # print get_printable_mat(m3_pow3_aut)
    # m3_pow4_mech = multiply_mats(m3_pow3_mech, m3)
    # print get_printable_mat(m3_pow4_mech)
    # m3_pow4_aut = get_power_mat(m3, 4)
    # print get_printable_mat(m3_pow4_aut)
    # m3_pow5_mech = multiply_mats(m3_pow4_mech, m3)
    # print get_printable_mat(m3_pow5_mech)
    # m3_pow5_aut = get_power_mat(m3, 5)
    # print get_printable_mat(m3_pow5_aut)
    # m3_pow6_mech = multiply_mats(m3_pow5_mech, m3)
    # print get_printable_mat(m3_pow6_mech)
    # m3_pow6_aut = get_power_mat(m3, 6)
    # print get_printable_mat(m3_pow6_aut)
    # m3_pow7_mech = multiply_mats(m3_pow6_mech, m3)
    # print get_printable_mat(m3_pow7_mech)
    # m3_pow7_aut = get_power_mat(m3, 7)
    # print get_printable_mat(m3_pow7_aut)
    # print
    # print get_printable_mat(get_power_mat(m3, 0))
    # print
    # print get_printable_mat(get_power_mat(m3, 1))
    pass


