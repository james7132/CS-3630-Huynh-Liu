A =  zeros(500, 2);
A(A == 0) = NaN;

f_x = 1211.2959;
f_y = 1206.00512;
s = 0.0;
c_x = 657.15924;
c_y = 403.17667;

K = [f_x,   s, c_x;
    0   , f_y, c_y; 
    0   ,   0,   1];

Camera = CentralCamera('name', 'robocam', 'default');


log = fopen('log-1427161855.txt');
data = textscan(log, '%d %d %s');
imagesData = data{3};
images = cell(0);
surfs = cell(0);
cameras = cell(0);
x = zeros([1, 2]);
for i = 1 : size(imagesData, 1)
    test = imagesData{i};

    v = [data{1}(i)
         data{2}(i)
        ];

    % get motor values (Left-Right wrpt Fluke)
    uL=v(1);
    uR=v(2);

    scale = 39.3701;  %Change it to accordingly to what you used in Assignment 3
    ScaledUL = double(uL)*scale;
    ScaledUR = double(uR)*scale;

    r = 1.375;
    L = 5.75;

    % calculate speed
    u(1) = 0.04 * r.*((ScaledUL+ScaledUR)./2);
    u(2) = 0.1875 * (r./L).*(ScaledUR-ScaledUL);
    
    x = x + u;
    if(~strcmp(test, '0'))
        image = imread(test);
        surf = isurf(image);
        camera = CentralCamera('image', image);
        
        images = [images, {image}];
        surfs = [surfs; {surf}];
        cameras = [cameras, {camera}];
    end
end
matches = cell(0);
solutions = cell(0);
for i = 1 : size(surfs, 1) - 1
    current = surfs{i};
    next = surfs{i + 1};
    match = current.match(next, 'thresh', 40);
    matches = [matches, {match}];
%     figure
%     idisp(images(1, i:i+1));
%     match.plot('w');
    F = match.ransac(@fmatrix, 1e-1, 'verbose');
%    E = K' * F * K;
    E = Camera.E(F);
    sol = Camera.invE(E);
    diff1 = sum(sum((sol(:,:,1) - inv(cameras{i}.T) * cameras{i + 1}.T).^2));
    diff2 = sum(sum((sol(:,:,2) - inv(cameras{i}.T) * cameras{i + 1}.T).^2));
    if(diff1 < diff2)
        sol = sol(:, :, 1);
    else
        sol = sol(:, :, 2);
    end
    solutions = [solutions, {sol}];
    [R, t] = tr2rt(cameras{i}.T)
    fkine
    cameras{i}.plot_camera('color', 'r');
end


% %% and a robot with noisy odometry
% 
% V=diag([.1, .3*pi/180].^2);        % default 0.1, 1.1
% veh=GenericVehicle(V,'dt',0.1);
% veh.x0 = [0,0, pi/2 * 2/3];
% driver = DeterministicPath('log-test (1).txt');
% veh.add_driver(driver);
% 
% % Creating the map. It places landmarks according to 'A' matrix.
% map = LandmarkMap(500, A, 5);
% 
% % Creating the sensor.  We firstly define the covariance of the sensor measurements
% % which report distance and bearing angle
% W = diag([0.1, 0.1*pi/180].^2);       %  default 0.1 1
% 
% % and then use this to create an instance of the Sensor class.
% sensor = GenericRangeBearingSensor(veh, map, W, 'animate');
% % Note that the sensor is mounted on the moving robot and observes the features
% % in the world so it is connected to the already created Vehicle and Map objects.
% 
% % Create the filter.  First we need to determine the initial covariance of the
% % vehicle, this is our uncertainty about its pose (x, y, theta)
% P0 = diag([0.1, 0.1, 0.1 * pi/180].^2);  % default .005 .005 .001s
% 
% % Now we create an instance of the EKF filter class
% ekf = GenericEKF(veh, V, P0, sensor, W, []);
% % and connect it to the vehicle and the sensor and give estimates of the vehicle
% % and sensor covariance (we never know this is practice).
% 
% % Now we will run the filter for 1000 time steps.  At each step the vehicle
% % moves, reports its odometry and the sensor measurements and the filter updates
% % its estimate of the vehicle's pose
% ekf.run(569); %596 non-closure  %870 closure
% % all the results of the simulation are stored within the EKF object
% 
% % First let's plot the map
% clf; map.plot()
% % and then overlay the path actually taken by the vehicle
% veh.plot_xy('b');
% % and then overlay the path estimated by the filter
% ekf.plot_xy('r');
% % which we see are pretty close
% 
% % Now let's plot the error in estimating the pose
% axis equal
% figure
% ekf.plot_error()
% % and this is overlaid with the estimated covariance of the error.
% 
% % Remember that the SLAM filter has not only estimated the robot's pose, it has
% % simultaneously estimated the positions of the landmarks as well.  How well did it
% % do at that task?  We will show the landmarks in the map again
% figure
% map.plot();
% % and this time overlay the estimated landmark (with a +) and the 3sigma 
% % uncertainty bounds as green ellipses
% ekf.plot_map(3,'g');
