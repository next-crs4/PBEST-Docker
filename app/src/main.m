function detected_samples = main(exp_data, verbose)
warning("off");
pkg load io;

if nargin < 2
    verbose = false;
end

% a) load pooling matrix
if verbose
    printf("\nloading pooling matrix from %s", Consts.pool_matrix)
end
load(Consts.pool_matrix)

% b) values measured experimentally
if verbose
    printf("\nreading values measured experimentally from file %s\n\n", exp_data)
end
[~,~,raw] = xlsread(exp_data);
raw(1,:) = [];
raw = cell2mat(raw);

% change measurement values to binary
if verbose
    printf("\nchanging measurement values to binary")
end
qMeasurement = zeros(48,1);
qMeasurement(find(raw(:,2))) = 1;

%qMeasurement = dlmread('../data/expResults.csv','\t', 1, 0);

% c) Detecting carriers
% find candidates using GPSR.
if verbose
    printf("\ndetecting carriers")
    printf("\nfind candidates using GPSR")
end
maxNum = 20; % the largest 1:maxNum entries are considered
dt = max(abs(poolingMatrix'*qMeasurement));
tau = 0.005*dt;
u = opm(qMeasurement,poolingMatrix,tau,maxNum);

% look for the solution with minimal error with the measurements
if verbose
    printf("\nlooking for the solution with minimal error with the measurements")
end
discreteOutput = selectByError(u,poolingMatrix,qMeasurement);
detected_samples = find(discreteOutput);

end

