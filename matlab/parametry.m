close all;
clear all; %#ok<*CLALL>
%% Load the PPG signal
nPPG = 60000;
Fs = 100;
dt = (0:nPPG-1)/Fs;
opts = detectImportOptions('C:/Users/Asia/Desktop/Praca/matlab/baza_uporz¹dkowana/osoba_5/20min - 30min.csv', 'NumHeaderLines', 0);
T = readtable('C:/Users/Asia/Desktop/Praca/matlab/baza_uporz¹dkowana/osoba_5/20min - 30min.csv', opts);
yn = table2array(T(:,6));
%% Plot the PPG signal
figure;
plot(dt,yn);
title('Sygna³ PPG');
xlabel('t [s]');
% Plot the PPG signal & ART signal
K = {};
ART = table2array(T(:,3));
art_sys = table2array(T(:,4));
art_dia = table2array(T(:,5));
figure;
plot(dt,yn);
K{1} = 'Sygna³ PPG';
hold on;
grid on;
plot(dt,(ART-mean(ART))*0.01,'r');
K{2} = 'Sygna³ ART';
title('Sygna³ PPG i sygna³ ART');
xlabel('t [s]');
legend(K);
%% Maximum & Minimum peaks - PPG signal
%max
[pks,locs_pks] = findpeaks(yn,'MinPeakProminence',0.3,'MinPeakDistance',50);
%min
[minimum,locs_min] = findpeaks(-yn,'MinPeakProminence',0.3,'MinPeakDistance',50);
minimum = -minimum;
%% Marking max and min on PPG signal
L = {}; %legend
figure;
plot(dt,yn);
L{1} = 'sygna³ PPG';
hold on;
L{2}= 'maksima (piki skurczowe)';
hold on;
plot(locs_pks*0.01,pks,'*');
hold on;
plot(locs_min*0.01,minimum,'*');
L{3}='minima';
title('Maksima i minima sygna³u PPG');
xlabel('t [s]');
legend(L);
%% Parameters
locs_max_size = size(locs_pks);
locs_min_size = size(locs_min);
cp = [];
st = [];
dt = [];
precent = [0.1,0.25,0.33,0.5,0.66,0.75];
precent_size = length(precent);
sw10 = [];
dw10 = [];
sw25 = [];
dw25 = [];
sw33 = [];
dw33 = [];
sw50 = [];
dw50 = [];
sw66 = [];
dw66 = [];
sw75= [];
dw75 = [];
height=0;

for i = 1:locs_max_size(1)-5
    %% maximum first
    if locs_min(1)>locs_pks(1) 
       %CP
       cp(i) = locs_pks(i+2) - locs_pks(i+1); 
       %ST
       st(i) = locs_pks(i+1) - locs_min(i);
       %DT
       dt(i) = locs_min(i+1) - locs_pks(i+1);
    end
    %% minimum first
    if locs_min(1)<locs_pks(1)
       %CP
       cp(i) = locs_pks(i+1) - locs_pks(i); 
       %ST
       st(i) = locs_pks(i) - locs_min(i);
       %DT
       dt(i) = locs_min(i+1) - locs_pks(i);
    end
end

%% Marking the parameters
L = {}; %legend
figure;
plot(yn(1:700));
L{1} = 'sygna³ PPG';
title('Fragment sygna³u PPG i jego parametery');
hold on;
%% Maximum first
if locs_min(1)>locs_pks(1)    
    plot([locs_min(1) locs_pks(2)], [minimum(1) minimum(1)],'red','LineWidth',3); %ST-1
    plot([locs_pks(2) locs_min(2)], [minimum(2) minimum(2)],'yellow','LineWidth',3); %DT-1
    plot([locs_pks(2) locs_pks(3)], [pks(2) pks(2)],'green','LineWidth',3); %CP-1
    plot([locs_min(2) locs_pks(3)], [minimum(2) minimum(2)],'blue','LineWidth',3); %ST-2
    plot([locs_pks(3) locs_min(3)], [minimum(3) minimum(3)],'Color',[rand rand rand],'LineWidth',3); %DT-2
    plot([locs_pks(3) locs_pks(4)], [pks(3) pks(3)],'Color',[rand rand rand],'LineWidth',3); %CP-2  
    plot([locs_min(3) locs_pks(4)], [minimum(3) minimum(3)],'magenta','LineWidth',3); %ST-3
    plot([locs_pks(4) locs_min(4)], [minimum(4) minimum(4)],'cyan','LineWidth',3); %DT-3
    plot([locs_pks(4) locs_pks(5)], [pks(4) pks(4)],'black','LineWidth',3); %CP-3
    
    L{2} = 'ST-1';
    L{3} = 'DT-1';
    L{4} = 'CP-1';
    L{5} = 'ST-2';
    L{6} = 'DT-2';
    L{7} = 'CP-2';
    L{8} = 'ST-3';
    L{9} = 'DT-3';
    L{10} = 'CP-3';
    
    %dashed lines
    plot([locs_pks(2) locs_pks(2)], [minimum(1) pks(2)],':k');
    plot([locs_pks(3) locs_pks(3)], [pks(2) pks(3)],':k');
    plot([locs_pks(3) locs_pks(3)], [minimum(2) pks(3)],':k');
    plot([locs_pks(4) locs_pks(4)], [pks(3) pks(4)],':k');
    plot([locs_pks(4) locs_pks(4)], [minimum(3) pks(4)],':k');
    plot([locs_pks(5) locs_pks(5)], [pks(4) pks(5)],':k');
    plot([locs_pks(3) locs_pks(3)], [minimum(2) minimum(3)],':k');
    plot([locs_pks(2) locs_pks(2)], [minimum(1) minimum(2)],':k');
    plot([locs_pks(4) locs_pks(4)], [minimum(3) minimum(4)],':k');
    legend(L);
    
