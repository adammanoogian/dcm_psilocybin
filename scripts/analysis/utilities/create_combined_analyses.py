"""
Combined PEB Analysis Figures

Creates combined figure panels for each experimental condition by combining:
1. PEB change - mean of group 1
2. PEB change - mean of 2nd group
3. PEB change - change toward 0
4. ASC11 composite behavioral associations

One combined figure per condition: rest, movie, meditation, music
"""

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from combine_plots import SVGCombiner

def create_condition_figures_2x2():
    """
    Create combined figures for each experimental condition in a 2x2 grid layout.
    Each figure contains 4 panels arranged as:
        [Pre-Psilocybin]  [Post-Psilocybin]
        [Change]          [Behavioral]
    """

    # Base paths
    plots_dir = "C:/Users/aman0087/Documents/Github/dcm_psilocybin/plots"
    output_dir = "C:/Users/aman0087/Documents/Github/dcm_psilocybin/plots/combined_analyses"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define conditions and their corresponding file patterns
    conditions = ['rest', 'movie', 'meditation', 'music']

    for condition in conditions:
        print(f"\n📊 Creating 2x2 combined figure for: {condition.upper()}")
        print("-" * 50)

        # Define the 4 required PNG files for this condition (need to generate PNGs first)
        files_to_combine = [
            # 1. PEB change - mean of group 1 (Pre-Psilocybin)
            f"{plots_dir}/PEB_change_-ses-01-ses-02_-task-{condition}_cov-_noFD_mean_of_group_1.png",

            # 2. PEB change - mean of 2nd group (Post-Psilocybin)
            f"{plots_dir}/PEB_change_-ses-01-ses-02_-task-{condition}_cov-_noFD_mean_of_second_group.png",

            # 3. PEB change - change toward 0 (Change)
            f"{plots_dir}/PEB_change_-ses-01-ses-02_-task-{condition}_cov-_noFD_Change_toward_0.png",

            # 4. ASC11 composite behavioral associations (Behavioral)
            f"{plots_dir}/PEB_behav_associations_-ses-02_-task-{condition}_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD_ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY.png"
        ]

        # Check if all files exist
        missing_files = []
        existing_files = []

        for file_path in files_to_combine:
            if os.path.isfile(file_path):
                existing_files.append(file_path)
                filename = os.path.basename(file_path)
                print(f"  ✅ Found: {filename[:50]}...")
            else:
                missing_files.append(file_path)
                filename = os.path.basename(file_path)
                print(f"  ❌ Missing: {filename[:50]}...")

        # Create combined figure if we have all 4 files
        if len(existing_files) == 4:
            print(f"  🎯 All 4 files found - creating 2x2 grid figure")

            try:
                # Create 2x2 subplot grid with tight spacing
                fig, axes = plt.subplots(2, 2, figsize=(16, 16))

                # Remove all spacing between subplots
                plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01,
                                   wspace=0.02, hspace=0.02)

                # Load and display each image
                titles = ['Pre-Psilocybin', 'Post-Psilocybin', 'Change', 'Behavioral']
                positions = [(0, 0), (0, 1), (1, 0), (1, 1)]

                for i, (file_path, title, pos) in enumerate(zip(existing_files, titles, positions)):
                    img = mpimg.imread(file_path)
                    axes[pos].imshow(img)
                    axes[pos].axis('off')
                    # Remove the title since the individual plots already have titles
                    # axes[pos].set_title(title, fontsize=16, fontweight='bold', pad=5)

                # Save the combined figure
                output_path_png = os.path.join(output_dir, f"combined_PEB_analysis_{condition}_2x2.png")
                output_path_pdf = os.path.join(output_dir, f"combined_PEB_analysis_{condition}_2x2.pdf")

                fig.savefig(output_path_png, dpi=300, bbox_inches='tight', pad_inches=0.01)
                fig.savefig(output_path_pdf, bbox_inches='tight', pad_inches=0.01)
                plt.close(fig)

                print(f"  💾 Saved: combined_PEB_analysis_{condition}_2x2.png")
                print(f"  💾 Saved: combined_PEB_analysis_{condition}_2x2.pdf")

            except Exception as e:
                print(f"  ❌ Error creating combined figure: {str(e)}")
        else:
            print(f"  ⚠️  Only {len(existing_files)}/4 files found - skipping 2x2 grid")
            print(f"  ℹ️  Run plot_PEB_results.py first to generate individual plots")

    print(f"\n🎉 Combined 2x2 figures saved to: {output_dir}")
    return output_dir


