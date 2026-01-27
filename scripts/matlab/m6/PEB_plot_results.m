function PEB_plot_results(f_PEB, verbose)
% PEB_plot_results - plot peb results (from a file or folder) and save the
% figure
% Usage:
% PEB_plot_results(f_PEB)
% f_PEB: path to a PEB .mat file or folder of
% verbose: if you want to display the plots right now (default = true)
%example usage: 
%PEB_plot_results("/scratch/fc37/PsiConnect/derivatives/PEB/AAL/adam_m6")
% copied from leo folder and modified to be function 02/06/25
% adjusted behav_associations str check 28/7/25
% changing heatmap key to normalised beta coefficients (for behav
% associations)

addpath('/fs04/fc37/adam/scripts/utils')

if nargin < 1 || isempty(f_PEB)
    % select PEB results file path
    %f_PEB        = "/scratch/fc37/PsiConnect/derivatives/PEB/AAL/adam_m2/PEB_change-ses1ses2_task-movie.mat";
    %f_PEB        = "/scratch/fc37/PsiConnect/derivatives/PEB/AAL/adam_m2/PEB_behav_associations_ses-ses-02_task-task-movie_cov-ASC5_RESTRUCTURE_noFD.mat"
    %f_PEB        = "/scratch/fc37/PsiConnect/derivatives/PEB/AAL/adam_m6/PEB_change_-ses-01-ses-02_-task-music_cov-_noFD.mat";
    %f_PEB        = "/scratch/fc37/PsiConnect/derivatives/PEB/AAL/adam_m2/PEB_behav_associations_ses-ses-02_task-task-music_cov-ASC5_AUDITORY_noFD.mat";
    %f_PEB       = "/scratch/fc37/PsiConnect/derivatives/PEB/AAL/adam_m6/PEB_behav_associations_-ses-02_-task-rest_cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat"

    verbose = true;
end

if isfolder(f_PEB)
    files = dir(fullfile(f_PEB, '*.mat'));
    for k = 1:numel(files)
        this_file = fullfile(files(k).folder, files(k).name);
        fprintf('Processing %s\n', this_file);
        PEB_plot_results(this_file);
    end
    return
end

% select model: currently it only works with "BMA" (after model reduction)
model        = "BMA";

% only show values whose posterior probability exceeds threshold
% (this only applies if model="BMA")
Pp_threshold = .99;
%Pp_threshold = 0.;

% to reorder the ROIs for plotting, define a permutation
% e.g., to switch 2<-->3 and 4<-->5, set ROI_reorder = [1,3,2,5,4];
ROI_reorder  = [];

% set font size for plots
font_size    = 12;

% revert diagonal element of effective connectivity to the same unit (Hz) 
% as the off-diagonal elements? To keep the self-connections negative, DCM 
% transforms the diagonal elements using a log function: log(-2x). 
% Historically, in the DCM literature, the diagonals are presented without 
% reverting this log transformation, which makes them hard to interpret. 
% I suggest reverting the log transformation to help you interpret the
% results. Then choose whether you want to publish them without reverting 
% for consistency with the literature. 
revert_diag = true;

%% read model
load(f_PEB)

if ~exist(model,"var")
    error("%s variable not loaded in the workspace",model)
end
model = eval(model);

% Ensure BMA and GCM variables are in the workspace
if ~exist("BMA", "var") || ~exist("GCM", "var")
    error("BMA or GCM data not found in the PEB file")
end
    
%% get ROI names from first DCM in the GCM cell array
if ~exist("ROI_names","var")
    if ~exist("GCM","var")
        error("GCM variable not loaded in the workspace")
    end
    ROI_names = get_ROI_names_from_GCM(GCM);
end

ROI_n         = length(ROI_names);

%% reshape model.Ep and model.Pp as (ROI_n,ROI_n,covariate_n)
model           = PEB_reshape_posterior(model,ROI_n);
cov_n           = size(model.M.X,2)

Ep              = model.Ep;
Pp              = model.Pp;

% set values below Pp threshold to zero
below_thr       = (Pp < Pp_threshold);
Ep(below_thr)   = 0;

% read covariate names
cov_names       = string(model.Xnames);

%% rescale diagonal if requested
% Applies g(y) = -exp(y)/2 to the elements on the diagonal of A.
% Assuming that the diagonal elements have been log-transformed by 
% f(x) = log(-2x), this function brings them back to the same unit (Hz) as
% the off-diagonal elements.

% if PEB type is "change" with 2 covariates (mean of group 1; and change)
if revert_diag && exist("PEB_type","var") && PEB_type=="change" && cov_n==2 
    % cov 1 (mean of group 1)
    A1                         = Ep(:,:,1);
    A1(logical(eye(size(A1)))) = -exp(diag(A1))/2;
    Ep(:,:,1)                  = A1;
    % cov 2 (change)
    A2                         = Ep(:,:,2);
    A2(logical(eye(size(A1)))) = exp(diag(A1))/2 - exp(diag(A1+A2))/2;
    Ep(:,:,2)                  = A2;
end
clear A1 A2

