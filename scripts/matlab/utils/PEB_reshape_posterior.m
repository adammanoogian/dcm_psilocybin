function model = PEB_reshape_posterior(model, ROI_n)
% Reshapes model.Ep and model.Pp as (ROI number,ROI number,covariate number)

    %% old code: doesn't work if a subset of A is used, e.g. A(1,2), A(1,3)
    % cov_n = length(model.Xnames) % covariates number
    % ROI_n = sqrt(length(model.Pnames)) % number of ROIs
    % Ep    = reshape(full(model.Ep),ROI_n,ROI_n, cov_n); % posterior expectations
    % Pp    = reshape(model.Pp,ROI_n,ROI_n,cov_n); % posterior prob
    
    %% Read fields from model
    cov_n   = size(model.M.X,2); % Covariates
    param_n = length(model.Pnames); % Parameters
    
    % Correct model matrix size (Ep)
    if size(model.Ep,2) ~= cov_n
        model.Ep = reshape(model.Ep,param_n,cov_n);
    end
    % Correct model posterior probability size (Pp)
    if size(model.Pp,2) ~= cov_n
        model.Pp = reshape(model.Pp,param_n,cov_n);
    end
    
    % Correct model matrix size (Cp)
    if isvector(model.Cp)
        model.Cp = diag(model.Cp);
    end
    
    % Get parameters included in the PEB (rows and columns)
    parts  = cell(1,param_n);
    for p = 1:param_n
        str = ['(?<field>[A-Za-z0-9\{\},]+)\('... % Match field and open bracket
            '(?<row>\d+)(,|\))'...     % Match row and open bracket or comma
            '(?<col>\d+)?(,|\))?'];    % Match column and open bracket or comma
        parts{p}     = regexp(model.Pnames{p}, str, 'names');
        parts{p}.row = str2double(parts{p}.row);
        parts{p}.col = str2double(parts{p}.col);
    end
    
    %% Reshape posteriors

    % Reshape posterior expectation
    Ep = zeros(ROI_n,ROI_n,cov_n);
    for i_cov = 1:cov_n
        for p = 1:param_n
            if strcmp(parts{p}.field, 'A')
                row = parts{p}.row;
                col = parts{p}.col;
                Ep(row,col,i_cov) = model.Ep(p,i_cov);
            end
        end
    end
    
    % Reshape posterior probability
    Pp = zeros(ROI_n,ROI_n,cov_n);
    for i_cov = 1:cov_n
        for p = 1:param_n
            if strcmp(parts{p}.field, 'A')
                row = parts{p}.row;
                col = parts{p}.col;
                Pp(row,col,i_cov) = model.Pp(p,i_cov);
            end
        end
    end

    %% replace Ep and Pp
    model.Ep = Ep;
    model.Pp = Pp;
    model.parts = parts;

end