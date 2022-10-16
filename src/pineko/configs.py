"""Tools related to the configuration file handling."""
import copy
import pathlib

import appdirs
import tomli

name = "pineko.toml"
"Name of the config file (wherever it is placed)"

# better to declare immediately the correct type
configs = {}
"Holds loaded configurations"


def defaults(base_configs):
    """Provide additional defaults.

    Parameters
    ----------
    base_config : dict
        user provided configuration

    Returns
    -------
    configs_ : dict
        enhanced configuration

    Note
    ----
    The general rule is to never replace user provided input.
    """
    configs_ = copy.deepcopy(base_configs)

    enhance_paths(configs_)

    return configs_


def enhance_paths(configs_):
    """Check required path and enhance them with root path.

    The changes are done inplace.

    Parameters
    ----------
    configs_ : dict
        configuration
    """
    # required keys without default
    for key in [
        "ymldb",
        "operator_cards",
        "grids",
        "operator_card_template",
        "theory_cards",
        "fktables",
        "ekos",
    ]:
        if key not in configs_["paths"]:
            raise ValueError(f"Configuration is missing a 'paths.{key}' key")
        if pathlib.Path(configs_["paths"][key]).anchor == "":
            configs_["paths"][key] = configs_["paths"]["root"] / configs_["paths"][key]
        else:
            configs_["paths"][key] = pathlib.Path(configs_["paths"][key])

    # optional keys which are by default None
    if "logs" not in configs_["paths"]:
        configs_["paths"]["logs"] = {}

    for key in ["eko", "fk"]:
        if key not in configs_["paths"]["logs"]:
            configs_["paths"]["logs"][key] = None
        elif pathlib.Path(configs_["paths"]["logs"][key]).anchor == "":
            configs_["paths"]["logs"][key] = (
                configs_["paths"]["root"] / configs_["paths"]["logs"][key]
            )
        else:
            configs_["paths"]["logs"][key] = pathlib.Path(
                configs_["paths"]["logs"][key]
            )


def detect(path=None):
    """Autodetect configuration file path.

    Parameters
    ----------
    path : str or os.PathLike
        user provided guess

    Returns
    -------
    pathlib.Path :
        file path
    """
    paths = []

    if path is not None:
        path = pathlib.Path(path)
        paths.append(path)

    paths.append(pathlib.Path.cwd())
    paths.append(pathlib.Path.home())
    paths.append(pathlib.Path(appdirs.user_config_dir()))
    paths.append(pathlib.Path(appdirs.site_config_dir()))

    for p in paths:
        configs_file = p / name if p.is_dir() else p

        if configs_file.is_file():
            return configs_file

    raise FileNotFoundError("No configurations file detected.")


def load(path=None):
    """Load config file.

    Parameters
    ----------
    path : str or os.PathLike
        file path

    Returns
    -------
    loaded : dict
        configuration dictionary
    """
    path = detect(path)

    with open(path, "rb") as fd:
        loaded = tomli.load(fd)

    if "paths" not in loaded:
        loaded["paths"] = {}
    if "root" not in loaded["paths"]:
        loaded["paths"]["root"] = pathlib.Path(path).parent

    return loaded
