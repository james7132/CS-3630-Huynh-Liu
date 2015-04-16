
% get target image position
targetImageName = 'img-end.jpg';
targetImage = imread(targetImageName);

% get list of existing images
images = dir('*.jpg')
imageNames = cell(size(images, 1), 1);
for i = 1 : size(images, 1)
    imageNames{i} = images(i).name;
end

newImage = imread('img-start.jpg');

testCriterion = 0;
while testCriterion < 3
    % process current image
    cornersC = icorner(newImage, 'nfeat', 4, 'color');
    
    % debug - display image and corners
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
