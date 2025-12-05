#!/usr/bin/env python3
"""
Organize all connectivity figures with systematic naming following overleaf paper conventions.

Naming Convention:
- m1-c: Rest session change (ses02-ses01)
- m1-d: Rest behavioral covariate
- m2-c: Music session change
- m2-d: Music behavioral covariate
- etc.

New hypotheses: h01, h02, h03 (with letter variants for sub-variants)
"""

import shutil
from pathlib import Path

# Project root
project_root = Path(__file__).parent.parent.parent

# Define figure organization mapping
# Organization by EXPERIMENTAL CONDITION (following overleaf table)
# m1 = REST, m2 = MUSIC, m3 = MOVIE, m4 = MEDITATION
# Letter codes: a = session change, b = behavioral association, etc.

FIGURE_MAPPING = {
    # =========================================================================
    # M1: REST CONDITION
    # =========================================================================
    'm1_rest': {
        # M1-A: Rest Session Change (Post - Pre Psilocybin)
        'm1-a_change_full.png': 'nilearn/session_change_rest_full_network.png',
        'm1-a1_change_dlpfc.png': 'nilearn/session_change_rest_dlpfc_outgoing.png',
        'm1-a2_change_hippocampus.png': 'nilearn/session_change_rest_hippocampus.png',

        # M1-A: PEB Matrix Heatmaps (Session Change)
        'm1-a_matrix_pre.png': 'peb_matrices/m1-a_matrix_pre.png',
        'm1-a_matrix_post.png': 'peb_matrices/m1-a_matrix_post.png',
        'm1-a_matrix_change.png': 'peb_matrices/m1-a_matrix_change.png',

        # M1-B: Rest Behavioral Association (11D-ASC Composite)
        'm1-b_behavioral_asc11_full.png': 'nilearn/behav_rest_asc_sensory_full_network.png',
        'm1-b1_behavioral_asc11_hipp.png': 'nilearn/behav_rest_asc_sensory_hippocampus.png',

        # M1-B: PEB Matrix Heatmap (Behavioral 11D-ASC)
        'm1-b_matrix.png': 'peb_matrices/m1-b_matrix.png',

        # Additional: Rest ASC Auditory (optional/supplementary)
        'm1-c_behavioral_asc5_full.png': 'nilearn/behav_rest_asc_auditory_full_network.png',
        'm1-c1_behavioral_asc5_hipp.png': 'nilearn/behav_rest_asc_auditory_hippocampus.png',

        # M1-C: PEB Matrix Heatmap (Behavioral 5D-ASC)
        'm1-c_matrix.png': 'peb_matrices/m1-c_matrix.png',
    },

    # =========================================================================
    # M2: MUSIC CONDITION
    # =========================================================================
    'm2_music': {
        # M2-A: Music Session Change
        'm2-a_change_full.png': 'nilearn/session_change_music_full_network.png',
        'm2-a1_change_dlpfc.png': 'nilearn/session_change_music_dlpfc_outgoing.png',
        'm2-a2_change_hippocampus.png': 'nilearn/session_change_music_hippocampus.png',

        # M2-A: PEB Matrix Heatmaps (Session Change)
        'm2-a_matrix_pre.png': 'peb_matrices/m2-a_matrix_pre.png',
        'm2-a_matrix_post.png': 'peb_matrices/m2-a_matrix_post.png',
        'm2-a_matrix_change.png': 'peb_matrices/m2-a_matrix_change.png',

        # M2-B: Music Behavioral Association (11D-ASC Composite)
        'm2-b_behavioral_asc11_full.png': 'nilearn/behav_music_asc_sensory_full_network.png',
        'm2-b1_behavioral_asc11_hipp.png': 'nilearn/behav_music_asc_sensory_hippocampus.png',

        # M2-B: PEB Matrix Heatmap (Behavioral 11D-ASC)
        'm2-b_matrix.png': 'peb_matrices/m2-b_matrix.png',

        # Additional: Music ASC Auditory (optional/supplementary)
        'm2-c_behavioral_asc5_full.png': 'nilearn/behav_music_asc_auditory_full_network.png',
        'm2-c1_behavioral_asc5_hipp.png': 'nilearn/behav_music_asc_auditory_hippocampus.png',

        # M2-C: PEB Matrix Heatmap (Behavioral 5D-ASC)
        'm2-c_matrix.png': 'peb_matrices/m2-c_matrix.png',
    },

    # =========================================================================
    # M3: MOVIE CONDITION
    # =========================================================================
    'm3_movie': {
        # M3-A: Movie Session Change
        'm3-a_change_full.png': 'nilearn/session_change_movie_full_network.png',
        'm3-a1_change_dlpfc.png': 'nilearn/session_change_movie_dlpfc_outgoing.png',
        'm3-a2_change_hippocampus.png': 'nilearn/session_change_movie_hippocampus.png',

        # M3-A: PEB Matrix Heatmaps (Session Change)
        'm3-a_matrix_pre.png': 'peb_matrices/m3-a_matrix_pre.png',
        'm3-a_matrix_post.png': 'peb_matrices/m3-a_matrix_post.png',
        'm3-a_matrix_change.png': 'peb_matrices/m3-a_matrix_change.png',

        # M3-B: Movie Behavioral Association (11D-ASC Composite)
        'm3-b_behavioral_asc11_full.png': 'nilearn/behav_movie_asc_sensory_full_network.png',
        'm3-b1_behavioral_asc11_hipp.png': 'nilearn/behav_movie_asc_sensory_hippocampus.png',

        # M3-B: PEB Matrix Heatmap (Behavioral 11D-ASC)
        'm3-b_matrix.png': 'peb_matrices/m3-b_matrix.png',
    },

    # =========================================================================
    # M4: MEDITATION CONDITION
    # =========================================================================
    'm4_meditation': {
        # M4-A: Meditation Session Change
        'm4-a_change_full.png': 'nilearn/session_change_meditation_full_network.png',
        'm4-a1_change_dlpfc.png': 'nilearn/session_change_meditation_dlpfc_outgoing.png',
        'm4-a2_change_hippocampus.png': 'nilearn/session_change_meditation_hippocampus.png',

        # M4-A: PEB Matrix Heatmaps (Session Change)
        'm4-a_matrix_pre.png': 'peb_matrices/m4-a_matrix_pre.png',
        'm4-a_matrix_post.png': 'peb_matrices/m4-a_matrix_post.png',
        'm4-a_matrix_change.png': 'peb_matrices/m4-a_matrix_change.png',

        # M4-B: Meditation Behavioral Association (11D-ASC Composite)
        'm4-b_behavioral_asc11_full.png': 'nilearn/behav_meditation_asc_sensory_full_network.png',
        'm4-b1_behavioral_asc11_hipp.png': 'nilearn/behav_meditation_asc_sensory_hippocampus.png',

        # M4-B: PEB Matrix Heatmap (Behavioral 11D-ASC)
        'm4-b_matrix.png': 'peb_matrices/m4-b_matrix.png',
    },

    # =========================================================================
    # CONTRASTS (Commented out in overleaf, but available)
    # =========================================================================
    'contrasts': {
        'contrast_rest_vs_music.png': 'nilearn/contrast_rest_vs_music_full_network.png',
        'contrast_rest_vs_movie.png': 'nilearn/contrast_rest_vs_movie_full_network.png',
        'contrast_music_vs_movie.png': 'nilearn/contrast_music_vs_movie_full_network.png',
    },

    # =========================================================================
    # H01: MULTI-CONDITION COMPARISONS (New Hypotheses)
    # =========================================================================
    'h01_multi_condition': {
        # H01-A: All Tasks Session Change - Overlay
        'h01-a_all_tasks_overlay.png': 'nilearn/combined/overlay_all_tasks_session_change.png',

        # H01-B: All Tasks Session Change - Side-by-Side
        'h01-b_all_tasks_sidebyside.png': 'nilearn/combined/sidebyside_all_tasks_session_change.png',

        # H01-C: ASC Auditory (Rest vs Music) - Overlay
        'h01-c_auditory_rest_music_overlay.png': 'nilearn/combined/overlay_asc_auditory_rest_vs_music.png',

        # H01-D: ASC Auditory (Rest vs Music) - Side-by-Side
        'h01-d_auditory_rest_music_sidebyside.png': 'nilearn/combined/sidebyside_asc_auditory_rest_vs_music.png',

        # H01-E: ASC Sensory (All Tasks) - Overlay
        'h01-e_sensory_all_tasks_overlay.png': 'nilearn/combined/overlay_asc_sensory_all_tasks.png',

        # H01-F: ASC Sensory (All Tasks) - Side-by-Side
        'h01-f_sensory_all_tasks_sidebyside.png': 'nilearn/combined/sidebyside_asc_sensory_all_tasks.png',
    },

    # =========================================================================
    # H02: dlPFC OUTGOING CONNECTIONS (Hypothesis Panels)
    # =========================================================================
    'h02_dlpfc_outgoing': {
        # H02-A: Session Change (Rest/Music/Movie/Meditation)
        'h02-a_dlpfc_session_change.png': 'nilearn/hypotheses/h02-a_frontal_mid_session_change.png',

        # H02-B: Behavioral 11D-ASC (Rest/Music/Movie)
        'h02-b_dlpfc_behavioral.png': 'nilearn/hypotheses/h02-b_frontal_mid_behavioral.png',
    },

    # =========================================================================
    # H03: HIPPOCAMPUS CONNECTIONS (Hypothesis Panels)
    # =========================================================================
    'h03_hippocampus': {
        # H03-A: Session Change (Rest/Music/Movie/Meditation)
        'h03-a_hippocampus_session_change.png': 'nilearn/hypotheses/h03-a_hippocampus_session_change.png',

        # H03-B: Behavioral 11D-ASC (Rest/Music/Movie)
        'h03-b_hippocampus_behavioral.png': 'nilearn/hypotheses/h03-b_hippocampus_behavioral.png',
    },

    # =========================================================================
    # PEB MATRIX PANELS (2x2 Combined Panels)
    # =========================================================================
    'peb_matrix_panels': {
        # M1: REST 2x2 Panel (Pre, Post, Change, Behavioral)
        'm1_peb_panel_2x2.png': 'peb_matrices/panels/m1_peb_panel_2x2.png',
        'm1_peb_panel_2x2.pdf': 'peb_matrices/panels/m1_peb_panel_2x2.pdf',

        # M2: MUSIC 2x2 Panel
        'm2_peb_panel_2x2.png': 'peb_matrices/panels/m2_peb_panel_2x2.png',
        'm2_peb_panel_2x2.pdf': 'peb_matrices/panels/m2_peb_panel_2x2.pdf',

        # M3: MOVIE 2x2 Panel
        'm3_peb_panel_2x2.png': 'peb_matrices/panels/m3_peb_panel_2x2.png',
        'm3_peb_panel_2x2.pdf': 'peb_matrices/panels/m3_peb_panel_2x2.pdf',

        # M4: MEDITATION 2x2 Panel
        'm4_peb_panel_2x2.png': 'peb_matrices/panels/m4_peb_panel_2x2.png',
        'm4_peb_panel_2x2.pdf': 'peb_matrices/panels/m4_peb_panel_2x2.pdf',
    },
}


