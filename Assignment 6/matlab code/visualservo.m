
% get target image position
targetImageName = 'pic-1428531465.jpg';
targetImage = imread(targetImageName);

% get list of existing images
images = dir('*.jpg');
imageNames = cell(size(images, 1), 1);
for i = 1 : size(images, 1)
    imageNames{i} = images(i).name;
end

%while criterion
    % construct motion plan
    motionPlanSize = 1;
    motionPlan = zeros(motionPlanSize, 3);
    %CREATE MOTION PLAN HERE

    % write motion plan to text
    dlmwrite('motion_plan.txt', motionPlan, ' ');

    % call python script to move robot and take picture
    system('python test.py');

    % get new list of images
    images = dir('*.jpg');
    newImageNames = cell(size(images, 1), 1);
    for i = 1 : size(images, 1)
        newImageNames{i} = images(i).name;
    end

    % find the new image
    new = ismember(imageNames, newImageNames);
    newImageName = newImageNames(~new)

    if size(newImageName, 1) > 0
        newImage = imread(newImageName(1));
    else
        disp('you done goofed, ya dingus');
    end

    imageNames = newImageNames;
%end
