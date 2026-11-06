# AQRS — Complete model and tool catalog

**Status:** Normative **decision register** for all methods discussed during project planning. This is explicitly **not a requirement to install every model**, nor evidence that any model is implemented. Model names and external source URLs are documented for future evaluation. English is the project language; native Windows and Linux/CPU feasibility are release constraints.

> **Rule:** Codex may not silently forget any cataloged candidate. By its assigned gate each must have an explicit decision: implemented, independently benchmarked, blocked by a verifiable prerequisite, or deliberately deferred. Only CORE requires product functionality; EVALUATE requires an **assessment**, not compulsory installation.

Machine-readable companion: [`../configs/model_tool_registry.json`](../configs/model_tool_registry.json). Evaluation protocol: [`MODEL_EVALUATION_PROTOCOL.md`](MODEL_EVALUATION_PROTOCOL.md). Linux rules: [`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md).

## Meaning of decisions

| Status | Commitment |
|---|---|
| **CORE** | A working, tested basic capability exists by the named gate. |
| **EVALUATE** | By that gate supply a reproducible comparison to the named baseline, or a reasoned and testable no-go/BLOCKED report. Adopt only with demonstrated incremental value. |
| **CONDITIONAL** | Registered tool; enable only when data, compute, license and a positive research case justify it. |
| **DEFERRED** | Explicitly outside mandatory v1.0 scope; separate authorization required later. |

## A. Predictive models and statistical baselines

| Model / method | Library | First gate | Status | Research role and fair baseline |
|---|---|---|---|---|
| [Zero-return prediction / No Trade](https://numpy.org/) | `Custom rules / NumPy` | M0/v0.1 | **CORE** | Essential null hypothesis and economic control; baseline: None |
| [Linear / Ridge / Logistic Regression](https://scikit-learn.org/) | `scikit-learn` | M0/v0.1 | **CORE** | Simple, interpretable predictive baseline; baseline: Zero-return predictor |
| [Momentum / Mean Reversion / Decision Tree](https://scikit-learn.org/) | `scikit-learn + custom rules` | M0/v0.1 | **CORE** | Rule-based trading baseline; ablations and controls; baseline: No Trade / matched control |
| [Random Forest](https://scikit-learn.org/) | `scikit-learn` | M2/v0.3 | **EVALUATE** | Tree-based challenger without boosting; baseline: Ridge and shallow trees |
| [LightGBM (GBDT)](https://github.com/lightgbm-org/LightGBM) | `lightgbm` | M2/v0.3 | **EVALUATE** | Fast nonlinear feature and forward-return prediction on CPU; baseline: Ridge, shallow tree, net-cost baseline |
| [XGBoost (GBDT)](https://github.com/dmlc/xgboost) | `xgboost` | M2/v0.3 | **EVALUATE** | LightGBM challenger with the same prediction target; baseline: LightGBM + Ridge |
| [CatBoost (GBDT)](https://github.com/catboost/catboost) | `catboost` | M2/v0.3 | **CONDITIONAL** | Alternative when meaningful categorical variables exist; baseline: LightGBM + Ridge |

## B. Unsupervised discovery, anomalies and regimes

**Critical distinction:** clustering, regime labeling and anomaly scores are **hypothesis generators**, not alpha. Only a causally available condition with independent incremental predictive and net-tradable value against appropriate controls can qualify.

| Model / method | Library | First gate | Status | Research role and fair baseline |
|---|---|---|---|---|
| [Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) | `scikit-learn` | M2/v0.3 | **EVALUATE** | Identify unusual market states; NOT alpha by itself; baseline: Simple rarity/quantile filters and random events |
| [PCA and Residual Models](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) | `scikit-learn / custom regression` | M2/v0.3 | **EVALUATE** | Remove common factors and investigate unusual residuals; baseline: Single-asset and linear baselines |
| [K-Means](https://scikit-learn.org/) | `scikit-learn` | M2/v0.3 | **CONDITIONAL** | Explore state clusters and conditional returns; baseline: Quantile buckets / simple clustering baseline |
| [Gaussian Mixture Models (GMM)](https://scikit-learn.org/) | `scikit-learn` | M2/v0.3 | **CONDITIONAL** | Soft-cluster and market-regime probabilities; baseline: K-Means / volatility buckets |
| [HDBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html) | `scikit-learn.cluster.HDBSCAN / hdbscan` | M2/v0.3 | **EVALUATE** | Detect rare state clusters and noise points without fixed cluster count; baseline: Quantile buckets, K-Means, Isolation Forest |
| [Hidden Markov Models (HMM)](https://github.com/hmmlearn/hmmlearn) | `hmmlearn (verify maintenance status)` | M2/v0.3 | **CONDITIONAL** | Evaluate latent market regimes and conditional predictive value; baseline: Rolling volatility/trend buckets |
| [Autoencoder (small MLP)](https://github.com/pytorch/pytorch) | `PyTorch` | M2/v0.3 | **EVALUATE** | Use reconstruction errors and latent features as anomaly hypotheses; baseline: PCA, Isolation Forest, simple statistics |

## C. Deep models for sequences, order books and graphs

**Caution:** PatchTST began as a general time-series forecasting architecture; DeepLOB is an order-book research implementation. Neither a published architecture nor an attractive backtest proves live intraday profitability.

| Model / method | Library | First gate | Status | Research role and fair baseline |
|---|---|---|---|---|
| [LSTM / GRU](https://github.com/unit8co/darts) | `PyTorch / Darts` | M2/v0.3 | **CONDITIONAL** | Learn sequential dependencies from longer windows; baseline: LightGBM on lagged features, Ridge, TCN |
| [Temporal Convolutional Networks (TCN)](https://github.com/unit8co/darts) | `Darts / PyTorch` | M2/v0.3 | **CONDITIONAL** | Learn causal sequence features as an alternative to LSTM; baseline: Lagged LightGBM and LSTM |
| [Temporal Fusion Transformer (TFT)](https://github.com/sktime/pytorch-forecasting) | `PyTorch Forecasting / Darts` | M2/v0.3 | **CONDITIONAL** | Model multivariate covariates and multi-horizon forecasts; baseline: LightGBM / TCN |
| [PatchTST](https://github.com/yuqinie98/PatchTST) | `yuqinie98/PatchTST / Darts` | M2/v0.3 | **CONDITIONAL** | Patch-based time-series transformer representations; baseline: Lagged LightGBM / TCN |
| [General Time-Series Transformers](https://github.com/unit8co/darts) | `PyTorch / Darts` | M2/v0.3 | **CONDITIONAL** | Learn temporal representations instead of engineered features; baseline: LSTM/TCN, LightGBM |
| [DeepLOB (CNN/LSTM-style architecture)](https://github.com/zcakhaa/DeepLOB-Deep-Convolutional-Neural-Networks-for-Limit-Order-Books) | `Research implementation + PyTorch` | M1/v0.2 | **CONDITIONAL** | Limit-order-book representations for short-horizon research; baseline: Order-flow imbalance/LOB statistics, LightGBM |
| [Graph Neural Networks (GNN)](https://github.com/pyg-team/pytorch_geometric) | `PyTorch Geometric` | M2/v0.3 | **CONDITIONAL** | Cross-asset, supply-chain and market-graph dependencies; baseline: Correlation and linear residuals |

## D. Financial text, NLP and LLMs

| Model / method | Library | First gate | Status | Research role and fair baseline |
|---|---|---|---|---|
| [FinBERT](https://github.com/ProsusAI/finBERT) | `ProsusAI/finBERT / Hugging Face` | M1/v0.2 | **CONDITIONAL** | Timestamped financial-news sentiment features; baseline: Lexicons, trivial sentiment/event control |
| [LLM/BERT Embeddings and Structured Text Extraction](https://github.com/huggingface/transformers) | `Transformers / sentence-transformers` | M1/v0.2 | **CONDITIONAL** | Features from news, filings and earnings events; baseline: Text categories / sentiment without an LLM |
| [gpt-oss (local open-weight language models)](https://github.com/openai/gpt-oss) | `openai/gpt-oss` | M8/v0.9 | **DEFERRED** | Optional local LLM feature extractor, not a required trading agent; baseline: Small text model / FinBERT |

**FinBERT licensing safeguard:** repository code, model weights and training data may carry different licenses. Check each license separately before deployment or redistribution. Publication timestamps and realistic processing delays are essential; text must never be available before release.

## E. Decisions, research optimization and reinforcement learning

| Model / method | Library | First gate | Status | Research role and fair baseline |
|---|---|---|---|---|
| [Model Predictive Control (MPC)](https://scipy.org/) | `Custom optimization / SciPy` | M5/v0.6 | **CONDITIONAL** | Multi-step decisions subject to position and trading-cost paths; baseline: Simple rule-based decision policy |
| [Classical Position and Risk Optimization](https://scipy.org/) | `NumPy / SciPy` | M5/v0.6 | **CORE** | Optimize net value, risk, no-trade and turnover separately from forecasts; baseline: Fixed-size policy + No Trade |
| [Optuna (Bayesian/TPE-style search)](https://github.com/optuna/optuna) | `Optuna` | M3/v0.4 | **CONDITIONAL** | Budgeted hyperparameter tuning within research folds only; baseline: Small predefined grid or defaults |
| [Multi-Armed Bandits (UCB/Thompson etc.)](https://www.jmlr.org/papers/volume3/auer02a/auer02a.pdf) | `Small custom implementation / optional bandit library` | M3/v0.4 | **CONDITIONAL** | Allocate research budget across exploration and exploitation; baseline: Static scheduler |
| [Successive Halving / Hyperband](https://scikit-learn.org/stable/modules/grid_search.html) | `scikit-learn / Optuna` | M3/v0.4 | **EVALUATE** | Inexpensive screening before expensive experiments; baseline: Static scheduler under the same budget |
| [Columns / Filter-based Strategy Cruncher (Mabe-style)](https://scikit-learn.org/) | `Custom decision-tree / threshold search` | M2/v0.3 | **CONDITIONAL** | Generate interpretable rules over broad candidate sets; baseline: Small decision tree and LightGBM |
| [PPO / SAC / A2C / TD3](https://github.com/DLR-RM/stable-baselines3) | `Stable-Baselines3` | POST-v1.0 | **DEFERRED** | Learn trading/execution policies; not a promise of alpha; baseline: Classical policy, optionally MPC |
| [FinRL (RL Trading Framework)](https://github.com/AI4Finance-Foundation/FinRL) | `AI4Finance-Foundation/FinRL` | POST-v1.0 | **DEFERRED** | Potential RL research environment, not a default dependency; baseline: Deterministic in-house environment |

**Distinct roles:** LightGBM optimizes a *forecast*, Optuna searches *hyperparameters*, bandits allocate a *research budget*, MPC optimizes *multi-step choices*, and RL learns a *policy*. They are not interchangeable “better AI models.” PPO/SAC/A2C/TD3 and FinRL remain deferred past v1.0 until a credible simulator and simpler decision baselines exist.

## F. Data, experiment and engineering tools

| Tool | Role | First gate | Status | Official source |
|---|---|---|---|---|
| **Python 3.11+** | Python package, CLI and CPU-first runtime | M0/v0.1 | **CORE** | [Documentation](https://www.python.org/) |
| **NumPy** | Numerical computation and deterministic random seeds | M0/v0.1 | **CORE** | [Documentation](https://numpy.org/) |
| **pandas** | OHLCV and feature processing using one DataFrame stack | M0/v0.1 | **CORE** | [Documentation](https://pandas.pydata.org/) |
| **Polars** | Alternative if memory/speed bottlenecks are demonstrated | M7/v0.8 | **CONDITIONAL** | [Documentation](https://github.com/pola-rs/polars) |
| **PyArrow / Parquet** | Columnar local Parquet storage | M0/v0.1 | **CORE** | [Documentation](https://arrow.apache.org/) |
| **DuckDB** | SQL directly over Parquet where justified | M1/v0.2 | **CONDITIONAL** | [Documentation](https://duckdb.org/) |
| **SQLite** | Persistent research journal and status tracking | M0/v0.1 | **CORE** | [Documentation](https://www.sqlite.org/) |
| **scikit-learn** | Baseline models, preprocessing and classical ML | M0/v0.1 | **CORE** | [Documentation](https://scikit-learn.org/) |
| **PyTorch** | Autoencoders, LSTM, TCN, DeepLOB and transformers | M2/v0.3 | **CONDITIONAL** | [Documentation](https://pytorch.org/) |
| **Darts** | Convenient time-series model comparison, not a required framework | M2/v0.3 | **CONDITIONAL** | [Documentation](https://github.com/unit8co/darts) |
| **PyTorch Forecasting** | TFT and deep time-series tooling | M2/v0.3 | **CONDITIONAL** | [Documentation](https://github.com/sktime/pytorch-forecasting) |
| **hmmlearn** | HMM tooling; review maintenance status before adoption | M2/v0.3 | **CONDITIONAL** | [Documentation](https://github.com/hmmlearn/hmmlearn) |
| **PyTorch Geometric** | Graph neural network framework | M2/v0.3 | **CONDITIONAL** | [Documentation](https://github.com/pyg-team/pytorch_geometric) |
| **Hugging Face Transformers** | Text and embedding models; separately verify weights/text licenses | M1/v0.2 | **CONDITIONAL** | [Documentation](https://github.com/huggingface/transformers) |
| **MLflow** | Optional experiment UI/artifact management; SQLite remains authoritative | M7/v0.8 | **CONDITIONAL** | [Documentation](https://github.com/mlflow/mlflow) |
| **pytest** | Tests for causality, costs, data, journaling and release gates | M0/v0.1 | **CORE** | [Documentation](https://github.com/pytest-dev/pytest) |
| **Ruff** | Linting and code hygiene | M0/v0.1 | **CORE** | [Documentation](https://github.com/astral-sh/ruff) |
| **Git / Git SHA** | Source versioning and experiment provenance | M0/v0.1 | **CORE** | [Documentation](https://git-scm.com/) |
| **Eigene reproduzierbare Python-Runner/Backtestlogik** | Reproducible Python runner/backtester with causal event/fill semantics | M0/v0.1 | **CORE** | [Documentation](https://docs.python.org/3/) |

## G. Milestones and minimum commitments

| Gate | Required capability | Not required |
|---|---|---|
| **M0/v0.1** | Linear, null and rule controls plus a causally correct pipeline; catalog and registry are available/versioned. | Install LightGBM, HDBSCAN or PyTorch now. |
| **M1/v0.2** | Real data, availability and cost contract; decide whether order-book, text or cross-asset data are accessible. | Train DeepLOB or FinBERT without valid source data. |
| **M2/v0.3** | Demonstrate at least one **supervised** challenger (LightGBM) and one **unsupervised** hypothesis generator (Isolation Forest), compared with simple baselines. XGBoost, HDBSCAN, PCA, autoencoders and Random Forest receive testable evaluation or blocker decisions and bounded pilots if feasible. | Put every model into production. |
| **M3/v0.4** | Compare a bounded multi-stage scheduler against a fixed schedule; evaluate Successive Halving. Optuna/bandits only where value is evidenced. | Make RL a research scheduler. |
| **M4/v0.5** | Apply statistics, controls and multiple-testing safeguards to **all** model families, attempts and windows. | Exempt complex models from research standards. |
| **M5/v0.6** | Classical cost/risk-aware decision optimization; MPC only after a credible need is shown. | PPO/SAC automatic trader. |
| **M6/v0.7–M7/v0.8** | Monitor/version active models and anomaly detectors, capture costs and ensure reproducible operations. | Require GPUs/cloud or load all model families at once. |
| **M8/v0.9–M9/v1.0** | Audit **every** registry entry and record `ADOPTED`/`REJECTED`/`DEFERRED`/`BLOCKED_*` decision; integrated benchmark. At least one supervised and one unsupervised discovery variant works in the supported test environment. | Make all 32 models profitable, deployed or even useful. |

## H. Model adoption and rejection criteria

Before a pilot, record: research question, necessary data, early costs, accepted wall/RAM budget, baseline, forecast/net metrics, statistical plan, chronological folds, tuning budget, attempt count and train-only fitting. Afterwards assign `ADOPTED`, `REJECTED`, `DEFERRED`, `BLOCKED_DATA`, `BLOCKED_LICENSE` or `BLOCKED_RESOURCES` with run ID and justification. **Incremental independent value governs adoption, not the model name.**

## I. Specific technical risks

- HDBSCAN on millions of observations and large neural models can exhaust CPU/RAM. Profile first, sample when justified, and obey the Resource Governor.
- Regime/HMM methods must see only historical information in each fold; no full-series Viterbi smoothing used as a supposed real-time signal.
- Autoencoders, PCA, K-Means, GMM and HDBSCAN fit scaling/representation only on training periods. Check how unseen observations will be scored. HDBSCAN may require a separate prediction API and is not automatically an online classifier.
- Order-book networks need sufficiently complete, legally usable L2/L3 streams and realistic fills; OHLCV is not enough.
- FinBERT/LLM features require licensed, precisely timestamped texts and no retrospective availability before publication.
- Compare CatBoost/LightGBM/XGBoost/neural networks with identical time windows, costs, validation standards and explicit tuning budgets; tuning is part of multiple testing.
- RL and FinRL are not required through v1.0. Simulation profits without a credible decision environment are weak evidence.
- Windows/Linux/CPU wheel availability and memory footprint are adoption prerequisites. Optional dependencies must not break a clean native Windows or headless Linux M0 install.

## J. Sources and verification date

Links point to official projects or relevant reference implementations. Re-check versions, licenses, wheels and maintenance **at actual adoption time**; this document is not a license grant. Catalog baseline date: **November 6, 2026**.

## K. Resource Governor: cross-cutting requirement for **all** models

This catalog is **not** an instruction to calibrate 32 models one after another. Each trial must declare its fits, folds, seeds and parameter combinations, and the Resource Governor must measure or conservatively estimate total runtime and RAM before starting. Data/license/compute-constrained methods receive `BLOCKED_*`/`DEFERRED`, **not** stealthy unlimited calibration. Automated reruns without a new approved budget are prohibited. See [`RESOURCE_GOVERNOR.md`](RESOURCE_GOVERNOR.md).
