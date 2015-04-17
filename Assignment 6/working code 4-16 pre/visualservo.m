
% get target image position
targetImageName = 'img-end.jpg';
targetImage = imread(targetImageName);

num = 4;

Tc = transl(0,0,0);

targetC = icorner(targetImage, 'nfeat', num, 'color');
imageSize = size(targetImage);
corners = [0, 0;
           imageSize(1), 0;
           0, imageSize(2);
           imageSize(1:2)];
targetP = zeros(2 * num, 1);
for i = 1 : num
    distance = inf;
    closest = -1;
    for j = 1 : num
        curDistance = sum((corners(i, :) - [targetC(j).u, targetC(j).v]) .^ 2);
        if curDistance < distance
            distance = curDistance;
            closest = j;
        end
    end
    targetP(2 * i - 1 : 2 * i, :) = [targetC(closest).u, targetC(closest).v];
end

lambda = 0.5;

% get list of existing images
images = dir('*.jpg')
imageNames = cell(size(images, 1), 1);

for i = 1 : size(images, 1)
    imageNames{i} = images(i).name;
end

newImage = imread('img-start.jpg');

J = zeros(6,6);
cam = CentralCamera('default');

testCriterion = 0;
while testCriterion < 3
    % process current image
    cornersC = icorner(newImage, 'nfeat', num, 'color');
    currentP = zeros(2 * num, 1);
    for i = 1 : num
        distance = inf;
        closest = -1;
        for j = 1 : num
            curDistance = sum((corners(i, :) - [cornersC(j).u, cornersC(j).v]) .^ 2);
            if curDistance < distance
                distance = curDistance;
                closest = j;
            end
        end
        
        currentP(2 * i - 1 : 2 * i, :) = [cornersC(closest).u, cornersC(closest).v];
        J(2 * i - 1: 2 * i, :) = cam.visjac_p([cornersC(closest).u; cornersC(closest).v], 2);
    end
    J
    diff = targetP - currentP
    invJ = pinv(J);     %infJ = inv(J' * J) * J'; %same result
    v = lambda * (invJ * diff)
    Tc = trnorm(Tc * delta2tr(v))
%     diff' * invJ * diff
%     v' * v
    %304.8mm in 1ft
    
    % debug - display image and corners
    idisp(targetImage);
    targetC.plot();
    figure
    idisp(newImage);
    cornersC.plot();
    
    % construct motion plan
    motionPlanSize = 1;
    motionPlan = zeros(motionPlanSize, 3);
    %CREATE MOTION PLAN HERE
    motionPlan = [motionPlan; [1 1 1]];
    motionPlan = [motionPlan; [0 0 1]];

    % write motion plan to text
    dlmwrite('motion_plan.txt', motionPlan, ' ');

    % call python script to move robot and take picture
    system('calico.bat --exec logDataServo.py');
    disp 'Python done, returning to Matlab.'
    
    % get new list of images
    images = dir('*.jpg');
    newImageNames = cell(size(images, 1), 1);
    for i = 1 : size(images, 1)
        newImageNames{i} = images(i).name;
    end

    % find the new image
    new = ismember(newImageNames, imageNames);
    newImageName = newImageNames(~new);

    newImage = imread(newImageName{1});
    imageNames = newImageNames;
    
    testCriterion = testCriterion + 1;
end
