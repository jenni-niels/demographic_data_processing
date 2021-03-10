import pandas as pd
import xarray as xr
import arviz as az
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def make_trace_plots(data_run, ei_run, convergence_stat, j):
    data_path = f"../outputs/{data_run}/{ei_run}"
    outfilePath = f"../analysis/figs/convergence/{data_run}/{ei_run}/"
    if not os.path.exists(outfilePath):
        os.makedirs(outfilePath)
    suffix = f"MD_{convergence_stat}_{j}.csv"

    df_list = []
    max_draw = 1000
    for i in range(1,5):
        df_i = pd.read_csv(f"{data_path}/{i}/{suffix}")
        df_i["chain"] = i
        df_i["draw"] = np.arange(len(df_i), dtype = int)
        df_list.append(df_i)

    df_concat = pd.concat(df_list)
    df = df_concat[df_concat["draw"]<max_draw].set_index(["chain", "draw"])
    xdata = xr.Dataset.from_dataframe(df)
    idata = az.InferenceData(posterior=xdata)

    for col in df.columns:
        try:
            az.plot_trace(idata, var_names=[col])
            plt.savefig(f"{outfilePath}{col}.png")
        except:
            print("Encountered an error...")
            continue

    return df
