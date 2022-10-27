import os
import pathlib

import pineko
import pineko.configs
import pineko.theory
import pineko.theory_card

theory_obj = pineko.theory.TheoryBuilder(208, ["LHCB_Z_13TEV_DIMUON"])
theory_obj_hera = pineko.theory.TheoryBuilder(208, ["HERACOMBCCEM"])
theory_obj_test = pineko.theory.TheoryBuilder(208, ["HERACOMBCCEM"], silent=True)


def benchmark_operators_cards_path(test_files, test_configs):
    pineko.configs.configs = pineko.configs.defaults(test_configs)
    path = theory_obj.operator_cards_path
    assert path == pathlib.Path(test_files / "data/operator_cards/208/")


def benchmark_ekos_path(test_files):
    path = theory_obj.ekos_path()
    assert path == pathlib.Path(test_files / "data/ekos/208/")


def benchmark_fks_path(test_files):
    path = theory_obj.fks_path
    assert path == pathlib.Path(test_files / "data/fktables/208/")


def benchmark_grids_path(test_files):
    path = theory_obj.grids_path()
    assert path == pathlib.Path(test_files / "data/grids/208/")


def benchmark_load_grids(test_files):
    dataset_name = "LHCB_Z_13TEV_DIMUON"
    grids = theory_obj.load_grids(dataset_name)
    assert grids["LHCB_DY_13TEV_DIMUON"] == pathlib.Path(
        test_files / "data/grids/208/LHCB_DY_13TEV_DIMUON.pineappl.lz4"
    )


def benchmark_inherit_grid(tmp_path):
    from_grid = theory_obj.grids_path()
    theory_obj.inherit_grid("TestGrid", from_grid, tmp_path)


def benchmark_inherit_grids(test_files):
    new_theory_ID = 2081
    theory_obj.inherit_grids(new_theory_ID)
    folder_path = pathlib.Path(test_files / "data" / "grids" / str(new_theory_ID))
    assert folder_path.is_dir()
    assert (folder_path / "LHCB_DY_13TEV_DIMUON.pineappl.lz4").is_file()
    theory_obj.inherit_grids(new_theory_ID)
    for item in folder_path.iterdir():
        item.unlink()
    folder_path.rmdir()


def benchmark_inherit_eko(tmp_path):
    from_eko = theory_obj.ekos_path()
    theory_obj.inherit_eko("TestEko", from_eko, tmp_path)


def benchmark_inherit_ekos(test_files):
    new_theory_ID = 2081
    theory_obj.inherit_ekos(new_theory_ID)
    folder_path = pathlib.Path(test_files / "data" / "ekos" / str(new_theory_ID))
    assert folder_path.is_dir()
    assert (folder_path / "LHCB_DY_13TEV_DIMUON.tar").is_file()
    theory_obj.inherit_ekos(new_theory_ID)
    for item in folder_path.iterdir():
        item.unlink()
    folder_path.rmdir()


def benchmark_opcard(test_files, test_configs):
    th_path = pineko.theory_card.path(208)

    grid_name = "LHCB_DY_13TEV_DIMUON"
    theory_obj.opcard(
        grid_name,
        pathlib.Path(test_files / "data/grids/208/LHCB_DY_13TEV_DIMUON.pineappl.lz4"),
        1.0,
        th_path,
    )
    op_path = pathlib.Path(
        test_files / theory_obj.operator_cards_path / "LHCB_DY_13TEV_DIMUON.yaml"
    )
    theory_obj.opcard(
        grid_name,
        pathlib.Path(test_files / "data/grids/208/LHCB_DY_13TEV_DIMUON.pineappl.lz4"),
        1.0,
        th_path,
    )
    if os.path.exists(op_path):
        os.remove(op_path)
    else:
        raise ValueError("operator card not found")


def benchmark_eko(test_files, test_configs):
    th_path = pineko.theory_card.path(208)

    grid_name = "LHCB_DY_13TEV_DIMUON"
    grid_path = pathlib.Path(theory_obj.grids_path() / (grid_name + ".pineappl.lz4"))
    base_configs = pineko.configs.load(test_files)
    pineko.configs.configs = pineko.configs.defaults(base_configs)
    tcard = pineko.theory_card.load(208)
    theory_obj.activate_logging(
        pathlib.Path(test_files / "logs/eko/"),
        "208-LHCB_DY_13TEV_DIMUON.log",
        ["208-LHCB_DY_13TEV_DIMUON.log"],
    )
    theory_obj.opcard(grid_name, pathlib.Path(test_files / grid_path), 1.0, th_path)

    theory_obj.eko(grid_name, grid_path, tcard)

    log_path = pathlib.Path(test_files / "logs/eko/208-LHCB_DY_13TEV_DIMUON.log")
    if os.path.exists(log_path):
        os.remove(log_path)
    else:
        raise ValueError("log file not found")
    op_path = pathlib.Path(
        test_files / theory_obj.operator_cards_path / "LHCB_DY_13TEV_DIMUON.yaml"
    )
    if os.path.exists(op_path):
        os.remove(op_path)
    else:
        raise ValueError("operator card not found")


def benchmark_activate_logging(test_files):
    assert not theory_obj_test.activate_logging(
        pathlib.Path(test_files / "logs/fk/"), "test_log.log", ["test_log.log"]
    )
    theory_obj.activate_logging(
        pathlib.Path(test_files / "logs/fk/"), "test_log.log", ["test_log.log"]
    )
    log_path = pathlib.Path(test_files / "logs/fk/test_log.log")
    if os.path.exists(log_path):
        os.remove(log_path)
    else:
        raise ValueError("log file not found")


def benchmark_fk(test_files, test_configs):
    th_path = pineko.theory_card.path(208)

    grid_name = "HERA_CC_318GEV_EM_SIGMARED"
    grid_path = pathlib.Path(
        theory_obj_hera.grids_path() / (grid_name + ".pineappl.lz4")
    )
    base_configs = pineko.configs.load(test_files)
    pineko.configs.configs = pineko.configs.defaults(base_configs)
    tcard = pineko.theory_card.load(208)
    theory_obj_hera.activate_logging(
        pathlib.Path(test_files / "logs/fk/"),
        "208-HERA_CC_318GEV_EM_SIGMARED.log",
        ["208-HERA_CC_318GEV_EM_SIGMARED.log"],
    )
    theory_obj_hera.opcard(
        grid_name, pathlib.Path(test_files / grid_path), 1.0, th_path
    )

    theory_obj_hera.fk(grid_name, grid_path, tcard, pdf=None)
    # test overwrite function
    theory_obj_hera.fk(grid_name, grid_path, tcard, pdf=None)
    log_path = pathlib.Path(test_files / "logs/fk/208-HERA_CC_318GEV_EM_SIGMARED.log")
    if os.path.exists(log_path):
        os.remove(log_path)
    else:
        raise ValueError("log file not found")
    op_path = pathlib.Path(
        test_files
        / theory_obj_hera.operator_cards_path
        / "HERA_CC_318GEV_EM_SIGMARED.yaml"
    )
    if os.path.exists(op_path):
        os.remove(op_path)
    else:
        raise ValueError("operator card not found")

    fk_path = pathlib.Path(
        test_files
        / theory_obj_hera.fks_path
        / "HERA_CC_318GEV_EM_SIGMARED.pineappl.lz4"
    )
    if os.path.exists(fk_path):
        os.remove(fk_path)
    else:
        raise ValueError("fktable not found")
