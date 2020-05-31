function [ ] = COVID19b( b,beta,gamma,xi,epsilon, mu, delta,theta,zeta,d,ti,tf,S0,E0 ,I0, Q0, R0)

%COVID19 virus spread model 

f=@(t,x) [b-beta*x(1)*x(3)+zeta*x(5)-d*x(1);
          beta*x(1)*x(3)-(gamma+xi)*x(2)-d*x(2);
          gamma*x(2)-(epsilon+delta)*x(3)-(mu+d)*x(3);
          delta*x(3)-theta*x(4)-(mu+d)*x(4);
          epsilon*x(3)+theta*x(4)+xi*x(2)-zeta*x(5)-d*x(5)];

[t,xa]=ode45(f,[ti tf],[S0 E0 I0 Q0 R0]);

plot(t,xa(:,1))
hold on 

for i=2:5
    plot(t,xa(:,i))
end 
legend('S','E','I','Q','R')
end

