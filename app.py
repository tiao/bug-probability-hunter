import scipy.stats as stats
import math
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def estimate_pmin(n, k, alpha):
  """
  Estimates the minimum possible probability of the bug.

  Args:
    n: Number of tests.
    k: Number of times the bug was observed.
    alpha: Desired confidence level (e.g., 0.05 for 95% confidence).

  Returns:
    Minimum possible probability of the bug.
  """

  # Beta-Binomial model
  a = k + 1
  b = n - k + 1
  pmin = stats.beta.ppf(alpha, a, b)
  return pmin

def calculate_required_tests(pmin, alpha):
  """
  Calculates the required number of tests after fixing the bug.

  Args:
    pmin: Minimum possible probability of the bug.
    alpha: Desired confidence level (e.g., 0.05 for 95% confidence).

  Returns:
    Required number of tests.
  """

  t = int(math.ceil(math.log(alpha) / math.log(1 - pmin)))
  return t

####  Example usage:
# n: the number of tests made;
# k: the number of times the bug was observed in the n tests;
# n = 4
# k = 1
# alpha = 0.05
# pmin = estimate_pmin(n, k, alpha)
# print(f"Estimated minimum probability: {pmin:.3f}")
# required_tests = calculate_required_tests(pmin, alpha)
# print(f"Required number of tests after fixing: {required_tests}")

# Título da aplicação
st.title("Análise de Bugs não determinísticos")

# Inputs para o usuário
n = st.number_input("Número de testes:", min_value=1, step=1, value=4)
k = st.number_input("Número de bugs encontrados:", min_value=1, step=1)
alpha = 0.05

# Cálculos
pmin = estimate_pmin(n, k, alpha)
required_tests = calculate_required_tests(pmin, alpha)

# Resultados
st.markdown(f"<p style='font-size: 24px;'>Número de testes necessários após a correção: <b>{required_tests}</b></p>", unsafe_allow_html=True)

# Gráfico
plt.figure()
tests = np.arange(1, (required_tests*2)+1)
significances = 1 - (1 - pmin)**tests
plt.plot(tests, significances)
plt.xlabel('Número de Testes')
plt.ylabel('Significância Estatística')
plt.title('Relação entre o número de testes e a significância estatística')
plt.grid(True)
plt.axhline(y=0.99, color='g', linestyle='--', label='99%')
plt.axhline(y=0.95, color='r', linestyle='--', label='95%')
plt.axhline(y=0.90, color='gray', linestyle='--', label='90%')
plt.legend(loc='right')
st.pyplot(plt)

st.write("**Referência:** [Probabilistic bug hunting](https://www.lpenz.org/articles/bugprobhunt/index.html)")
