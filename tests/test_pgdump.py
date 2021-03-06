import pytest
import subprocess

from pgbackup import pgdump

url = "postgres://admin:admin@localhost:5432/db_one"

def test_dump_calls_pg_dump(mocker):
    """
    Use pg_dump with the db url
    """
    mocker.patch('subprocess.Popen')
    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(["pg_dump", url], stdout=subprocess.PIPE)

def test_dump_handles_oserror(mocker):
    """
    pgdump.dump returns a reasonable error if pg_dump isn't installed.
    """
    mocker.patch('subprocess.Popen', side_effect=OSError("no such file"))
    with pytest.raises(SystemExit):
        pgdump.dump(url)

def test_dump_with_filename_without_timestamp():
    """
    pgdump.db_file_name returns the name of the database
    """
    assert pgdump.dump_with_filename(url) == "db_one.sql"

def test_dump_with_filename_with_timestamp():
    """
    pgdump.dump_with_filename returns the name of the database
    """
    timestamp = "2020-08-25T11:40:00"
    assert pgdump.dump_with_filename(url, timestamp) == "db_one-2020-08-25T11:40:00.sql"
