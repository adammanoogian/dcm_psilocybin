#!/bin/bash
#SBATCH --job-name=peb_batch
#SBATCH --output=peb_batch_%j.log
#SBATCH --error=peb_batch_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=20:00:00

module load matlab/r2022a

echo "Starting MATLAB PEB batch job at $(date)"

# 1a: Change, movie
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-01', 'ses-02'}, {'task-movie'}, 'change', {}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 1b: Change, music
matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-01', 'ses-02'}, {'task-music'}, 'change', {}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 1c: Change, rest
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-01', 'ses-02'}, {'task-rest'}, 'change', {}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 1d: Change, meditation
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-01', 'ses-02'}, {'task-meditation'}, 'change', {}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 2a: Contrast, rest vs. movie
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-rest', 'task-movie'}, 'contrast', {}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 2b: Contrast, rest vs. music
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-rest', 'task-music'}, 'contrast', {}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 2c: Contrast, music vs. movie
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-music', 'task-movie'}, 'contrast', {}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 3a: Behavioral association, music, 5D-ASC "audio"
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-music'}, 'behav_associations', {'ASC5_AUDITORY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 3b: Behavioral association, movie, 5D-ASC "visual"
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-movie'}, 'behav_associations', {'ASC5_RESTRUCTURE'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 4a: Behavioral association, music, 11D-ASC composite
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-music'}, 'behav_associations', {'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 4b: Behavioral association, movie, 11D-ASC composite
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-movie'}, 'behav_associations', {'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 5a: Behavioral association, movie, clouds scale
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-movie'}, 'behav_associations', {'CLOUDS_FMRIPATTERNS', 'CLOUDS_FMRIFACES', 'CLOUDS_FMRIOBJECTS'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 6a: Behavioral association, rest, 5D-ASC "auditory"
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-rest'}, 'behav_associations', {'ASC5_AUDITORY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 6b: Behavioral association, rest, 5D-ASC "visual"
#  matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-rest'}, 'behav_associations', {'ASC5_RESTRUCTURE'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 6c: Behavioral association, rest, 11D-ASC composite
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-rest'}, 'behav_associations', {'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 7a: Behavioral associations (constrained A), rest, 11D-ASC composite
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-rest'}, 'behav_associations', {'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 7b: Behavioral associations (constrained A), movie, 11D_ASC composite
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-movie'}, 'behav_associations', {'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 7c: Behavioral associations (constrained A), music, 11D_ASC composite
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-music'}, 'behav_associations', {'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &

# 7d: Behavioral associations (constrained A), meditation, 11D_ASC composite
# matlab -nodisplay -nosplash -r "try, PEB_run_bash({'ses-02'}, {'task-meditation'}, 'behav_associations', {'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'}), catch ex, disp(getReport(ex)), exit(1), end, exit" &


wait

echo "Finished at $(date)"