def organize_figures():
    """Organize all figures into structured folders with systematic naming."""

    figures_root = project_root / "figures"
    organized_root = figures_root / "organized"

    print("=" * 70)
    print("ORGANIZING CONNECTIVITY FIGURES")
    print("=" * 70)
    print(f"\nSource: {figures_root}")
    print(f"Destination: {organized_root}\n")

    stats = {'copied': 0, 'missing': 0, 'errors': 0}

    for category, file_mapping in FIGURE_MAPPING.items():
        category_dir = organized_root / category
        category_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*70}")
        print(f"Category: {category.upper().replace('_', ' ')}")
        print(f"{'='*70}")

        for new_name, source_path in file_mapping.items():
            source = figures_root / source_path
            dest = category_dir / new_name

            if source.exists():
                try:
                    shutil.copy2(source, dest)
                    print(f"  ✓ {new_name}")
                    print(f"    <- {source_path}")
                    stats['copied'] += 1
                except Exception as e:
                    print(f"  ✗ {new_name}: ERROR - {e}")
                    stats['errors'] += 1
            else:
                print(f"  ⚠ {new_name}: SOURCE NOT FOUND")
                print(f"    <- {source_path}")
                stats['missing'] += 1

    # Summary
    print("\n" + "=" * 70)
    print("ORGANIZATION COMPLETE")
    print("=" * 70)
    print(f"\nStatistics:")
    print(f"  ✓ Copied: {stats['copied']}")
    print(f"  ⚠ Missing: {stats['missing']}")
    print(f"  ✗ Errors: {stats['errors']}")
    print(f"\nOrganized figures location: {organized_root}")

    return stats


if __name__ == '__main__':
    organize_figures()
