from nose.tools import assert_raises, with_setup
from os import remove
from os.path import exists

from pkglts.hash_management import compute_hash, modified_file_hash, pth_as_key


ex_file = 'toto.txt'


def teardown():
    if exists(ex_file):
        remove(ex_file)


def test_pth_as_key_produce_unique_path():
    pth1 = pth_as_key("./toto/titi/")
    pth2 = pth_as_key("toto/titi")
    pth3 = pth_as_key("./toto/../toto/titi")

    assert pth1 == pth2
    assert pth1 == pth3


def test_compute_hash():
    assert compute_hash("toto") == compute_hash("toto")
    assert compute_hash("toto") != compute_hash("titi")


@with_setup(teardown=teardown)
def test_modified_file_raise_error_if_file_not_in_hashmap():
    with open(ex_file, 'w') as f:
        f.write("lorem ipsum\n" * 10)

    assert_raises(IOError, lambda: modified_file_hash(ex_file, {}))


@with_setup(teardown=teardown)
def test_modified_file_detect_modifications_only_in_preserved_sections():
    with open(ex_file, 'w') as f:
        f.write("lorem ipsum\n" * 10)

    assert not modified_file_hash(ex_file, {ex_file: []})


@with_setup(teardown=teardown)
def test_modified_file_if_not_same_preserved_sections():
    txt = "lorem ipsum\n" * 10

    with open(ex_file, 'w') as f:
        f.write("{# pkglts, toto\n")
        f.write(txt)
        f.write("#}\n")

    assert modified_file_hash(ex_file, {ex_file: dict(titi="azerty")})


@with_setup(teardown=teardown)
def test_modified_file_detect_modifications_in_preserved_sections():
    txt = "lorem ipsum\n" * 10
    hv = compute_hash(txt)

    with open(ex_file, 'w') as f:
        f.write("{# pkglts, toto\n")
        f.write(txt)
        f.write("\n#}\n")

    assert not modified_file_hash(ex_file, {ex_file: dict(toto=hv)})

    with open(ex_file, 'w') as f:
        f.write("{# pkglts, toto\n")
        f.write(txt * 2)
        f.write("\n#}\n")

    assert modified_file_hash(ex_file, {ex_file: dict(toto=hv)})
