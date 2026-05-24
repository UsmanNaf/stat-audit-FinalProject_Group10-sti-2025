import numpy as np

# ==========================================
# 1. BERNOULLI DISTRIBUTION
# ==========================================

def mle_bernoulli(data):
    """
    Menghitung Maximum Likelihood Estimator (MLE) untuk distribusi Bernoulli.
    Rumus: p_mle = mean(data)
    """
    if len(data) == 0:
        return 0
    return np.mean(data)

def log_likelihood_bernoulli(p, data):
    """
    Menghitung Log-Likelihood dari data Bernoulli berdasarkan parameter p.
    """
    # Menghindari log(0) dengan clip nilai p
    p = np.clip(p, 1e-10, 1 - 1e-10)
    n = len(data)
    k = np.sum(data)
    return k * np.log(p) + (n - k) * np.log(1 - p)


# ==========================================
# 2. POISSON DISTRIBUTION
# ==========================================

def mle_poisson(data):
    """
    Menghitung Maximum Likelihood Estimator (MLE) untuk distribusi Poisson.
    Rumus: lambda_mle = mean(data)
    """
    if len(data) == 0:
        return 0
    return np.mean(data)

def log_likelihood_poisson(lam, data):
    """
    Menghitung Log-Likelihood dari data Poisson berdasarkan parameter lambda (lam).
    """
    if lam <= 0:
        return -np.inf
    n = len(data)
    sum_x = np.sum(data)
    # Log-likelihood tanpa bagian log(x!) karena konstan terhadap lambda
    return sum_x * np.log(lam) - n * lam


# ==========================================
# 3. BAYESIAN INFERENCE (BETA-BINOMIAL)
# ==========================================

def beta_posterior(alpha_prior, beta_prior, data):
    """
    Mengupdate parameter distribusi Beta (Posterior) setelah melihat data Bernoulli.
    Rumus: 
      alpha_posterior = alpha_prior + sukses (jumlah angka 1)
      beta_posterior  = beta_prior + gagal (jumlah angka 0)
    """
    sukses = np.sum(data)
    gagal = len(data) - sukses
    
    alpha_post = alpha_prior + sukses
    beta_post = beta_prior + gagal
    
    return alpha_post, beta_post