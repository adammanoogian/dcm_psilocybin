function [A_constrained] = utils_get_constrained_A(f_PEB)
%UTILS_GET_CONSTRAINED_A Given a previous PEB, get the A matrix of only sig
%connections
%usage: running a behav PEB based only on a previous PEB's significant connections
%hardcoded to get 'change' Pp and must be 10 ROIs
%ATM 28/07/25

    %config
    model = "BMA";
    Pp_threshold = .99;

    %load model
    load(f_PEB)
    if ~exist(model,"var")
    error("%s variable not loaded in the workspace",model)
    end

    model = eval(model);
    
    if ~exist("BMA", "var") || ~exist("GCM", "var")
        error("BMA or GCM data not found in the PEB file")
    end
    
    %hardcoded for 2nd covariate and must have 10 ROIs/connections
    Pp_change = model.Pp(101:200);
    Pp_idx = logical(Pp_change >= Pp_threshold);
    A_cell = model.Pnames(Pp_idx);
    A_constrained = A_cell.';

end

