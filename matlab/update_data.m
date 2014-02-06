output = bestlh(10,3,1,1);
csvwrite('matlab_output.csv',output);
%scatter3(output(:,1),output(:,2),output(:,3))