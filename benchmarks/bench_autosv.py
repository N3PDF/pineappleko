import shutil

import lhapdf
import numpy as np
import pineappl

from pineko import scale_variations


def benchmark_compute_ren_sv_grid(test_files, tmp_path, test_pdf, lhapdf_path):
    to_test_grid_path = (
        test_files
        / "data"
        / "grids"
        / "400"
        / "ATLAS_TTB_8TEV_LJ_TRAP_totest.pineappl.lz4"
    )
    name_grid = "ATLAS_TTB_8TEV_LJ_TRAP_norensv_fixed.pineappl.lz4"
    grid_path = test_files / "data" / "grids" / "400" / name_grid
    new_grid_path = tmp_path / name_grid
    shutil.copy(grid_path, new_grid_path)
    max_as = 2
    nf = 5
    pdf_name = "NNPDF40_nlo_as_01180"
    scale_variations.compute_ren_sv_grid(new_grid_path, max_as, nf)
    plusrensv_grid_path = (
        tmp_path / "ATLAS_TTB_8TEV_LJ_TRAP_norensv_fixed_plusrensv.pineappl.lz4"
    )
    with lhapdf_path(test_pdf):
        pdf = lhapdf.mkPDF(pdf_name)
    to_test_grid = pineappl.grid.Grid.read(to_test_grid_path)
    plusrensv_grid = pineappl.grid.Grid.read(plusrensv_grid_path)
    sv_list = [(0.5, 1.0), (2.0, 1.0)]  # Only ren sv have to be tested
    bin_number = to_test_grid.bins()
    to_test_res = to_test_grid.convolute_with_one(
        2212,
        pdf.xfxQ2,
        pdf.alphasQ2,
        np.array([], dtype=bool),
        np.array([], dtype=np.uint64),
        np.array([], dtype=bool),
        sv_list,
    ).reshape(bin_number, len(sv_list))
    plusrensv_res = plusrensv_grid.convolute_with_one(
        2212,
        pdf.xfxQ2,
        pdf.alphasQ2,
        np.array([], dtype=bool),
        np.array([], dtype=np.uint64),
        np.array([], dtype=bool),
        sv_list,
    ).reshape(bin_number, len(sv_list))
    rtol = 1.0e-14
    for sv in sv_list:
        for n_res, old_res in zip(
            to_test_res.transpose()[sv_list.index(sv)],
            plusrensv_res.transpose()[sv_list.index(sv)],
        ):
            np.testing.assert_allclose(n_res, old_res, rtol=rtol)