% if PEB type is "behav_assoc" or "groupmean"
if revert_diag && exist("PEB_type","var") && (PEB_type=="behav_associations" || PEB_type=="groupmean")
    for i_cov = 1:cov_n
        A                        = Ep(:,:,i_cov);
        A(logical(eye(size(A)))) = -exp(diag(A))/2;
        Ep(:,:,i_cov)            = A;
    end
end
clear A

%% plot the log transformation to help the interpretation
plot_log_transform = false;
if plot_log_transform == true
    fig             = figure;
    fig.NumberTitle = "off";
    fig.Name        = "y=-exp(x)/2";
    x               = -1:0.05:1;
    plot(x,-exp(x)/2,"DisplayName","Reverse transformation: -exp(x)/2")
    hold on
    scatter(0,-0.5,"DisplayName","Prior expectation (real value = -0.5)")
    legend
    xlabel("Log-transformed diagonal value produced by SPM")
    ylabel("Real value after reverting the log-transformation")
end
%% if PEB type = "change", sum the two covariates to get group 2 mean
if cov_n==2 && exist("PEB_type","var") && PEB_type=="change"
    Ep(:,:,3)   = Ep(:,:,1) + Ep(:,:,2);
    cov_names   = [cov_names,"mean of second group"];
    cov_n       = 3;
end

%% reorder ROIs if requested
if ~isempty(ROI_reorder)
    if length(ROI_reorder) < ROI_n
        error("All ROI numbers must be included in the new order list")
    end
    ROI_names   = ROI_names(ROI_reorder);
    Ep          = Ep(ROI_reorder,ROI_reorder,:);
end

%% Create colormap
% hot = [1,0,0;  % Red
%        1,1,0]; % Yellow
hot = [0.8,0.2,0.066;
       1,1,1]; 
hot = interp1([1,0],hot,linspace(0,1,64));
% cold = [0,1,1;            % Turqoise
%         0,0.0745,0.6078]; % Dark blue
cold = [1,1,1;
        0,0.266,0.533];
cold = interp1([1,0],cold,linspace(0,1,64));        
% Combine and add white in the middle
cmap = [cold;hot];
cmap(64:65,:) = 1;
clear hot cold

%% plot
fig = figure;

fig.NumberTitle = "off";
fig.Name        = "Posterior Expectation";
fig.Position    = [680 126 560 773];
tl              = tiledlayout(1,cov_n,"TileSpacing","compact","Padding","compact");

% turn off tex interpreter for axes tick labels, titles, etc (so the
% underscore is not interpeterd as a subscript)
%set(groot,"defaultAxesTickLabelInterpreter","none") % only tick labels
set(groot,"defaulttextinterpreter","none") % generl for all text

for i_cov = 1:cov_n
    tile = nexttile;
    imagesc(Ep(:,:,i_cov))

    title(cov_names(i_cov))

    % set aspect ratio 1:1
    pbaspect([1,1,1])
    
    % add axes labels (To-From)
    set(gca,"XAxisLocation","top");
    xlabel("From","FontSize",font_size, "FontWeight","bold");
    ylabel("To","FontSize",font_size, "FontWeight","bold");
    
    % add ROI labels on top
    yticks(1:ROI_n)
    yticklabels(ROI_names)
    xticks(1:ROI_n)
    xticklabels(ROI_names)
    xtickangle(30)

    % set colorbar limits
    lim = max([abs(min(Ep(:))), abs(max(Ep(:)))]);
    if lim > 0
        clim([-lim,lim])
    end
    
    % display colorbar
    if i_cov == cov_n
        % set colormap
        colormap(cmap);
        cbar = colorbar;
        % Add colorbar Label
        if exist("PEB_type","var") && PEB_type == "behav_associations"
            ylabel(cbar, "Normalised beta coefficients", "FontSize", font_size, ...
                "FontName", "Arial", "Rotation", -90);
        else
            ylabel(cbar, "Effective Connectivity (Hz)", "FontSize", font_size, ...
                "FontName", "Arial", "Rotation", -90);
        end
        % Increase padding
        cbar.Label.Position(1) = cbar.Label.Position(1) + 1.5;
    end

    % display numeric values
    for i = 1:ROI_n
        for j = 1:ROI_n
            if abs(round(Ep(i,j,i_cov),2)) > 0
                formatted_value = sprintf("%0.2f", Ep(i,j,i_cov)); % 2 decimal digits
                % if value is high, use white font
                if abs(Ep(i,j,i_cov)) < 0.5*lim
                    col = [0 0 0];
                else
                    col = [1 1 1];
                end
                text(j, i, formatted_value,...
                    "HorizontalAlignment","center",...
                    "VerticalAlignment", "middle",...
                    "Color",col,...
                    "FontSize", font_size, "FontName", "Arial");
            end
        end
    end
end
clear i j i_cov

% maximise window
fig.WindowState = "maximized";


% save the plot
plot_dir = '/fs04/fc37/adam/plots/m6';
[~, base_name, ~] = fileparts(f_PEB); % get base name without extension
plot_file = fullfile(plot_dir, [base_name, '.png']);

saveas(fig, plot_file);
fprintf('Plot saved to: %s\n', plot_file);
end
