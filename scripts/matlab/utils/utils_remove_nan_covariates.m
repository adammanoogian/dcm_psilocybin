function [GCM_tb, GCM, joined] = utils_remove_nan_covariates(GCM_tb, GCM, joined)
% Removes rows with NaN or empty values in any covariate from joined, GCM_tb, and GCM
% GCM_tb: cell array of tables (one per group)
% GCM: cell array of file paths (vertcat(GCM_tb{:}).Path)
% joined: table of covariates (rows correspond to GCM_cat)

nan_or_empty = any(ismissing(joined) | isnan(table2array(joined)), 2);
if any(nan_or_empty)
    disp('Removing participants with missing or NaN covariate values:')
    disp(joined(nan_or_empty,:))
    joined(nan_or_empty,:) = [];
    % Remove corresponding rows from GCM and GCM_tb
    GCM(nan_or_empty) = [];
    group_sizes = cellfun(@height, GCM_tb);
    idx = 1;
    for i_g = 1:numel(GCM_tb)
        idx_group = nan_or_empty(idx:idx+group_sizes(i_g)-1);
        if any(idx_group)
            GCM_tb{i_g}(idx_group,:) = [];
        end
        idx = idx + group_sizes(i_g);
    end
    clear group_sizes idx idx_group
end

end
