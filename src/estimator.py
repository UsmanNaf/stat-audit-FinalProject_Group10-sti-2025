import numpy as np
from scipy.stats import bernoulli, poisson, beta
from typing import Dict, List, Union, Tuple
import math


# ============================================================================
# 1. FUNGSI UNTUK DISTRIBUSI BERNOULLI
# ============================================================================

def mle_bernoulli(data: List[int]) -> Dict[str, float]:
    """
    Menghitung Maximum Likelihood Estimation (MLE) untuk parameter θ 
    pada distribusi Bernoulli.
    
    Rumus: θ̂ = k / n
    dengan:
        k = jumlah sukses (nilai 1) dalam data
        n = total jumlah observasi
    
    Referensi: Tsun (2020), hal. 45
    
    Args:
        data (List[int]): Daftar nilai observasi Bernoulli (0 atau 1)
    
    Returns:
        Dict[str, float]: Dictionary berisi estimasi parameter θ
    """
    # Menghitung jumlah data (n)
    n = len(data)
    
    # Menghitung jumlah sukses (k) dengan fungsi sum()
    k = sum(data)
    
    # Menghitung MLE: θ̂ = k / n
    # Nilai default 0.0 jika data kosong untuk menghindari division by zero
    theta_hat = k / n if n > 0 else 0.0
    
    # Mengembalikan hasil dalam bentuk dictionary
    return {'theta': theta_hat}


def log_likelihood_bernoulli(theta: float, k: int, n: int) -> float:
    """
    Menghitung nilai log-likelihood untuk distribusi Bernoulli.
    
    Rumus: ℓ(θ) = k·ln(θ) + (n-k)·ln(1-θ)
    
    Referensi: Tsun (2020), hal. 47
    
    Args:
        theta (float): Parameter θ yang akan diuji
        k (int): Jumlah sukses
        n (int): Total jumlah observasi
    
    Returns:
        float: Nilai log-likelihood
    """
    # Menangani kasus ekstrim (theta = 0 atau theta = 1)
    # Nilai log(0) = -∞, sehingga perlu penanganan khusus
    if theta <= 0 or theta >= 1:
        return -np.inf
    
    # Menghitung log-likelihood: k·ln(θ) + (n-k)·ln(1-θ)
    log_likelihood = k * np.log(theta) + (n - k) * np.log(1 - theta)
    
    return log_likelihood


# ============================================================================
# 2. FUNGSI UNTUK DISTRIBUSI POISSON
# ============================================================================

def mle_poisson(data: List[int]) -> Dict[str, float]:
    """
    Menghitung Maximum Likelihood Estimation (MLE) untuk parameter λ 
    pada distribusi Poisson.
    
    Rumus: λ̂ = (1/n) · Σ x_i = rata-rata (mean) dari data
    
    Referensi: Tsun (2020), hal. 52
    
    Args:
        data (List[int]): Daftar nilai observasi Poisson (bilangan cacah)
    
    Returns:
        Dict[str, float]: Dictionary berisi estimasi parameter λ
    """
    # Menghitung jumlah data (n)
    n = len(data)
    
    # Menghitung MLE: λ̂ = mean(data) = (Σ x_i) / n
    lambda_hat = np.mean(data) if n > 0 else 0.0
    
    return {'lambda': lambda_hat}


def log_likelihood_poisson(lambda_val: float, data: List[int]) -> float:
    """
    Menghitung nilai log-likelihood untuk distribusi Poisson.
    
    Rumus: ℓ(λ) = Σ [ x_i·ln(λ) - λ - ln(x_i!) ]
    
    Referensi: Tsun (2020), hal. 54
    
    Args:
        lambda_val (float): Parameter λ yang akan diuji
        data (List[int]): Daftar nilai observasi Poisson
    
    Returns:
        float: Nilai log-likelihood
    """
    # Menangani parameter λ ≤ 0 (tidak valid)
    if lambda_val <= 0:
        return -np.inf
    
    # Inisialisasi total log-likelihood
    total_log_likelihood = 0.0
    
    # Iterasi setiap observasi untuk menghitung kontribusinya
    for x in data:
        # Menghitung ln(x!) menggunakan fungsi log gamma
        # log_gamma(x+1) = ln(x!)
        log_factorial = math.lgamma(x + 1)
        
        # Kontribusi observasi: x·ln(λ) - λ - ln(x!)
        contribution = x * np.log(lambda_val) - lambda_val - log_factorial
        
        # Akumulasi ke total
        total_log_likelihood += contribution
    
    return total_log_likelihood


# ============================================================================
# 3. FUNGSI UNTUK POSTERIOR BETA (BAYESIAN)
# ============================================================================

def beta_posterior(k: int, m: int, alpha_prior: float = 1.0, beta_prior: float = 1.0) -> Dict[str, float]:
    """
    Menghitung parameter posterior distribusi Beta untuk model binomial.
    
    Distribusi Beta adalah conjugate prior untuk distribusi Bernoulli/Binomial.
    
    Rumus:
        - Prior: Beta(α₀, β₀)
        - Posterior: Beta(α₀ + k, β₀ + (m - k))
        - Mode posterior = (α - 1) / (α + β - 2)  untuk α > 1, β > 1
        - Mean posterior = α / (α + β)
    
    dengan:
        k = jumlah sukses
        m = total percobaan (n)
        α₀ = parameter alpha prior (default = 1 untuk prior uniform)
        β₀ = parameter beta prior (default = 1 untuk prior uniform)
    
    Referensi: Tsun (2020), hal. 78-82
    
    Args:
        k (int): Jumlah sukses
        m (int): Total jumlah percobaan
        alpha_prior (float): Parameter α prior (default: 1.0)
        beta_prior (float): Parameter β prior (default: 1.0)
    
    Returns:
        Dict[str, float]: Dictionary berisi:
            - 'alpha': parameter α posterior
            - 'beta': parameter β posterior
            - 'mode': mode distribusi posterior
            - 'mean': mean distribusi posterior
    """
    # Validasi input
    if m <= 0:
        raise ValueError("Total percobaan (m) harus > 0")
    if k < 0 or k > m:
        raise ValueError("Jumlah sukses (k) harus antara 0 dan m")
    
    # 1. Menghitung parameter posterior
    # α_posterior = α_prior + k
    alpha_post = alpha_prior + k
    
    # β_posterior = β_prior + (m - k)
    beta_post = beta_prior + (m - k)
    
    # 2. Menghitung mode posterior
    # Mode Beta(α,β) = (α - 1) / (α + β - 2) untuk α > 1 dan β > 1
    if alpha_post > 1 and beta_post > 1:
        mode_post = (alpha_post - 1) / (alpha_post + beta_post - 2)
    else:
        # Jika α atau β ≤ 1, mode tidak terdefinisi dengan rumus tersebut
        # Alternatif: menggunakan nilai di mana PDF mencapai maksimum
        from scipy.optimize import minimize_scalar
        def neg_beta_pdf(x):
            return -beta.pdf(x, alpha_post, beta_post)
        result = minimize_scalar(neg_beta_pdf, bounds=(0, 1), method='bounded')
        mode_post = result.x if result.success else (alpha_post - 1) / (alpha_post + beta_post - 2)
    
    # 3. Menghitung mean posterior
    # Mean Beta(α,β) = α / (α + β)
    mean_post = alpha_post / (alpha_post + beta_post)
    
    # Mengembalikan semua hasil dalam dictionary
    return {
        'alpha': alpha_post,
        'beta': beta_post,
        'mode': mode_post,
        'mean': mean_post
    }
