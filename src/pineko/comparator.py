import io
import subprocess

import numpy as np
import pandas as pd


def build_data_frame(full_output):
    """
    Parse a Rust table into a `pd.DataFrame`.

    Parameters
    ----------
        full_output : str
            console output

    Returns
    -------
        df : pd.DataFrame
            data frame
    """
    # split by lines
    output = full_output.splitlines()
    stream = io.StringIO()
    # determine columns
    columns = [[e.strip(), e.strip() + "_2"] for e in output[2].split()[1:]]
    columns = ["bin"] + [f for e in columns for f in e] + ["pine", "fk", "reldiff"]
    # get rid of all the white space
    for line in output[4:-2]:
        stream.write(" ".join([e.strip() for e in line.split()]) + "\n")
    # setup dataframe
    stream.seek(0)
    return pd.read_table(stream, names=columns, sep=" ")


def compare(pineappl_path, fktable_path, pdf):
    """
    Print comparison table via `pineappl diff`.

    Parameters
    ----------
        pineappl_path : str
            uncovoluted grid
        fktable_path : str
            convoluted grid
        pdf : str
            PDF set name
    """
    # get the output
    comparison = subprocess.run(
        [
            "pineappl",
            "diff",
            "--ignore_orders",
            str(pineappl_path),
            str(fktable_path),
            pdf,
        ],
        capture_output=True,
    )
    # parse to data frame
    df = build_data_frame(comparison.stdout.decode())
    df.set_index("bin", inplace=True)
    # remove bins' upper edges when bins are trivial
    obs_labels = np.unique(
        [lab for lab in filter(lambda lab: "_" in lab and "my" not in lab, df.columns)]
    )
    df.drop(obs_labels, axis=1, inplace=True)
    # print("\n".join(output))
    return df
