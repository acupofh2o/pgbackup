import pytest

from pgbackup import cli

url = "postgres://admin:admin@localhost:5432//db_one"

@pytest.fixture
def parser():
    return cli.create_parser()


def test_parser_without_driver(parser):
    """
    Without a specified driver the parser will exit
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url])

def test_parser_without_destination(parser):
    """
    The parser will exit if no destination is provided
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "local"])


def test_parser_with_driver_and_destination(parser):
    """
    The Parser will not exit if it gets a driver and a destination
    """
    args = parser.parse_args([url, "--driver", "local", "/path"])
    assert args.driver == "local"
    assert args.destination == "/path"

def test_parser_with_unkown_driver(parser):
    """
    Parser will exit if you pass in an unknown driver
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "azure", "destination"])

def test_parser_with_known_drivers(parser):
    """
    Parser will not exit if you pass in a known driver.
    """
    for driver in ["local", "s3"]:
        assert parser.parse_args([url, "--driver", driver, "destination"])
