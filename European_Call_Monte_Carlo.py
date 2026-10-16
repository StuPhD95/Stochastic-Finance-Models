"""
European call option using Monte Carlo.
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters.
S0 = 100    # Price of underlying asset today.
K = 100     # Strike price.
T = 2       # Time to expiry (years).
r = 0.05    # Annual continuously compounded risk-free interest rate.
sigma = 0.2 # Annual volatility
n = 100000  # Number of independent expiry prices. 
seed = 42   # To allow for reproducibility.

# Generate standard normal random draws.
rng = np.random.default_rng(seed)
z = rng.standard_normal(size=n) 

# Generate prices of underlying asset at expiry.
deterministic_term = (r - 0.2*sigma**2)*T
stochastic_term = sigma*np.sqrt(T)*z
price_at_expiry = S0*np.exp(deterministic_term + stochastic_term)

# Calculate payoffs and their mean.
payoffs = np.maximum(price_at_expiry - K, 0)
mean_payoffs = payoffs.mean()

# Discount 
discount_factor = np.exp(-r*T)
price_estimate = discount_factor * mean_payoffs

# Compute standard error and confidence interval.
discounted_payoffs = discount_factor * payoffs
discounted_payoff_std = discounted_payoffs.std(ddof=1)
standard_error = discounted_payoff_std / np.sqrt(n)
print(f"Standard Error = {standard_error:.4f}")

ci_lower = price_estimate - 1.96 * standard_error
ci_upper = price_estimate + 1.96 * standard_error
print(f"Estimated price: ${price_estimate:.4f}")
print(f"Approximate 95% confidence interval: [${ci_lower:.4f}, ${ci_upper:.4f}]")

# Plot
sample_sizes = np.unique(np.geomspace(100, n, 120).round().astype(int))

running_prices = []
running_errors = []

for i in sample_sizes:
    sample = discounted_payoffs[:i]
    running_prices.append(sample.mean())
    running_errors.append(sample.std(ddof=1) / np.sqrt(i))

running_prices = np.array(running_prices)
running_errors = np.array(running_errors)

plt.plot(sample_sizes, running_prices,label="Running price estimate")

plt.fill_between(sample_sizes,
    running_prices - 1.96 * running_errors,
    running_prices + 1.96 * running_errors,
    alpha=0.2,
    label="Approximate 95% confidence interval")

plt.xscale("log")
plt.xlabel("Number of simulations (log scale)", fontsize=16)
plt.ylabel("Estimated call price ($)", fontsize=16)
plt.title("Simulated European Call Option with 95% Percentile Band", fontsize=16)
plt.legend(loc="lower right", frameon=True, fontsize=16)
plt.tick_params(axis="both", labelsize=16)
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()