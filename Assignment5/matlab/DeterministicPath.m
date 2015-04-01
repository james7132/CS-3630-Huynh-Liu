%DeterministicPath Vehicle driver class

classdef DeterministicPath < handle
    properties
        veh
        log
        nrLines
        counter
    end
    
    methods
        
        function driver = DeterministicPath(filename)
            % Constructor
            fileID = fopen(filename);
            driver.log = textscan(fileID, '%d %d %s');            
            driver.nrLines=size(driver.log{1},1)
            fprintf(1,'read %d lines from %s\n',driver.nrLines,filename);
            driver.counter=1;
        end
        
        function init(driver)
        end
        
        function [ret] = demand(driver)
            % Return controls
            driver.counter = driver.counter + 1;
            if driver.counter>driver.nrLines
                u=[0;0];
                measurement = '';
            else
                % Motor values given to the Fluke [-200,200]
                % Left and right with respect to the Fluke
                v = [
                    driver.log{1}(driver.counter)
                    driver.log{2}(driver.counter)
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
                measurement = driver.log{3}(driver.counter);
                
                if measurement{1} == '0'
                    measurement = '';
                else
                    measurement = measurement{1};
                end
                
                
            end
            ret.u = u;
            ret.measurement = measurement;

        end
        
    end % methods
end % classdef
