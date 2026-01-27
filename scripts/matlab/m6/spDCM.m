clear
addpath('/scratch/fc37/leo/Toolboxes/spm12') % load latest spm12

%% define paths and parameters

% name of parcellation dir inside derivatives/parcellations
parc_dirname    = 'AAL'
% name of masks dir inside parcellation dir defined above
masks_dirname   = 'adam_m6'

% define paths and variables
dir_base        = fullfile('/','fs03','fc37','PsiConnect');
dir_bids        = fullfile(dir_base,'bids');
dir_deriv       = fullfile(dir_base,'derivatives');
dir_ts          = fullfile(dir_deriv,'timeseries',parc_dirname,masks_dirname); % time series
dir_DCM         = fullfile(dir_deriv,'spDCM',parc_dirname,masks_dirname);

tasks           = {'meditation','movie','music','rest'} %{'meditation','movie','music','rest'}
run_str         = '1';
pipeline        = 'tedanaGLM'

TR              = 0.91;      % repetition time
DCM_overwrite   = true;     % overwrite DCM file

batch_size      = feature('numcores') - 2; % n parallel processes (available CPUs - 2)

%% read BIDS folder to find all subjects, sessions, scans, etc
BIDS            = spm_BIDS(dir_bids);

%% DCM specification (loop over the rows of the BIDS.subjects table)
row_n       = length(BIDS.subjects);
tasks_n     = length(tasks);
GCM         = {};
for i_row = 1:row_n 
    % read subject name and session name
    subj       = BIDS.subjects(i_row).name;
    ses        = BIDS.subjects(i_row).session;

    for i_task = 1:tasks_n
        task            = tasks{i_task};
    
        % create subject-specific DCM folder if not already existing
        dir_out         = fullfile(dir_DCM,subj,ses);
        if ~exist(dir_out,'dir'); mkdir(dir_out); end
        
        DCM_name        = [subj,'_',ses,'_task-',task,'_run-',run_str,'_DCM.mat'];
        file_DCM        = fullfile(dir_out,DCM_name);
        if exist(file_DCM,'file')
            if DCM_overwrite
                % delete existing DCM file if DCM_overwrite = true
                delete(file_DCM)
            else
                % skip this task
                warning(['Skipped existing DCM: ',subj,' ',ses,' ',task])
                continue
            end
        end
        
        % load time series
        f_ts        = fullfile(dir_ts,subj,ses,['task-',task],...
            [subj,'_',ses,'_task-',task,'_run-',run_str,'_timeseries-',pipeline,'.mat']);
        if exist(f_ts,'file')
            load(fullfile(f_ts),'time_series','ROI_names');
        else
            warning(['Skipped due to missing time series file: ',subj,' ',ses,' ',task])
            continue
        end

        n           = size(time_series,2);	% number of ROIs
        v           = size(time_series,1);	% number of volumes
        DCM.Y.y     = time_series;
        DCM.name    = DCM_name;
        for i = 1:n
            DCM.xY(i).name = ROI_names{i};
        end
        DCM.v       = v;
        DCM.n       = n;    
        DCM.Y.name  = ROI_names;
        DCM.Y.dt    = TR; % repetition time
        DCM.Y.X0    = zeros(v,1);
        DCM.Y.Q     = spm_Ce(ones(1,n)*v);
        DCM.delays  = repmat(DCM.Y.dt,DCM.n,1); % delays
        DCM.U.u     = zeros(v,1);
        DCM.U.name  = {'null'};
        
        DCM.a       = ones(n,n);
        DCM.b       = zeros(n,n,0);
        DCM.c       = zeros(n,0);
        DCM.d       = zeros(n,n,0);
        
        DCM.options.stochastic  = 0;
        DCM.options.nonlinear   = 0;
        DCM.options.two_state   = 0;
        DCM.options.analysis    = 'CSD'; % cross spectral densities
        DCM.options.induced     = 1;
        DCM.options.maxnodes    = n; % number of modes
        DCM.options.maxit       = 256; % max number of iterations
        DCM.options.nograph     = 1; % turn off graphical display
        % DCM.options.order       = 8; % AR model order
        DCM.options.nmax        = n + 1;
        
        save(file_DCM,'DCM');
        GCM                     = vertcat(GCM,{file_DCM});
    end
end

disp(GCM) % show list of DCM files

%% DCM estimation
delete(gcp('nocreate')) % delete previous parpool if active

poolobj         = parpool(batch_size)
GCM_n           = length(GCM);
for i_batch = 1:batch_size:GCM_n
    tic
    parfor i_row = i_batch:min((i_batch + batch_size - 1),GCM_n)
        file_DCM = GCM{i_row};
        disp(['Estimating: ',file_DCM])
        spm_dcm_fmri_csd(file_DCM); 
    end          
    tEnd        = datenum(0,0,0,0,0,toc); % time since previous 'tic'
    fprintf('Elapsed time is %s\n', datestr(tEnd,'HH:MM:SS'))
end
delete(poolobj)