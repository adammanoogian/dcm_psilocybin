function PEB_run_bash(ses_string, task_string, PEB_type, other_covariates)
% PEB_run_bash - Run PEB analysis with input parameters.
% ses_string:str e.g. 'ses-02'
% task_string:str e.g. 'task-movie'
% PEB_type:str e.g. 'behav_associations'
% other_covariates:cell array, e.g. {'age','sex'}

if nargin < 4
    error('All input parameters (ses_string, task_string, PEB_type, other_covariates) must be provided.');
end


%%
%copied from leo folder 20/05/25
%atm 20/05/25 changed PEB save directory naming to be dynamic
%atm 21/05/25 - added function to remove NaN covariates, rearranged M setup
%atm 25/05/25 - copied from peb_run.m to make bash compatible version


%% settings and paths
%addpath('/scratch/fc37/leo/Toolboxes/spm12') % replace with your spm12 dir
addpath('/fs04/fc37/adam/toolboxes/spm12')
addpath('/fs04/fc37/adam/scripts/utils/') %not finding my match_subjects.m at the moment
%addpath('/fs04/fc37/leo/psiconnect/scripts')

% Set up directories
parc            = 'AAL'; % parcellation dir inside derivatives/parcellations
masks_dirname   = 'adam_m6'; % masks dir inside parcellation dir
dir_base        = fullfile('/','scratch','fc37','PsiConnect');
dir_bids        = fullfile(dir_base,'bids');
dir_deriv       = fullfile(dir_base,'derivatives');
dir_phenotype   = fullfile(dir_base,'phenotype');
dir_DCM         = fullfile(dir_deriv,'spDCM',parc,masks_dirname);
dir_PEB         = fullfile(dir_deriv,'PEB',parc,masks_dirname);

% Validate ses_string and task_string inputs
if ischar(ses_string), ses_string = {ses_string}; end
if ischar(task_string), task_string = {task_string}; end

% Specify criteria for each group, e.g. group{1}, group{2}, etc.
group = {};
idx = 1;
for i_ses = 1:numel(ses_string)
    for i_task = 1:numel(task_string)
        group{idx} = {'sub-PC*', ses_string{i_ses}, task_string{i_task}, 'DCM.mat'};
        idx = idx + 1;
    end
end

% Only keep participants that appear in all groups?
match_subjects  = true;

% Exclude any subjects? Either {} or cell array: {'sub-PC001','sub-PC202'}

%adding on pc215 because not found in scales? 
exclude_subjects= {'sub-PC003','sub-PC005','sub-PC007','sub-PC010',...
                   'sub-PC022','sub-PC202','sub-PC230','sub-PC232',...
                   'sub-PC215'};

% Choose PEB analysis type from the following options:
% 'groupmean'          : only 1 group provided, compute mean effective connectivity
% 'change'             : use group 1 as baseline and compute change, e.g. in longitudinal studies
% 'contrast'           : use mean of both groups as baseline, compute deviation from baseline due to group difference (positive=group2>group1)
% 'behav_associations' : all groups will be merged, compute linear associations with other covariates (see below)
% see https://en.wikibooks.org/wiki/SPM/Parametric_Empirical_Bayes_(PEB)#Example_design_matrices
% PEB_type        = 'behav_associations';

% Other covariates in addition to change or contrast, e.g. age, sex, or
% behavioural measures. The code will look for these values in the 
% participants.tsv file (in BIDS folder) and in the "phenotype" folder.
% Each covariate must match a column in one of those spreadsheets.
% The first column of each spreadsheet must be named "participant_id".
% Check that all columns indicating sessions/tasks etc have the same name
% across all spreadsheets (e.g. all session columns are named "ses")
% other_covariates = {'ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY'}; % either {} or a cell array, e.g. {'sex','age','fd_mean'}
% other_covariates = {'none'}
ses_string_filename = strjoin(ses_string, '-');
task_string_filename = strjoin(task_string, '-');
cov_string = strjoin(other_covariates, '_');

% Output file name (it will be saved in dir_PEB defined above)
%PEB_filename    = ['PEB' '_' PEB_type '_' 'ses-' ses_string '_' task_string '_' 'cov-' cov_string '_noFD'];
%PEB_filename = sprintf('PEB_%s_-%s_-%s_cov-%s_noFD', PEB_type, ses_string_filename, task_string_filename, cov_string);
% if using A-constrained
PEB_filename = sprintf('PEB_%s_-%s_-%s_cov-%s_Aconstrained_noFD', PEB_type, ses_string_filename, task_string_filename, cov_string);
%PEB_filename    = 'PEB_beh_task-movie_noFD_cov_';
PEB_overwrite   = true; % true=overwrite existing file with the same name

