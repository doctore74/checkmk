import pytest  # type: ignore
from pathlib2 import Path
import cmk_base.ip_lookup as ip_lookup


@pytest.fixture()
def _cache_file():
    p = Path(ip_lookup._cache_path())
    p.parent.mkdir(parents=True, exist_ok=True)  # pylint: disable=no-member

    yield p

    if p.exists():
        p.unlink()


def test_initialize_ip_lookup_cache_not_existing(_cache_file):
    if _cache_file.exists():
        _cache_file.unlink()

    ip_lookup_cache = ip_lookup._initialize_ip_lookup_cache()

    assert ip_lookup_cache == {}


def test_initialize_ip_lookup_cache_invalid_syntax(_cache_file):
    with _cache_file.open(mode="w", encoding="utf-8") as f:
        f.write(u"{...")

    ip_lookup_cache = ip_lookup._initialize_ip_lookup_cache()

    assert ip_lookup_cache == {}


def test_initialize_ip_lookup_cache_existing(_cache_file):
    cache_id1 = "host1", 4
    with _cache_file.open(mode="w", encoding="utf-8") as f:
        f.write(u"%r" % {cache_id1: "1"})

    ip_lookup_cache = ip_lookup._initialize_ip_lookup_cache()

    assert ip_lookup_cache == {cache_id1: "1"}


def test_update_ip_lookup_cache_empty_file(_cache_file):
    cache_id = "host1", 4
    ip_lookup._update_ip_lookup_cache(cache_id, "127.0.0.1")

    cache = ip_lookup._load_ip_lookup_cache(lock=False)
    assert cache[cache_id] == "127.0.0.1"

    cache = ip_lookup._load_ip_lookup_cache(lock=False)
    assert cache[cache_id] == "127.0.0.1"


def test_update_ip_lookup_cache_extend_existing_file(_cache_file):
    cache_id1 = "host1", 4
    cache_id2 = "host2", 4

    ip_lookup._update_ip_lookup_cache(cache_id1, "127.0.0.1")
    ip_lookup._update_ip_lookup_cache(cache_id2, "127.0.0.2")

    cache = ip_lookup._load_ip_lookup_cache(lock=False)
    assert cache[cache_id1] == "127.0.0.1"
    assert cache[cache_id2] == "127.0.0.2"


def test_update_ip_lookup_cache_update_existing_entry(_cache_file):
    cache_id1 = "host1", 4
    cache_id2 = "host2", 4

    with _cache_file.open(mode="w", encoding="utf-8") as f:
        f.write(u"%r" % {cache_id1: "1", cache_id2: "2"})

    ip_lookup._update_ip_lookup_cache(cache_id1, "127.0.0.1")

    cache = ip_lookup._load_ip_lookup_cache(lock=False)
    assert cache[cache_id1] == "127.0.0.1"
    assert cache[cache_id2] == "2"


def test_load_legacy_lookup_cache(_cache_file):
    cache_id1 = "host1", 4
    cache_id2 = "host2", 4

    with _cache_file.open("w", encoding="utf-8") as f:
        f.write(u"%r" % {"host1": "127.0.0.1", "host2": "127.0.0.2"})

    cache = ip_lookup._load_ip_lookup_cache(lock=False)
    assert cache[cache_id1] == "127.0.0.1"
    assert cache[cache_id2] == "127.0.0.2"
