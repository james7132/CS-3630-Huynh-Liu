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

log = fopen('log-1428031739.txt');
data = textscan(log, '%d %d %s');
oldImage = 0;
oldSurf = 0;
oldCamera = 0;
imagesData = data{3};
images = cell(0);
surfs = cell(0);
cameras = cell(0);
matches = cell(0);
solutions = cell(0);
x = zeros([1, 3]);
x_hist = zeros(1, 3);
for i = 1 : size(imagesData, 1)
      test = imagesData{i};
%     v = [data{1}(i)
%      data{2}(i)
%     ];
% 
%     % get motor values (Left-Right wrpt Fluke)
%     uL=v(1);
%     uR=v(2);
% 
%     scale = 39.3701;  %Change it to accordingly to what you used in Assignment 3
%     ScaledUL = double(uL)*scale;
%     ScaledUR = double(uR)*scale;
% 
%     r = 1.375;
%     L = 5.75;
% 
%     % calculate speed
%     u(1) = 0.04 * r.*((ScaledUL+ScaledUR)./2);
%     u(2) = 0.1875 * (r./L).*(ScaledUR-ScaledUL);
% 
%     x = x + u;
%     x_hist = [x_hist; x];
    if(~strcmp(test, '0'))
        image = imread(test);
        surf = isurf(image);
        camera = CentralCamera('image', image, 'default');
%         figure
%         imshow(image);
%         hold on
%         plot(surf.u, surf.v, '*', 'color', 'red');
        
        if(oldSurf ~= 0)
            match = oldSurf.match(surf, 'thresh', 4);
%             figure
%             idisp({oldImage, image});
%             match.plot();
            F = match.ransac(@fmatrix, 1e-2, 'verbose');
%              figure
%              idisp({oldImage, image});
%              match.inlier.plot('g');
            %E = camera.E(oldCamera);
            E = transpose(K) * F * K;
            Q = [0 0 100]';
            sol = camera.invE(E, Q);
            
            R = sol(1:3, 1:3);
            t = sol(1:3, 4);
            
            euler = tr2eul(R);
            x(3) = x(3) + euler(3);
            x(1) = x(1) + sol(1) * cos(x(3) - sol(2) * sin(x(3)));
            x(2) = x(2) + sol(1) * sin(x(3) + sol(2) * cos(x(3)));
            
            x_hist = [x_hist; x];
            
            solutions = [solutions, {sol}];
            matches = [matches, {match}];
        end
        
        oldImage = image;
        oldSurf = surf;
        oldCamera = camera;
        
        images = [images, {image}];
        surfs = [surfs; {surf}];
        cameras = [cameras, {camera}];
    end
end

% currentTransform = [1,0,0,0;
%                     0,1,0,0;
%                     0,0,1,0;
%                     0,0,0,1];
% scale = [1,0,0,0;
%                     0,1,0,0;
%                     0,0,1,0;
%                     0,0,0,1];
% x = zeros(1);
% y = zeros(1);
% for i = 1 : size(solutions, 2)
%     solutions{i} = solutions{i} * scale;
% end
% for i = 1 : size(solutions, 2)
%     x = [x, currentTransform(1, 4)];
%     y = [y, currentTransform(2, 4)];
%     currentTransform = currentTransform + solutions{i};
% end
plot(x_hist(:,1),x_hist(:,2));