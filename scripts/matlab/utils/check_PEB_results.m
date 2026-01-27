function [outputArg1,outputArg2] = check_PEB_results(inputArg1,inputArg2)
%CHECK_PEB_RESULTS Useful functions for visualizing DCM/PEB through spm
%   Detailed explanation goes here



% Compare nested PEB models. Decide which connections to switch off based on the 
% structure of each template DCM in the GCM cell array. This should have one row 
% and one column per candidate model (it doesn't need to be estimated).
BMA = spm_dcm_peb_bmc(PEB, GCM);



% Review results
spm_dcm_peb_review(BMA,GCM)









outputArg1 = inputArg1;
outputArg2 = inputArg2;
end