% Choose which DCM parameters to estimate at the group level. The most
% frequent choice is the full effective connectivity matrix: {'A'}.
% One can also select specific connections, e.g. {'A(1,1)','A(1,3)'},
% e.g. to only test the connections that changed between two groups for
% behavioural associations as a second analysis.
%field           = {'A'};
%field           = {'A(1,2)','A(1,6)','A(2,2)','A(5,2)','A(5,5)','A(6,1)','A(6,5)','A(6,6)'};

%f_PEB_constraint = '/scratch/fc37/PsiConnect/derivatives/PEB/AAL/adam_m2/PEB_change_ses-ses-01-ses-02_task-task-music_cov-_noFD.mat';
f_PEB_constraint = '/scratch/fc37/PsiConnect/derivatives/PEB/AAL/adam_m6/PEB_change_-ses-01-ses-02_-task-meditation_cov-_noFD.mat';
field = utils_get_constrained_A(f_PEB_constraint);

% Specify PEB covariance model. The 'all' option means the between-subject
% variability of each connection will be estimated individually 
M.Q             = 'all'; % 'single' or 'all' (much slower)

% Also save individual DCMs updated using empirical priors? (This produces
% a very large result file)
individual_DCMs = false;

%% check if the number of groups is as expected
groups_n        = length(group);
fprintf('You defined %i groups \n',groups_n)
for i_g = 1:groups_n
    fprintf('Group %i criteria: \n',i_g)
    disp(group{i_g})
end

% throw error if 'change' but only one group
if (strcmp(PEB_type,'change') && (numel(group) < 2))
    error(['You have selected "change" but only specified ' ...
        'one group. Please provide two ses_string/task_string values.'])
end

% throw error if 'contrast' analysis but < 2 groups
if strcmp(PEB_type,'contrast') && (numel(task_string) < 2)
    error(['You have selected "contrast" but only specified ' ...
        'one group. Please provide two task_string values.'])
end

% throw error if 'groupmean' analysis but > 1 group
if strcmp(PEB_type,'groupmean') && (numel(group) > 1)
    error('You have selected "groupmean" with more than one group')
end

% throw warning if 'behav_associations' analysis but > 1 group
if strcmp(PEB_type,'behav_associations') && (numel(group) > 1)
    warning('You have selected "behav_associations" with more than one group')
end

%% find DCM files matching criteria
% initialise tables of DCM files split by group
GCM_tb          = cell(groups_n,1);

