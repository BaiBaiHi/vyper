

def test_default_param_abi(get_contract):
    code = """
@public
@payable
def safeTransferFrom(_data: bytes[100] = "test", _b: int128 = 1):
    pass
    """
    abi = get_contract(code)._classic_contract.abi

    assert len(abi) == 4
    assert set([fdef['name'] for fdef in abi]) == {'safeTransferFrom'}
    assert abi[0]['inputs'] == []
    assert abi[1]['inputs'] == [{'type': 'int128', 'name': '_b'}]
    assert abi[2]['inputs'] == [{'type': 'bytes', 'name': '_data'}]
    assert abi[3]['inputs'] == [{'type': 'bytes', 'name': '_data'}, {'type': 'int128', 'name': '_b'}]


def test_basic_default_param_passthrough(get_contract):
    code = """
@public
def fooBar(_data: bytes[100] = "test", _b: int128 = 1) -> int128:
    return 12321
    """

    c = get_contract(code)

    assert c.fooBar() == 12321
    assert c.fooBar(2) == 12321
    assert c.fooBar(b"drum drum") == 12321
    assert c.fooBar(b"drum drum", 2) == 12321


def test_basic_default_param_set(get_contract):
    code = """
@public
def fooBar(a:int128, b: uint256 = 333) -> (int128, uint256):
    return a, b
    """

    c = get_contract(code)
    assert c.fooBar(456, 444) == [456, 444]
    assert c.fooBar(456) == [456, 333]


def test_basic_default_param_set_2args(get_contract):
    code = """
@public
def fooBar(a:int128, b: uint256 = 999, c: address = 0x0000000000000000000000000000000000000001) -> (int128, uint256, address):
    return a, b, c
    """

    c = get_contract(code)
    c_default_value = '0x0000000000000000000000000000000000000001'
    b_default_value = 999
    addr2 = '0x1000000000000000000000000000000000004321'

    # b default value, c default value
    assert c.fooBar(123) == [123, b_default_value, c_default_value]
    # c default_value, b set from param
    assert c.fooBar(456, 444) == [456, 444, c_default_value]
    # b default set, c set from param
    assert c.fooBar(555, addr2) == [555, b_default_value, addr2]
    # no default values
    assert c.fooBar(6789, 4567, addr2) == [6789, 4567, addr2]


def test_default_param_bytes(get_contract):
    code = """
@public
def fooBar(a: bytes[100], b: int128, c: bytes[100] = "testing", d: uint256 = 999) -> (bytes[100], int128, bytes[100], uint256):
    return a, b, c, d
    """
    c = get_contract(code)
    c_default = b"testing"
    d_default = 999

    # c set, d default value
    assert c.fooBar(b"booo", 12321, b'woo') == [b"booo", 12321, b'woo', d_default]
    # d set, c default value
    assert c.fooBar(b"booo", 12321, 888) == [b"booo", 12321, c_default, 888]
    # d set, c set
    assert c.fooBar(b"booo", 12321, b"lucky", 777) == [b"booo", 12321, b"lucky", 777]
    # no default values
    assert c.fooBar(b"booo", 12321) == [b"booo", 12321, c_default, d_default]
