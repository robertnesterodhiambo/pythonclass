import numpy as np
from scipy.optimize import fsolve

class TANKModel:
    def __init__(self, beta, lambda_h, r, income, initial_consumption):
        self.beta = beta  # Discount factor
        self.lambda_h = lambda_h  # Fraction of hand-to-mouth households
        self.r = r  # Real interest rate
        self.income = income  # Income (assumed constant for simplicity)
        self.C_o = initial_consumption  # Initial consumption for optimizing households

    def euler_equation(self, C_o_next):
        """
        Euler equation for optimizing households.
        """
        return self.C_o - (self.beta * (1 + self.r) * C_o_next)

    def aggregate_consumption(self, C_o_next):
        """
        Calculate aggregate consumption.
        """
        C_h = self.income  # Hand-to-mouth households consume their entire income
        C_o = fsolve(self.euler_equation, self.C_o)  # Solving for C_o using the Euler equation
        aggregate_C = (1 - self.lambda_h) * C_o_next + self.lambda_h * C_h
        return aggregate_C

    def simulate_period(self, periods):
        """
        Simulate the model for a given number of periods.
        """
        consumption_path = []
        C_o_next = self.C_o

        for t in range(periods):
            aggregate_C = self.aggregate_consumption(C_o_next)
            consumption_path.append(aggregate_C)
            C_o_next = fsolve(self.euler_equation, C_o_next)[0]

        return consumption_path

# Parameters
beta = 0.96  # Discount factor
lambda_h = 0.4  # Fraction of hand-to-mouth households
r = 0.03  # Real interest rate
income = 1.0  # Income (constant for simplicity)
initial_consumption = 0.8  # Initial consumption for optimizing households

# Create the model instance
model = TANKModel(beta, lambda_h, r, income, initial_consumption)

# Simulate the model for 10 periods
periods = 10
consumption_path = model.simulate_period(periods)

# Output the results
for t, consumption in enumerate(consumption_path):
    print(f"Period {t+1}: Aggregate Consumption = {consumption}")