% find matching files for each group
for i_g = 1:groups_n
    filt        = strjoin([{''},group{i_g},{''}],'*'); % start/end with *
    filt        = strrep(filt,'**','*'); % replace ** with *
    
    temp        = dir(fullfile(dir_DCM,['**/',filt])); % recursive search
    match_n     = length(temp); % number of matching files

    fprintf('%i files matched filter for group %i: %s \n',match_n,i_g,filt)
    %disp(GCM_tb{i_g}) % show list of files

    if match_n == 0
        error('No files meeting criteria for group %i',i_g)
    end

    % split DCM file paths into columns (participant_id,ses,task,run)
    GCM_tb{i_g}     = split({temp.name}','_');
    % ignore last field, e.g. '_DCM'
    new_vars        = split(GCM_tb{i_g}(:,1:end-1),'-');
    new_vars        = new_vars(1,:,1);
    GCM_tb{i_g}     = cell2table(GCM_tb{i_g}(:,1:end-1),'VariableNames',new_vars);
    GCM_tb{i_g}     = renamevars(GCM_tb{i_g},'sub','participant_id');
    GCM_tb{i_g}.Path= fullfile({temp.folder}',{temp.name}'); % full paths
end
clear filt temp match_n new_vars i_g

%% only keep participants that appear in all groups (if requested)
% Only works if file names follow the BIDS conventions
if match_subjects && groups_n > 1
    if isfile('match_subjects_across_groups.m')
        GCM_tb = match_subjects_across_groups(GCM_tb);
    else
        error('File "match_subjects_across_groups.m" not found in current dir or MATLAB path')
    end
    % check that there is at least one participant in common across groups
    if isempty(GCM_tb)
        error('No common subjects across groups. Review groups or set match_subjects=false')
    end
end

%% exclude participants (if requested)
% Only works if file names follow the BIDS conventions
if ~isempty(exclude_subjects)
    for i_g = 1:groups_n
        fprintf('Excluding the following subjects from group %i: \n',i_g)
        disp(exclude_subjects)
        disp('Group before excluding participants:')
        disp(GCM_tb{i_g})
        % find indices of participants to exclude (row numbers)
        idx_exclude = ismember(GCM_tb{i_g}.participant_id,exclude_subjects);
        if ~isempty(idx_exclude)
            % delete rows from table
            GCM_tb{i_g}(idx_exclude,:) = [];
            disp('Group after excluding participants:')
            disp(GCM_tb{i_g})
        else
            warning('None of the participants to exclude were present')
        end
        if isempty(GCM_tb{i_g})
            error('After excluding participants, group %i is empty',i_g)
        end
    end
end
clear idx_exclude i_g

%% get list of DCM file paths after participant matching and exclusions
GCM                 = vertcat(GCM_tb{:}).Path;

%% Inspect quality of DCM fit across participants
DCM_check           = spm_dcm_fmri_check(GCM);

% Display variance explained for each scan as a table
tab_var             = vertcat(GCM_tb{:});
tab_var.Path        = [];
tab_var.run         = [];
tab_var.variance_explained = cellfun(@(x) x.diagnostics(1), DCM_check);
disp(tab_var)

% look for other covariates in all TSV files within the bids/phenotype (sub)folder(s)
if ~isempty(other_covariates)
    disp(['Attempting to find requested covariates in all the tsv files' ...
        ' within the "phenotype" folder (and its subfolders)'])
    clear phen
    f_part              = fullfile(dir_bids,'participants.tsv');
    fprintf('Loading file: %s \n',f_part)
    phen.participants   = struct2table(spm_load(f_part));
    
    % load phenotype assessment spreadsheets (.tsv) from dir_phenotype
    % The first column of each spreadsheet must be named "participant_id".
    % Check that all columns indicating sessions/tasks etc have the same name
    % across spreadsheets
    f                   = spm_select('FPListRec',dir_phenotype,'.*\.tsv$');
    if isempty(f), f = {}; else; f = cellstr(f); end
    for i=1:numel(f)
        fprintf('Loading file: %s \n',f{i})
        f_name          = spm_file(f{i},'basename');
        % Replace dashes, white spaces, and parentheses with an underscore
        f_name          = regexprep(f_name, '[-\s]', '_');
        try
            table_new   = struct2table(spm_load(f{i}));
            % convert text to numbers unless the column contains only text
            for i_col = 1:width(table_new)
                temp_col = table_new.(i_col);
                if ~isnumeric(temp_col)
                    temp_col = str2double(temp_col);
                    if ~all(isnan(temp_col))
                        table_new.(i_col) = temp_col;
                    end
                end
            end
            % store new table in phenotype structure
            phen.(f_name)   = table_new;
        catch
            warning('Could not load TSV file: %s', f{i})
        end
    end
    
    % join participants.tsv with all the phenotype tables in dir_phenotype
    disp('Behavioural covariate(s) requested:')
    disp(other_covariates)
    joined          = table();
    phen_tables     = fieldnames(phen);
    for i_sh = 1:length(phen_tables)
        tb_name     = phen_tables{i_sh};
        tb          = phen.(tb_name);
        tb_fields   = tb.Properties.VariableNames;
        found       = intersect(tb_fields,other_covariates);
        % remove participants from excluded list
        if ~isempty(exclude_subjects)
            idx_exclude = ismember(tb.participant_id,exclude_subjects);
            tb(idx_exclude,:) = [];
        end
        if ~isempty(found) && ~isempty(tb)
            fprintf('Covariate(s) found in "%s" spreadsheet:\n', tb_name)
            disp(found(:))
            if isempty(joined)
                joined      = tb;
            else
                temp = tb;
                joined      = outerjoin(joined,tb,'MergeKeys',true);
                % rename joined column
                column_names= joined.Properties.VariableNames;
                joined.Properties.VariableNames = erase(column_names,'_joined');
            end
        end
    end
    column_names    = joined.Properties.VariableNames;


    cloud_covs = {'CLOUDS_FMRIPATTERNS', 'CLOUDS_FMRIFACES', 'CLOUDS_FMRIOBJECTS'};
    if all(ismember(cloud_covs, column_names)) && any(ismember(other_covariates, cloud_covs))
        disp('Combining CLOUDS_FMRIPATTERNS, CLOUDS_FMRIFACES, CLOUDS_FMRIOBJECTS into CLOUDS_COMPOSITE');
        joined.CLOUDS_COMPOSITE = mean(table2array(joined(:,cloud_covs)), 2, 'omitnan');
        % Remove the original covariates from joined and other_covariates
        joined(:,cloud_covs) = [];
        other_covariates(ismember(other_covariates, cloud_covs)) = [];
        % Add the composite covariate to other_covariates if not already present
        if ~ismember('CLOUDS_COMPOSITE', other_covariates)
            other_covariates{end+1} = 'CLOUDS_COMPOSITE';
        end
        % Update column_names
        column_names = joined.Properties.VariableNames;
    end


    % Check that all covariates have been found in at least one spreadsheet
    disp('Summary')
    disp('Covariate(s) found:')
    cov_found       = intersect(column_names,other_covariates);
    disp(cov_found)
    % check if any covariates are missing
    cov_missing     = setdiff(other_covariates,column_names);
    if ~isempty(cov_missing)
        warning('Covariate(s) not found:')
        disp(cov_missing)
        error('Covariate(s) not found')
    end
        
    % inner join and keep track of original row positions in first table
    GCM_cat                 = vertcat(GCM_tb{:});
    % erase 'sub-' prefix in case it is omitted from some TSV files
    GCM_cat.participant_id  = erase(GCM_cat.participant_id,'sub-');
    joined.participant_id   = erase(joined.participant_id,'sub-');
    [joined, rows_in_temp]  = innerjoin(GCM_cat,joined);
    % sort rows in order to maintain the order in the first table
    [~, sortinds]           = sort(rows_in_temp);
    % apply this sort order to the new table
    joined                  = joined(sortinds,:);
    % only keep columns corresponding to requested covariates
    joined                  = joined(:,other_covariates);

    % Remove rows with NaN or empty values in any covariate
    [GCM_tb, GCM, joined] = utils_remove_nan_covariates(GCM_tb, GCM, joined);
    
    % Z-score covariates
    for i_cov = 1:width(joined)
        joined{:,i_cov} = utils_zscore_covariates(joined{:,i_cov});
    end
    
    if size(joined,1) < length(GCM)
        disp(joined)
        error('Could not find covariate values for each subject/session')
    elseif size(joined,1) > length(GCM)
        error(['Multiple values for the same covariate found across TSV files ' ...
            'without enough info to match it to a single subject and session. ' ...
            'Try adding a "ses" column to the TSV files if missing.'])
    end

end

%% Specify the design matrix M.X
N                   = length(GCM); % # files (rows of design matrix M.X)

% 1st covariate must be a column of ones
M.X                 = ones(N,1);

% the other covariates depend on the PEB type:
% if PEB type is 'change', use group assignments as covariates
if strcmp(PEB_type,'change')
    group_size = height(GCM_tb{1});
    for i_g = 2:groups_n
        M.X(group_size+1:group_size + height(GCM_tb{i_g}), i_g) = 1;
        group_size = group_size + height(GCM_tb{i_g});
    end
end
% if PEB type is 'contrast', use contrast with previous group
% (the mean will be sutracted later)
if strcmp(PEB_type,'contrast')
    group_size = height(GCM_tb{1});
    for i_g = 2:groups_n
        M.X(group_size-height(GCM_tb{i_g-1})+1 : group_size, i_g) = -1;
        M.X(group_size+1 : group_size+height(GCM_tb{i_g}), i_g) = 1;
        group_size = group_size + height(GCM_tb{i_g});
    end
end

if ~isempty(other_covariates)
    % add covariates as additional columns in the design matrix
    M.X(:,size(M.X,2)+1:size(M.X,2)+size(joined,2)) = table2array(joined);
end

disp('Design matrix:')
disp(M.X)

if any(isnan(M.X),"all") || any(isinf(M.X),"all")
    error("Design matrix contains non-numeric values (NaN or Inf).")
end
clear f_part phen f f_name joined phen_tables i_sh tb_name tb_fields found
clear cov_found cov_missing GCM_cat sortinds group_size i_g i_col temp_col
clear idx_exclude tb

%% subtract mean (where appropriate) and set covariate names
M.Xnames = {};
% if contrast or behav assoc, subtract mean from design matrix M.X
if strcmp(PEB_type,'groupmean')
    M.Xnames{1}     = 'mean of group 1';
elseif strcmp(PEB_type,'change')
    M.Xnames{1}     = 'mean of group 1';
    for i_g = 2:groups_n
        M.Xnames{i_g} = sprintf('change (group %i - group 1)',i_g);
    end
elseif strcmp(PEB_type,'contrast')
    % subtract mean of all columns except the first
    M.X(:,2:end)    = M.X(:,2:end) - mean(M.X(:,2:end));
    M.Xnames{1}     = 'mean of all groups combined';
    disp('Subtracted mean of all columns except the first')
    disp('Updated design matrix:')
    disp(M.X)
    for i_g = 2:groups_n
        M.Xnames{i_g} = sprintf('contrast (group %i - group %i)',i_g,i_g-1);
    end
elseif strcmp(PEB_type,'behav_associations')
    % subtract mean of all columns except the first
    M.X(:,2:end)    = M.X(:,2:end) - mean(M.X(:,2:end));
    disp('Subtracted mean of all columns except the first')
    disp('Updated design matrix:')
    disp(M.X)
    M.Xnames{1}     = 'mean of all groups combined';
else
    error('PEB type not recognised: %s',PEB_type)
end
clear i_g

% set names of additional covariates
M.Xnames            = [M.Xnames,other_covariates];

disp('List of all covariates:')
disp(M.Xnames')

% Visualise design matrix
figure('Name','Design matrix','Position',[600 100 300 800])
imagesc(M.X)
title('Design matrix (M.X)')
colormap('gray')
colorbar
xlabel('Covariates')
xticks(1:size(M.X,2))
ylabel('Participants')
yticks(unique(round(linspace(1, size(M.X,1), groups_n+1))))

%% load ROI_names from the first DCM
load(GCM{1},'DCM')
ROI_names           = DCM.Y.name;
disp('ROI names:')
disp(ROI_names)

%% check before continuing (popup dialog)
flag = false;
while flag
    answer = questdlg(['Check the command window: are the design matrix, ' ...
        'the list of covariates, and the ROI names as you expected?'], ...
	    'Would you like to continue?', ...
	    'Yes','No','Ask again in 10 seconds so I can scroll!','Yes');
    if strcmp(answer,'Yes')
        flag = false;
    elseif strcmp(answer,'No')
        error('Execution interrupted by user')
    else
        pause('on')
        pause(10)
    end
end
clear flag answer ans

%% Estimate and reduce PEB
disp('Running PEB...')

% If no write permission in current dir, change to home dir (the SPM12 PEB
% script needs permission to store a temporary file in the current dir)
if ~fileattrib('.','UserWrite')
    cd(getenv('HOME'))
end

% Estimate model
tic
if individual_DCMs
    disp('individual DCMs will be updated using empirical priors')
    [PEB,DCM_indiv] = spm_dcm_peb(GCM,M,field);
else
    PEB             = spm_dcm_peb(GCM,M,field);
end
toc

% Bayesian model reduction
disp('Running Bayesian model reduction...')
tic
BMA                 = spm_dcm_peb_bmc(PEB);
toc

%% save results

% create PEB dir if it doesn't exist
if ~isfolder(dir_PEB)
    mkdir(dir_PEB)
end

% attempt to save using the requested output file name
f_PEB           = fullfile(dir_PEB,[PEB_filename,'.mat']);

% if the file already exists and PEB_overwrite=false, add a timestamp 
if any(isfile(f_PEB)) && ~PEB_overwrite
    PEB_filename = [PEB_filename,'-',datestr(now,'YYYYmmddhhMMss')];
    f_PEB        = fullfile(dir_PEB,[PEB_filename,'.mat']);
    fprintf(['A PEB file with the same name already exists so a '...
        'timestamp was added to the file name: %s \n' ],f_PEB)
end
clear PEB_filename

% save entire workspace
save(f_PEB)
fprintf('PEB output saved in: %s \n',f_PEB)

%% Visualise PEB results

disp('Visualising results')

% before model reduction (using SPM12 GUI)
%spm_dcm_peb_review(PEB,GCM)

% after model reduction (using SPM12 GUI)
spm_dcm_peb_review(BMA,GCM)

% to visualise all covariates in one plot and reorder the ROIs, edit the 
% "PEB_plot_results.m" script and run it separately