end

%% Minimum first
if locs_min(1)<locs_pks(1)   
    plot([locs_min(1) locs_pks(1)], [minimum(1) minimum(1)],'red','LineWidth',3); %ST-1
    plot([locs_pks(1) locs_min(2)], [minimum(1) minimum(1)],'yellow','LineWidth',3); %DT-1    
    plot([locs_pks(1) locs_pks(2)], [pks(1) pks(1)],'green','LineWidth',3); %CP-1 
    plot([locs_min(2) locs_pks(2)], [minimum(2) minimum(2)],'blue','LineWidth',3); %ST-2
    plot([locs_pks(2) locs_min(3)], [minimum(2) minimum(2)],'Color',[rand rand rand],'LineWidth',3); %DT-2
    plot([locs_pks(2) locs_pks(3)], [pks(2) pks(2)],'Color',[rand rand rand],'LineWidth',3); %CP-2
    plot([locs_pks(3) locs_min(3)], [minimum(3) minimum(3)],'magenta','LineWidth',3); %ST-3
    plot([locs_pks(3) locs_min(4)], [minimum(4) minimum(4)],'cyan','LineWidth',3); %DT-3
    plot([locs_pks(3) locs_pks(4)], [pks(3) pks(3)],'black',LineWidth',3); %CP-3
    L{2} = 'ST-1';
    L{3} = 'DT-1';
    L{4} = 'CP-1';
    L{5} = 'ST-2';
    L{6} = 'DT-2';    
    L{7} = 'CP-2';
    L{8} = 'ST-3';    
    L{9} = 'DT-3';
    L{10} = 'CP-3';

    %dashed lines
    plot([locs_pks(1) locs_pks(1)], [pks(1) minimum(1)],':k');
    plot([locs_pks(2) locs_pks(2)], [pks(2) minimum(2)],':k');
    plot([locs_pks(2) locs_pks(2)], [pks(1) pks(2)],':k');
    plot([locs_min(2) locs_min(2)], [minimum(1) minimum(2)],':k');
    plot([locs_pks(3) locs_pks(3)], [pks(2) pks(3)],':k');
    plot([locs_min(3) locs_min(3)], [minimum(2) minimum(3)],':k');
    plot([locs_pks(3) locs_pks(3)], [pks(3) minimum(3)],':k');
    plot([locs_pks(4) locs_pks(4)], [pks(4) pks(3)],':k');
    plot([locs_pks(3) locs_pks(3)], [minimum(4) minimum(3)],':k');

    legend(L);     
    
end
%% %-Parameters: sw, dw, cp
for i = 1:locs_max_size(1)-5
    %% Single signal extraction
       single = yn(locs_min(i):locs_min(i+1));
       single_size = size(single);
       single_x = [1:single_size(1)];
    %% Single signal plot
    if i == 4
        figure;
        plot(single_x+locs_min(i),single,'-','LineWidth',7);
        title({'Pojedynczy sygna³ PPG';'Parametry przy % wysokoœci'});
        hold on;
    end
    precent_graph_size = [];
    %% Percent of height graph
    for j=1:precent_size
        height = max(single) - min(single);
        percent_of_height = height * precent(j);
        single_percent_level = min(single)+percent_of_height;
        upper_signal = [];
        precent_graph_x = [];
        
        upper_signal = [upper_signal single_percent_level];

        for k = 1:(length(single))
            if single(k) >= single_percent_level
                upper_signal = [upper_signal single(k)];
                precent_graph_x = [precent_graph_x k];
            end 
        end
         upper_signal = [upper_signal single_percent_level];
               
         precent_graph_size(j) = precent_graph_x(1);
         upper_signal_size = size(upper_signal);
         move = [1:upper_signal_size(2)];

        %% Parameters for % graph
        %max
        [A, t] = max(upper_signal); 
        
        %sw10, dw_10, sw10 + dw10, dw10/sw10
        if j == 1 
            sw10 = [sw10 t];
            dw10 = [dw10 length(upper_signal) - t];
            cw10 = sw10 + dw10;
            relation10 = dw10./sw10;
        end
        
        %sw25, dw_25, sw25 + dw25, dw25/sw25
        if j == 2
            sw25 = [sw25 t];
            dw25 = [dw25 length(upper_signal) - t];
            cw25 = sw25 + dw25;
            relation25 = dw25./sw25;
        end
        
        %sw33, dw_33, sw33 + dw33, dw33/sw33
        if j == 3
            sw33 = [sw33 t];
            dw33 = [dw33 length(upper_signal) - t];
            cw33 = sw33 + dw33;
            relation33 = dw33./sw33;
        end
        
        %sw50, dw_50, sw50 + dw50, dw50/sw50
        if j == 4 
            sw50 = [sw50 t];
            dw50 = [dw50 length(upper_signal) - t];
            cw50 = sw50 + dw50;
            relation50 = dw50./sw50;
        end
        
        %sw66, dw_66, sw66 + dw66, dw66/sw66
        if j == 5 
            sw66 = [sw66 t];
            dw66 = [dw66 length(upper_signal) - t];
            cw66 = sw66 + dw66;
            relation66 = dw66./sw66;
        end
        
        %sw75, dw_75, sw75 + dw75, dw75/sw75
        if j == 6 
            sw75 = [sw75 t];
            dw75 = [dw75 length(upper_signal) - t];
            cw75 = sw75 + dw75;
            relation75 = dw75./sw75;
        end

        %% Marking parameters
        if i == 4
            plot([locs_min(i)+precent_graph_size(j)-1 locs_min(i)+precent_graph_size(j)-2+t], [upper_signal(1) upper_signal(1)],'LineWidth',3, 'Color', [rand,rand,rand]); %sw 
            plot([locs_min(i)+precent_graph_size(j)-2+t locs_min(i)+precent_graph_size(j)-2+length(upper_signal)], [upper_signal(1) upper_signal(1)],'LineWidth',3,'Color', [rand,rand,rand]); %dw
            hold on;
            plot(move+precent_graph_size(j)+locs_min(i)-2,upper_signal,'-','LineWidth',7);           
        end
    end
    %dashed lines
     if i ==4        
         plot([locs_min(i)+precent_graph_size(j)-2+t locs_min(i)+precent_graph_size(j)-2+t], [A min(single)],':k');
         legend('10%','SW-10','DW-10','25%','SW-25','DW-25','33%','SW-33','DW-33','50%','SW-50','DW-50','66%','SW-66','DW-66','75%','SW-75','DW-75','100%');
     end
end

%Matching BP (sys&dia) to peaks
sys = [];
dia = [];

for i=1:locs_max_size-5
    n = locs_pks(i);
    sys = [sys art_sys(n)];
    dia = [dia art_dia(n)];
end

%Saving results & Converting units
%1 sample = 10 ms
results=[10*cp.' 10*st.' 10*dt.' 10*sw10.' 10*dw10.' 10*cw10.' relation10.' 10*sw25.' 10*dw25.' 10*cw25.' relation25.' 10*sw33.' 10*dw33.' 10*cw33.' relation33.' 10*sw50.' 10*dw50.' 10*cw50.' relation50.' 10*sw66.' 10*dw66.' 10*cw66.' relation66.' 10*sw75.' 10*dw75.' 10*cw75.' relation75.' sys.' dia.'];
cHeader = {'cp' 'st' 'dt' 'sw10' 'dw10' 'sw10+dw10' 'dw10/sw10' 'sw25' 'dw25' 'sw25+dw25' 'dw25/sw25' 'sw33' 'dw33' 'sw33+dw33' 'dw33/sw33' 'sw50' 'dw50' 'sw50+dw50' 'dw50/sw50' 'sw66' 'dw66' 'sw66+dw66' 'dw66/sw66' 'sw75' 'dw75' 'sw75+dw75' 'dw75/sw75' 'sys' 'dia'}; %dummy header
commaHeader = [cHeader;repmat({','},1,numel(cHeader))]; %insert commaas
commaHeader = commaHeader(:)';
textHeader = cell2mat(commaHeader); %cHeader in text with commas
%write header to file
fid = fopen('results20-1.csv','w'); 
fprintf(fid,'%s\n',textHeader);
fclose(fid);
%write data to end of file
dlmwrite('results20-1.csv',results,'-append');



