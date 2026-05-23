# 📊 Open Source Analytics: Issue Frequency & Contributor Diversity in pandas

Analisis dinamika kontribusi open-source pada repositori **pandas-dev/pandas** menggunakan data *closed issues* dan *merged pull requests*. Proyek ini memodelkan frekuensi issue yang mengikuti **distribusi Poisson** dan mengukur **keberagaman kontributor** (*contributor diversity*) untuk memahami faktor-faktor yang mempengaruhi produktivitas dan keberlanjutan proyek open-source.

---

## 🎯 Project Description

Proyek ini bertujuan untuk menganalisis pola aktivitas dan kolaborasi dalam repositori open-source pandas. Dengan memanfaatkan:

- **Issue frequency** yang mengikuti distribusi Poisson
- **Contributor diversity** yang diukur menggunakan Shannon/Simpson index

Proyek ini membangun model statistik dan simulasi dalam **tiga lapisan utama**:

| Layer | Tujuan |
|-------|--------|
| **Estimation** | Mengestimasi rata-rata issue per minggu dan tingkat keberagaman kontributor |
| **Inference** | Menguji perbedaan diversity antara periode high vs low issue frequency |
| **Simulation** | Memproyeksikan diversity di masa depan berdasarkan parameter historis |

Data diperoleh melalui **GitHub API** crawling, mencakup informasi temporal, identitas kontributor, dan asosiasi mereka dengan proyek (MEMBER, CONTRIBUTOR, NONE).

---

## 🔬 Research Questions

### 1. Estimation Layer
Berapa probabilitas sebuah PR di-merge, dan seberapa tidak pasti estimasi tersebut?

### 2. Inference / Testing Layer
Apakah rata-rata jumlah komentar berbeda secara signifikan antara PR yang merged vs unmerged?

### 3. Simulation Layer
Berapa probabilitas sebuah issue butuh lebih dari 30 hari untuk ditutup?

---

## 📈 Key Findings


## How To Run


## Team Table
| Nama                   | NIM          |
|------------------------|--------------|
| Raynar Usman Annafis   | 15196250xx   | 
| Zaky Aditya Susanto    | 1519625023   |
| Bethelina Imanuella Y  | 1519625014   |
| Kirana Cinta Mentari   | 1519625021   | 
| Luqman                 | 15196250xx   | 
