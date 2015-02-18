% demo08_squareWorldMCL
% Demo generic Monte Carlo Localization

path(path,'threedee') 

%% Create a map
A = [
    0, 0, 15.5, 11.5
    15.5, 11.5, 20, 11
    45.5, 0, 6, 36.5
    0, 21, 5.5, 15.5
    5.5, 36.5, 22.5, 4.5
    28, 36.5, 17.5, 6
    ]
A(:, 1) = A(:, 1) - 20;
A(:, 2) = A(:, 2) - 20;
map=SquareMap(A, 35)

%% and a robot with noisy odometry
V=diag([0.01, 0.1*pi/180].^2)
veh=Differential(V, 'x0', [-20, 0, 0])
veh.add_driver(DeterministicPath('log-1423005664.txt'));

%% and then a sensor with noisy readings
W=0.05^2;
sensor = RangeSensor(veh,map, W,'log-1423005664.txt')

%% define two covariances for random noise Q and L (hmmm!)
% For Q, use the uncertainly estimates from A2!
Q = diag([0.01,0.01,0.1*pi/180].^2);
L = diag(0.1); 

%% Finally, construct ParticleFilter
pf = GenericParticleFilter(veh, sensor, Q, L, 200);

%% and run for 1000 steps
pf.run(1000,'nouniform');

