from utils.auth import hash_password, verify_password


def test_hash_and_verify():
    p = 'senha123'
    h = hash_password(p)
    assert verify_password(p, h)
    assert not verify_password('outra', h)
