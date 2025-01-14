#!/usr/bin/env python
from numpy.ma.core import shape
import pytest
import numpy as np
import trx_file_memmap.trx_file_memmap as tmm

from tempfile import mkdtemp
import os.path as path


@pytest.mark.parametrize(
    "arr,expected,value_error",
    [
        (np.ones((5, 5, 5), dtype=np.int16), None, True),
        (np.ones((5, 4), dtype=np.int16), "mean_fa.4.int16", False),
        (np.ones((5, 4), dtype=np.float64), "mean_fa.4.float64", False),
        (np.ones((5, 1), dtype=np.float64), "mean_fa.float64", False),
        (np.ones((1), dtype=np.float64), "mean_fa.float64", False),
    ],
)
def test__generate_filename_from_data(
    arr, expected, value_error, filename="mean_fa.bit"
):

    if value_error:
        with pytest.raises(ValueError):
            new_fn = tmm._generate_filename_from_data(arr=arr, filename=filename)
            assert new_fn is None
    else:
        new_fn = tmm._generate_filename_from_data(arr=arr, filename=filename)
        assert new_fn == expected


@pytest.mark.parametrize(
    "filename,expected,value_error",
    [
        ("mean_fa.float64", ("mean_fa", 1, ".float64"), False),
        ("mean_fa.5.int32", ("mean_fa", 5, ".int32"), False),
        ("mean_fa", None, True),
        ("mean_fa.5.4.int32", None, True),
        pytest.param(
            "mean_fa.fa", None, True, marks=pytest.mark.xfail, id="invalid extension"
        ),
    ],
)
def test__split_ext_with_dimensionality(filename, expected, value_error):
    if value_error:
        with pytest.raises(ValueError):
            assert tmm._split_ext_with_dimensionality(filename) == expected
    else:
        assert tmm._split_ext_with_dimensionality(filename) == expected


@pytest.mark.parametrize(
    "offsets,nb_vertices,expected",
    [
        (np.array(range(5), dtype=np.int16), 4, np.array([1, 1, 1, 1, 0])),
        (np.array([0, 1, 0, 3, 4], dtype=np.int16), 4, np.array([1, 3, 0, 1, 0])),
        (np.array(range(4), dtype=np.int16), 4, np.array([1, 1, 1, 1])),
    ],
)
def test__compute_lengths(offsets, nb_vertices, expected):

    lengths = tmm._compute_lengths(offsets=offsets, nb_vertices=nb_vertices)
    assert np.array_equal(lengths, expected)


@pytest.mark.parametrize(
    "ext,expected",
    [
        (".bit", True),
        (".int16", True),
        (".float32", True),
        (".ushort", True),
        (".txt", False),
    ],
)
def test__is_dtype_valid(ext, expected):
    assert tmm._is_dtype_valid(ext) == expected


@pytest.mark.parametrize(
    "arr,l_bound,r_bound,expected",
    [
        (np.array(range(5), dtype=np.int16), None, None, 4),
        (np.array([0, 1, 0, 3, 4], dtype=np.int16), None, None, 1),
        (np.array([0, 1, 2, 0, 4], dtype=np.int16), None, None, 2),
        (np.array(range(5), dtype=np.int16), 1, 2, 2),
        (np.array(range(5), dtype=np.int16), 3, 3, 3),
        (np.zeros((5), dtype=np.int16), 3, 3, -1),
    ],
)
def test__dichotomic_search(arr, l_bound, r_bound, expected):
    end_idx = tmm._dichotomic_search(arr, l_bound=l_bound, r_bound=r_bound)
    assert end_idx == expected


@pytest.mark.parametrize(
    "basename, create, expected",
    [
        ("offsets.int16", True, np.array(range(12), dtype=np.int16).reshape((3, 4))),
        ("offsets.float32", False, None),
    ],
)
def test__create_memmap(basename, create, expected):
    if create:
        # Need to create array before evaluating
        filename = path.join(mkdtemp(), basename)
        fp = np.memmap(filename, dtype=np.int16, mode="w+", shape=(3, 4))
        fp[:] = expected[:]
        mmarr = tmm._create_memmap(filename=filename, shape=(3, 4), dtype=np.int16)
        assert np.array_equal(mmarr, expected)

    else:
        mmarr = tmm._create_memmap(filename=basename, shape=(0,), dtype=np.int16)
        assert path.isfile(basename)
        assert np.array_equal(mmarr, np.zeros(shape=(0,), dtype=np.float32))


# need dpg test with missing keys
@pytest.mark.parametrize(
    "path,check_dpg,value_error",
    [
        ("trx_file_memmap/tests/data/small_compressed.trx", False, False),
        ("trx_file_memmap/tests/data/small.trx", True, False),
        ("trx_file_memmap/tests/data/small_fldr.trx", False, False),
        ("trx_file_memmap/tests/data/dontexist.trx", False, True),
    ],
)
def test__load(path, check_dpg, value_error):

    # Need to perhaps improve test
    if value_error:
        with pytest.raises(ValueError):
            assert not isinstance(
                tmm.load(input_obj=path, check_dpg=check_dpg), tmm.TrxFile
            )
    else:
        assert isinstance(tmm.load(input_obj=path, check_dpg=check_dpg), tmm.TrxFile)


@pytest.mark.parametrize(
    "path",
    [
        ("trx_file_memmap/tests/data/small.trx"),
    ],
)
def test_load_zip(path):
    assert isinstance(tmm.load_from_zip(path), tmm.TrxFile)


@pytest.mark.parametrize("path", [("trx_file_memmap/tests/data/small_fldr.trx")])
def test_load_directory(path):
    assert isinstance(tmm.load_from_directory(path), tmm.TrxFile)


def test_concatenate():
    pass


def test_save():
    pass


def test_zip_from_folder():
    pass


def test_trxfile_init():
    pass


def test_trxfile_print():
    pass


def test_trxfile_len():
    pass


def test_trxfile_getitem():
    pass


def test_trxfile_deepcopy():
    pass


def test_get_real_len():
    pass


def test_copy_fixed_arrays_from():
    pass


def test_initialize_empty_trx():
    pass


def test_create_trx_from_pointer():
    pass


def test_trxfile_resize():
    pass


def test_trxfile_append():
    pass


def test_trxfile_getgroup():
    pass


def test_trxfile_select():
    pass


def test_trxfile_to_memory():
    pass


def test_trxfile_close():
    pass
