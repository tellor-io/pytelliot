"""
Unit tests covering telliot config options.
"""
import os
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from telliot.apps.config import ConfigFile
from telliot.apps.config import ConfigOptions


@dataclass
class SubConfig(ConfigOptions):
    option_c: str = "abc"


@dataclass
class MyOptions(ConfigOptions):
    option_a: int = 1
    option_b: SubConfig = field(default_factory=SubConfig)


def main(config_format):
    """Test default configs"""

    # Make sure that config file does not exist
    tmpdir = Path("./temp").resolve().absolute()
    config_file = tmpdir / f"myconfig.{config_format}"
    config_file_bak = config_file.with_suffix(".bak")
    if config_file.exists():
        os.remove(config_file)
    if config_file_bak.exists():
        os.remove(config_file_bak)

    # Create folder if it doesn't exist
    tmpdir.mkdir(parents=True, exist_ok=True)

    # Make sure starting with clean folder
    assert not config_file.exists()
    assert not config_file_bak.exists()

    cf = ConfigFile(
        name="myconfig",
        config_type=MyOptions,
        config_dir=tmpdir,
        config_format=config_format,
    )

    # Make sure default was created and verify default value
    assert cf.config_file.exists()
    options = cf.get_config()
    assert options.option_a == 1

    # Make a change to the config and save it
    options.option_a = 3
    cf.save_config(options)
    assert config_file_bak.exists()

    # Create a new config object from the existing file.  Verify new values
    cf2 = ConfigFile(
        name="myconfig",
        config_type=MyOptions,
        config_dir=tmpdir,
        config_format=config_format,
    )
    op2 = cf2.get_config()
    assert op2.option_a == 3

    # Cleanup
    os.remove(config_file)
    os.remove(config_file_bak)


def test_yaml():
    """Test YAML format"""
    main("yaml")


def test_json():
    """Test JSON format"""
    main("json")
