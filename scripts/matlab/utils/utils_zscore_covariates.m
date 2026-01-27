function z = utils_zscore_covariates(x)
%UTILS_ZSCORE_COVARIATES Z-score normalization for a covariate vector
%   z = utils_zscore_covariates(x) returns the z-scored version of x, ignoring NaNs.
%   x should be a numeric vector.

if ~isvector(x)
    error('Input must be a vector.');
end

x = double(x); % ensure numeric
mu = mean(x(~isnan(x)));
sigma = std(x(~isnan(x)));

z = (x - mu) / sigma;

end
