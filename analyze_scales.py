import argparse
import pandas as pd

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
                      'CLOUDS_FMRIPATTERNS', 'CLOUDS_FMRIFACES', 'CLOUDS_FMRIOBJECTS']

df = pd.read_csv(src_file, sep="\t")  # Load the TSV file

df = df[scales_of_interest]

# clean data
df = df.dropna()  # Remove rows with NaN values

df.head



# %% plot the scales

def plot_scales(df, scales):
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set(style="whitegrid")
    
    for scale in scales:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[scale], kde=True, bins=30)
        plt.title(f'Distribution of {scale} Scores')
        plt.xlabel('Scores')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

def individual_box_whisker(df, scales):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

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


plot_scales(df, scales_of_interest)

individual_box_whisker(df, scales_of_interest)

# plot based on the individual scores

# Compute the mean and standard deviation for 'ASC5_AUDITORY'
threshold = df['ASC5_AUDITORY'].mean() + 1 * df['ASC5_AUDITORY'].std()

# Filter the dataframe to include only rows with 'ASC5_AUDITORY' values above the threshold
df_skinny = df[df['ASC5_AUDITORY'] > threshold]

print(df_skinny.index.tolist())
individual_box_whisker(df_skinny, scales_of_interest)

individual_box_whisker(df[df['ASC5_AUDITORY'] < threshold], scales_of_interest)

# %%
