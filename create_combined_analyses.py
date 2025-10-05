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
from combine_plots import SVGCombiner

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
    
    # Initialize SVG combiner
    combiner = SVGCombiner(spacing=0, background_color='white')
    
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
    print("  - Panel 1: Mean of Group 1 (baseline)")
    print("  - Panel 2: Mean of Group 2 (post-intervention)")  
    print("  - Panel 3: Change Toward Zero")
    print("  - Panel 4: ASC11 Composite Behavioral Associations")
    print("=" * 80)
    
    # List available files for debugging
    list_available_files()
    
    # Create combined figures
    output_dir = create_condition_figures()
    
    print(f"\n✨ Process complete!")
    print(f"📂 Check the output directory: {output_dir}")
    print("\nExpected outputs:")
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