import argparse
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#!/usr/bin/env python3
"""
This script analyzes and summarizes the data from scales available in phenotype_raw_data.
Example usage (using the ses-02_raw file and analyzing the "dasc" scale):

    python analyze_scales.py /path/to/ses-02_raw.csv --scales dasc

# scales of interest
    - 'ASC5_AUDITORY', 'ASC5_RESTRUCTURE', 'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'
    - 'CLOUDS_FMRIPATTERNS', 'CLOUDS_FMRIFACES', 'CLOUDS_FMRIOBJECTS'

# analyses to do:
- distribution of the scores for each scale
    
    """


#%% setup data
# decide timepoint
src_file = "C:\\Users\\aman0087\\Documents\\massive_output_local\\phenotype\\bids\\ses-02\\ses-02.tsv"  # Change this to your actual file name

# scales of interest
scales_of_interest = ['ASC5_AUDITORY', 'ASC5_RESTRUCTURE', 'ASC11_AUDIOVISUAL', 'ASC11_COMPLEX', 'ASC11_ELEMENTARY', 'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY',
                      'CLOUDS_FMRIPATTERNS', 'CLOUDS_FMRIFACES', 'CLOUDS_FMRIOBJECTS', 'MEQ30_MEAN', 
                      'ASC11_COGNITION', 'ASC11_ANXIETY']

df_full = pd.read_csv(src_file, sep="\t")  # Load the TSV file

df = df_full[scales_of_interest]

# default data file and scales of interest (can be overridden via CLI)
SRC_FILE_DEFAULT = "C:\\Users\\aman0087\\Documents\\massive_output_local\\phenotype\\bids\\ses-02\\ses-02.tsv"

# scales of interest
SCALES_OF_INTEREST = ['ASC5_AUDITORY', 'ASC5_RESTRUCTURE', 'ASC11_AUDIOVISUAL', 'ASC11_COMPLEX', 'ASC11_ELEMENTARY', 'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY',
                      'CLOUDS_FMRIPATTERNS', 'CLOUDS_FMRIFACES', 'CLOUDS_FMRIOBJECTS', 'MEQ30_MEAN']


def load_and_prepare(src_file=SRC_FILE_DEFAULT, scales=None):
    """Load TSV and return dataframe with selected scales (dropping missing columns/rows).

    Returns the dataframe and the list of scales actually present.
    """
    if scales is None:
        scales = SCALES_OF_INTEREST
    df_full = pd.read_csv(src_file, sep="\t")  # Load the TSV file
    # keep only scales present in the file
    present = [s for s in scales if s in df_full.columns]
    missing = [s for s in scales if s not in df_full.columns]
    if missing:
        print(f'Warning: the following requested scales are missing from {src_file}: {missing}')
    df = df_full[present].copy()
    df = df.dropna()
    return df, present