def create_condition_figures():
    """
    Create combined figures for each experimental condition.
    Each figure contains 4 panels in horizontal layout.
    """

    # Base paths
    plots_dir = "C:/Users/aman0087/Documents/Github/dcm_psilocybin/plots"
    output_dir = "C:/Users/aman0087/Documents/Github/dcm_psilocybin/plots/combined_analyses"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize SVG combiner with negative spacing to overlap figures slightly
    # This eliminates white space between panels
    combiner = SVGCombiner(spacing=-180, background_color='white')

    # Define conditions and their corresponding file patterns
    conditions = ['rest', 'movie', 'meditation', 'music']

    for condition in conditions:
        print(f"\n📊 Creating combined figure for: {condition.upper()}")
        print("-" * 50)

        # Define the 4 required files for this condition
        files_to_combine = [
            # 1. PEB change - mean of group 1
            f"{plots_dir}/PEB_change_-ses-01-ses-02_-task-{condition}_cov-_noFD_mean_of_group_1.svg",

            # 2. PEB change - mean of 2nd group
            f"{plots_dir}/PEB_change_-ses-01-ses-02_-task-{condition}_cov-_noFD_mean_of_second_group.svg",

            # 3. PEB change - change toward 0
            f"{plots_dir}/PEB_change_-ses-01-ses-02_-task-{condition}_cov-_noFD_Change_toward_0.svg",

            # 4. ASC11 composite behavioral associations (constrained version)
            f"{plots_dir}/PEB_behav_associations_-ses-02_-task-{condition}_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD_ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY.svg"
        ]

        # Check if all files exist
        missing_files = []
        existing_files = []

        for file_path in files_to_combine:
            if os.path.isfile(file_path):
                existing_files.append(file_path)
                filename = os.path.basename(file_path)
                print(f"  ✅ Found: {filename}")
            else:
                missing_files.append(file_path)
                filename = os.path.basename(file_path)
                print(f"  ❌ Missing: {filename}")

        # Create combined figure if we have files
        if existing_files:
            output_path = os.path.join(output_dir, f"combined_PEB_analysis_{condition}.svg")

            if len(existing_files) == 4:
                print(f"  🎯 All 4 files found - creating complete figure")
            else:
                print(f"  ⚠️  Only {len(existing_files)}/4 files found - creating partial figure")

            try:
                combiner.combine_horizontal(
                    existing_files,
                    output_path,
                    align='center'
                )
                print(f"  💾 Saved: {os.path.basename(output_path)}")

            except Exception as e:
                print(f"  ❌ Error creating combined figure: {str(e)}")
        else:
            print(f"  ❌ No files found for {condition} - skipping")

    print(f"\n🎉 Combined figures saved to: {output_dir}")
    return output_dir

