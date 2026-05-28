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

def log_likelihood_bernoulli(p, k, n=None):
    """
    Menghitung Log-Likelihood dari distribusi Bernoulli secara fleksibel.
    Bisa menerima (p, data_biner) ATAU (p, k, n).
    """
    # Menghindari log(0) atau log(1) yang menghasilkan -inf/nan
    p = np.clip(p, 1e-10, 1 - 1e-10)
    
    # Jika argumen kedua berupa array/Series data mentah biner
    if isinstance(k, (list, np.ndarray, pd.Series)):
        data = k
        k_success = np.sum(data)
        n_total = len(data)
    else:
        # Jika argumen berupa k (jumlah sukses) dan n (total data) langsung
        k_success = k
        n_total = n
        
    return k_success * np.log(p) + (n_total - k_success) * np.log(1 - p)

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

def beta_posterior(k, m, alpha_prior=1, beta_prior=1):
    """
    Menghitung parameter posterior Beta berdasarkan jumlah sukses (k) dan gagal (m).
    Mengembalikan dictionary sesuai kebutuhan notebook.
    """
    alpha_post = alpha_prior + k
    beta_post = beta_prior + m
    
    # Rumus Mean dan Mode Posterior (Tsun, 2020)
    mean_post = alpha_post / (alpha_post + beta_post)
    
    if alpha_post > 1 and beta_post > 1:
        mode_post = (alpha_post - 1) / (alpha_post + beta_post - 2)
    else:
        mode_post = 0.5 # Default jika uniform berlanjut
        
    return {
        'alpha': alpha_post,
        'beta': beta_post,
        'mean': mean_post,
        'mode': mode_post
    }