def plot_scales(df, scales):

    # Plot the boxplot with lower opacity
    sns.boxplot(data=df[scales], boxprops=dict(alpha=0.3), medianprops=dict(color='black'), whiskerprops=dict(alpha=0.3), capprops=dict(alpha=0.3), flierprops=dict(markerfacecolor='gray', alpha=0.2))
    
    # Overlay each participant's scores as a line with a color gradient
    x = np.arange(len(scales))
    n_participants = len(df)
    cmap = plt.get_cmap('viridis')
    colors = [cmap(i / max(n_participants - 1, 1)) for i in range(n_participants)]
    for i in range(n_participants):
        plt.plot(x, df.iloc[i][scales], marker='o', color=colors[i], alpha=0.7, linewidth=1)

    plt.title('Individual Participant Scores with Box and Whisker Plot')
    plt.xlabel('Scales')
    plt.ylabel('Scores')
    plt.xticks(ticks=x, labels=scales, rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def plot_extremes_by_scale(df, scale='ASC5_AUDITORY', n_std=1, scales_to_plot=None):
    """Plot participants with values above/below a threshold for a chosen scale."""
    if scale not in df.columns:
        raise ValueError(f'{scale} not in dataframe')
    threshold = df[scale].mean() + n_std * df[scale].std()
    df_high = df[df[scale] > threshold]
    df_low = df[df[scale] < threshold]
    print('High indices:', df_high.index.tolist())
    if scales_to_plot is None:
        scales_to_plot = df.columns.tolist()
    if len(df_high) > 0:
        individual_box_whisker(df_high, scales_to_plot)
    if len(df_low) > 0:
        individual_box_whisker(df_low, scales_to_plot)

# %%
# test interaction between scales
from scipy import stats
from itertools import combinations
# avoid heavy dependencies: implement BH correction and LOOCV without statsmodels/sklearn


def pairwise_correlations(df, method='pearson'):
    """Compute pairwise correlations and p-values for all columns in df.

    Returns:
        corr_df: DataFrame of correlation coefficients
        pval_df: DataFrame of two-sided p-values
    """
    cols = df.columns.tolist()
    n = len(cols)
    corr = pd.DataFrame(np.zeros((n, n)), index=cols, columns=cols)
    pvals = pd.DataFrame(np.ones((n, n)), index=cols, columns=cols)

    for i, j in combinations(range(n), 2):
        x = df.iloc[:, i]
        y = df.iloc[:, j]
        if method == 'pearson':
            r, p = stats.pearsonr(x, y)
        elif method == 'spearman':
            r, p = stats.spearmanr(x, y)
        else:
            raise ValueError('method must be pearson or spearman')
        corr.iat[i, j] = r
        corr.iat[j, i] = r
        pvals.iat[i, j] = p
        pvals.iat[j, i] = p

    np.fill_diagonal(corr.values, 1.0)
    np.fill_diagonal(pvals.values, 0.0)
    return corr, pvals


def predictive_association(df, target_col):
    """Assess predictive association of each column to target_col using LOOCV linear regression.

    Returns:
        r2_series: Series of cross-validated R^2 (can be negative) for each predictor
        pvals_series: Series of p-values from simple linear regression fit (not CV)
    """
    predictors = [c for c in df.columns if c != target_col]
    n_samples = df.shape[0]
    y = df[target_col].values

    r2s = {}
    pvals = {}
    for i, col in enumerate(predictors):
        Xcol = df[col].values
        y_true = y
        preds = np.zeros_like(y_true, dtype=float)
        # manual LOOCV
        for test_idx in range(n_samples):
            train_idx = [k for k in range(n_samples) if k != test_idx]
            x_train = Xcol[train_idx]
            y_train = y_true[train_idx]
            # fit simple linear regression on training data
            slope, intercept, r_val, p_val_train, std_err = stats.linregress(x_train, y_train)
            preds[test_idx] = intercept + slope * Xcol[test_idx]
        # compute R^2 for CV predictions
        ss_res = np.sum((y_true - preds) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot != 0 else np.nan
        r2s[col] = r2

    # for p-value, use OLS on full data (simple regression)
    slope, intercept, r_value, p_value, std_err = stats.linregress(Xcol, y_true)
    pvals[col] = p_value

    r2_series = pd.Series(r2s)
    pvals_series = pd.Series(pvals)
    return r2_series, pvals_series


def bh_correction(pvals_df, alpha=0.05):
    """Apply Benjamini-Hochberg FDR correction to a DataFrame of p-values.

    Returns a boolean DataFrame of the same shape indicating significance, and an array of adjusted p-values
    (in the order of the non-NaN flattened p-values).
    """
    flat = pvals_df.values.flatten()
    mask_nan = np.isnan(flat)
    p = flat[~mask_nan]
    m = len(p)
    if m == 0:
        sig = np.zeros_like(flat, dtype=bool).reshape(pvals_df.shape)
        return pd.DataFrame(sig, index=pvals_df.index, columns=pvals_df.columns), np.array([])

    # sort p-values and keep original order
    order = np.argsort(p)
    p_sorted = p[order]
    # BH procedure: find largest k such that p_(k) <= (k/m) * alpha
    thresholds = (np.arange(1, m + 1) / m) * alpha
    below = p_sorted <= thresholds
    if not np.any(below):
        reject = np.zeros(m, dtype=bool)
    else:
        max_k = np.max(np.where(below)[0])  # zero-based index
        reject_sorted = np.zeros(m, dtype=bool)
        reject_sorted[: max_k + 1] = True
        # unsort
        reject = np.zeros(m, dtype=bool)
        reject[order] = reject_sorted

    # compute adjusted p-values (standard BH adjusted)
    p_adj = np.empty(m, dtype=float)
    # p_adj(k) = min_{l>=k} (m / l) * p_(l)
    tmp = (m / np.arange(1, m + 1)) * p_sorted
    # enforce monotonicity from the end
    tmp_rev = tmp[::-1]
    cummin_rev = np.minimum.accumulate(tmp_rev)
    p_adj_sorted = cummin_rev[::-1]
    # put back in original order
    p_adj[order] = p_adj_sorted

    corrected = np.zeros_like(flat, dtype=bool)
    corrected[~mask_nan] = reject
    sig = corrected.reshape(pvals_df.shape)
    return pd.DataFrame(sig, index=pvals_df.index, columns=pvals_df.columns), p_adj


def plot_correlation_heatmap(corr_df, pvals_df, sig_df=None, title='Correlation matrix', out_file=None, cmap='vlag'):
    """Plot a heatmap of correlations with significance marks.

    If sig_df is provided (bool DataFrame same shape), overlay asterisks for significance.
    """
    plt.figure(figsize=(max(8, corr_df.shape[0] * 0.6), max(6, corr_df.shape[1] * 0.6)))
    sns.heatmap(corr_df, annot=True, fmt='.2f', cmap=cmap, center=0, square=True, cbar_kws={'shrink': .8})
    plt.title(title)
    if sig_df is not None:
        # overlay text for significance
        for i in range(corr_df.shape[0]):
            for j in range(corr_df.shape[1]):
                if i == j:
                    continue
                if sig_df.iat[i, j]:
                    plt.text(j + 0.5, i + 0.5, '*', color='white', ha='center', va='center', fontsize=14)
    plt.tight_layout()
    if out_file:
        plt.savefig(out_file)
    plt.show()


def run_pairwise_analysis(df, method='pearson', fdr_alpha=0.05, out_prefix='scales_correlation'):
    """Run pairwise correlation analysis and plot heatmap files.

    Returns: dict with corr, pvals, sig
    """
    corr_df, pvals_df = pairwise_correlations(df, method=method)
    sig_df, corrected_flat = bh_correction(pvals_df, alpha=fdr_alpha)
    plot_correlation_heatmap(corr_df, pvals_df, sig_df, title=f'{method.title()} correlations', out_file=f'{out_prefix}_{method}.png')
    return {'corr': corr_df, 'pvals': pvals_df, 'sig': sig_df}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze scale interactions (correlations and predictive associations).')
    parser.add_argument('--scales', nargs='+', default=scales_of_interest, help='List of scales to analyze')
    parser.add_argument('--method', choices=['pearson', 'spearman'], default='pearson')
    parser.add_argument('--fdr-alpha', type=float, default=0.05)
    parser.add_argument('--out-prefix', type=str, default='scales_correlation')

    parser.add_argument('--src-file', type=str, default=SRC_FILE_DEFAULT, help='Path to TSV file with scales')
    parser.add_argument('--do-plots', action='store_true', help='Also run exploratory plots (histograms, boxplots)')
    args = parser.parse_args()

    df_all, present_scales = load_and_prepare(src_file=args.src_file, scales=args.scales)
    scales = [s for s in args.scales if s in present_scales]
    if len(scales) < 2:
        raise SystemExit('Need at least two scales to analyze')

    df_sub = df_all[scales].dropna()
    print(f'Running pairwise analysis on {len(df_sub)} subjects and {len(scales)} scales')
    results = run_pairwise_analysis(df_sub, method=args.method, fdr_alpha=args.fdr_alpha, out_prefix=args.out_prefix)

    if args.do_plots:
        # exploratory plots
        plot_scales(df_sub, scales)
        individual_box_whisker(df_sub, scales)


def individual_box_whisker(df, scales):
    """Box-and-whisker plot with individual participant lines overlaid."""
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    # Plot the boxplot with lower opacity
    sns.boxplot(data=df[scales], boxprops=dict(alpha=0.3), medianprops=dict(color='black'), whiskerprops=dict(alpha=0.3), capprops=dict(alpha=0.3), flierprops=dict(markerfacecolor='gray', alpha=0.2))
    # Overlay each participant's scores as a line with a color gradient
    x = np.arange(len(scales))
    n_participants = len(df)
    cmap = plt.get_cmap('viridis')
    colors = [cmap(i / max(n_participants - 1, 1)) for i in range(n_participants)]
    for i in range(n_participants):
        plt.plot(x, df.iloc[i][scales], marker='o', color=colors[i], alpha=0.7, linewidth=1)
    plt.title('Individual Participant Scores with Box and Whisker Plot')
    plt.xlabel('Scales')
    plt.ylabel('Scores')
    plt.xticks(ticks=x, labels=scales, rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def example_run():
    """Quick example: load default file, run pairwise correlations and save heatmap.

    Usage: call analyze_scales.example_run() from Python, or run the script with
    --src-file and optionally --scales and --do-plots.
    """
    df_all, present = load_and_prepare()
    if len(present) < 2:
        print('Not enough scales present in default file')
        return
    df_sub = df_all[present].dropna()
    run_pairwise_analysis(df_sub, out_prefix='example_scales')