def convert_to_png(dpi=300):
    """
    Convert combined SVG files to PNG format using Inkscape CLI.
    
    Parameters:
    -----------
    dpi : int
        Resolution for PNG output (default: 300 for publication quality)
    """
    import subprocess
    
    output_dir = "C:/Users/aman0087/Documents/Github/dcm_psilocybin/plots/combined_analyses"
    conditions = ['rest', 'movie', 'meditation', 'music']
    
    print(f"\n🖼️  Converting SVG files to PNG (DPI: {dpi})")
    print("=" * 80)
    
    # Try to use Inkscape CLI
    try:
        # Test if Inkscape is available
        result = subprocess.run(['inkscape', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Using Inkscape CLI for conversion...")
            
            success_count = 0
            for condition in conditions:
                svg_file = os.path.join(output_dir, f"combined_PEB_analysis_{condition}.svg")
                png_file = os.path.join(output_dir, f"combined_PEB_analysis_{condition}.png")
                
                if os.path.exists(svg_file):
                    try:
                        print(f"  🔄 Converting {condition}.svg...")
                        result = subprocess.run([
                            'inkscape',
                            '--export-type=png',
                            f'--export-dpi={dpi}',
                            f'--export-filename={png_file}',
                            svg_file
                        ], check=True, capture_output=True, text=True, timeout=30)
                        
                        if os.path.exists(png_file):
                            file_size = os.path.getsize(png_file) / (1024 * 1024)  # MB
                            print(f"  ✅ {condition}.svg → {condition}.png ({file_size:.1f} MB)")
                            success_count += 1
                        else:
                            print(f"  ❌ Failed to create {condition}.png")
                    except subprocess.TimeoutExpired:
                        print(f"  ❌ Timeout converting {condition}")
                    except subprocess.CalledProcessError as e:
                        print(f"  ❌ Failed: {condition} - {e.stderr if e.stderr else 'unknown error'}")
                else:
                    print(f"  ⚠️  File not found: {condition}.svg")
            
            if success_count > 0:
                print(f"\n✨ Successfully converted {success_count}/{len(conditions)} files to PNG!")
                print(f"📂 PNG files saved to: {output_dir}")
                return True
            else:
                print(f"\n❌ No files were converted successfully")
                return False
    
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ Inkscape not found in PATH")
        print("\n📝 Manual conversion instructions:")
        print("\n  Option 1: Install Inkscape and add to PATH")
        print("    Download from: https://inkscape.org/")
        print("\n  Option 2: Run these commands manually:")
        for condition in conditions:
            svg_file = os.path.join(output_dir, f"combined_PEB_analysis_{condition}.svg")
            png_file = os.path.join(output_dir, f"combined_PEB_analysis_{condition}.png")
            print(f'    inkscape --export-type=png --export-dpi={dpi} --export-filename="{png_file}" "{svg_file}"')
        return False

def list_available_files():
    """
    List all available PEB plot files to help with debugging.
    """
    plots_dir = "C:/Users/aman0087/Documents/Github/dcm_psilocybin/plots"
    
    print("📁 Available PEB plot files:")
    print("=" * 80)
    
    if not os.path.exists(plots_dir):
        print(f"Plots directory not found: {plots_dir}")
        return
    
    # Group files by type
    change_files = []
    behav_files = []
    other_files = []
    
    for filename in sorted(os.listdir(plots_dir)):
        if filename.endswith('.svg'):
            if 'PEB_change' in filename:
                change_files.append(filename)
            elif 'PEB_behav_associations' in filename:
                behav_files.append(filename)
            else:
                other_files.append(filename)
    
    print(f"\n🔄 PEB Change Files ({len(change_files)}):")
    for f in change_files:
        print(f"  {f}")
    
    print(f"\n🧠 Behavioral Association Files ({len(behav_files)}):")
    for f in behav_files:
        print(f"  {f}")
    
    if other_files:
        print(f"\n📊 Other Files ({len(other_files)}):")
        for f in other_files:
            print(f"  {f}")

def main():
    """
    Main function to create combined analysis figures.
    """
    print("🚀 PEB Combined Analysis Figure Generator")
    print("=" * 80)
    print("Creating combined figures for each condition:")
    print("  - Panel 1: Pre-Psilocybin (baseline)")
    print("  - Panel 2: Post-Psilocybin (post-intervention)")
    print("  - Panel 3: Change")
    print("  - Panel 4: Behavioral Associations")
    print("=" * 80)

    # List available files for debugging
    list_available_files()

    # Create 2x2 grid combined figures (requires PNGs)
    print("\n" + "=" * 80)
    print("📊 Creating 2x2 Grid Layout Figures")
    print("=" * 80)
    output_dir = create_condition_figures_2x2()

    # Also create horizontal SVG combinations as backup
    print("\n" + "=" * 80)
    print("📊 Creating Horizontal SVG Combinations (backup)")
    print("=" * 80)
    create_condition_figures()

    # Convert SVGs to PNG
    convert_to_png(dpi=300)

    print(f"\n✨ Process complete!")
    print(f"📂 Check the output directory: {output_dir}")
    print("\nExpected outputs (2x2 grid):")
    print("  - combined_PEB_analysis_rest_2x2.png")
    print("  - combined_PEB_analysis_movie_2x2.png")
    print("  - combined_PEB_analysis_meditation_2x2.png")
    print("  - combined_PEB_analysis_music_2x2.png")

    print("\nExpected outputs (horizontal):")
    print("  - combined_PEB_analysis_rest.svg")
    print("  - combined_PEB_analysis_movie.svg")
    print("  - combined_PEB_analysis_meditation.svg")
    print("  - combined_PEB_analysis_music.svg")

    print("\n📄 To convert to PDF using Inkscape:")
    output_dir = "C:/Users/aman0087/Documents/Github/dcm_psilocybin/plots/combined_analyses"
    conditions = ['rest', 'movie', 'meditation', 'music']
    for condition in conditions:
        svg_file = f"{output_dir}/combined_PEB_analysis_{condition}.svg"
        pdf_file = f"{output_dir}/combined_PEB_analysis_{condition}.pdf"
        print(f'  inkscape --export-type=pdf --export-filename="{pdf_file}" "{svg_file}"')

if __name__ == "__main__":
    main()