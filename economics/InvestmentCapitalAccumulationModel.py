import numpy as np

class InvestmentCapitalAccumulationModel:
    def __init__(self, A1, A2, K1, delta, r):
        self.A1 = A1  # Productivity in period 1
        self.A2 = A2  # Productivity in period 2
        self.K1 = K1  # Initial capital in period 1
        self.delta = delta  # Depreciation rate
        self.r = r  # Real interest rate

    def production_function(self, K):
        """
        Cobb-Douglas production function: Y = K^alpha
        """
        alpha = 0.3  # Capital share
        return K ** alpha

    def marginal_product_of_capital(self, K):
        """
        Marginal product of capital: F'(K) = alpha * K^(alpha - 1)
        """
        alpha = 0.3  # Capital share
        return alpha * K ** (alpha - 1)

    def profit(self, K, I, period):
        """
        Calculate profit for a given period.
        """
        if period == 1:
            return self.A1 * self.production_function(K) - I
        elif period == 2:
            K2 = I + (1 - self.delta) * K
            return self.A2 * self.production_function(K2) + (1 - self.delta) * K2

    def pdv_of_profits(self, I):
        """
        Calculate the present discounted value (PDV) of profits.
        """
        K2 = I + (1 - self.delta) * self.K1
        profit1 = self.profit(self.K1, I, period=1)
        profit2 = self.profit(K2, I, period=2)
        return profit1 + profit2 / (1 + self.r)

    def optimal_investment(self):
        """
        Find the optimal investment that maximizes the PDV of profits.
        """
        from scipy.optimize import minimize

        result = minimize(lambda I: -self.pdv_of_profits(I), x0=0, bounds=[(0, None)])
        return result.x[0]

# Parameters
A1 = 1.0  # Productivity in period 1
A2 = 1.2  # Productivity in period 2
K1 = 10.0  # Initial capital in period 1
delta = 0.1  # Depreciation rate
r = 0.05  # Real interest rate

# Create the model instance
model = InvestmentCapitalAccumulationModel(A1, A2, K1, delta, r)

# Find the optimal investment
optimal_investment = model.optimal_investment()
print(f"Optimal Investment: {optimal_investment}")

# Calculate the PDV of profits with the optimal investment
pdv_profits = model.pdv_of_profits(optimal_investment)
print(f"PDV of Profits: {pdv_profits}")
