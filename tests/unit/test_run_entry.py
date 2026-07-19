"""Tests pour run.py — purge de crash.log."""


def test_trim_crash_log_truncates_large_file(tmp_path, monkeypatch):
    import run

    crash = tmp_path / "crash.log"
    content = b"a" * (run._CRASH_LOG_MAX_BYTES // 2) + b"b" * (run._CRASH_LOG_MAX_BYTES // 2 + 100)
    crash.write_bytes(content)
    monkeypatch.setattr(run, "_CRASH_LOG", crash)

    run._trim_crash_log()

    data = crash.read_bytes()
    assert len(data) == run._CRASH_LOG_MAX_BYTES // 2
    assert data == content[-run._CRASH_LOG_MAX_BYTES // 2:]


def test_trim_crash_log_keeps_small_file(tmp_path, monkeypatch):
    import run

    crash = tmp_path / "crash.log"
    crash.write_bytes(b"petit contenu")
    monkeypatch.setattr(run, "_CRASH_LOG", crash)

    run._trim_crash_log()

    assert crash.read_bytes() == b"petit contenu"


def test_trim_crash_log_missing_file_no_error(tmp_path, monkeypatch):
    import run

    monkeypatch.setattr(run, "_CRASH_LOG", tmp_path / "absent.log")

    run._trim_crash_log()
