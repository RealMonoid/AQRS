from math import isfinite
from pathlib import Path

import yaml

from aqrs.market import FEATURE_NAMES

SECTIONS = {
    "project": "name seed artifact_dir",
    "market": "source symbol scenario bar_minutes n_bars timezone",
    "research": "horizon_bars train_bars validation_bars walk_forward_folds final_holdout_fraction candidates",
    "resource_governor": (
        "enabled fail_closed_on_unenforceable_limits max_research_trials_per_campaign "
        "max_model_fits_per_campaign max_seeds max_parallel_trials max_wall_seconds_per_trial "
        "max_wall_seconds_per_campaign max_peak_rss_mb_per_trial auto_retry_count preflight"
    ),
    "execution_simulation": (
        "price_reference exit_after_horizon_bars allow_short max_open_positions notional_per_trade"
    ),
    "costs": "fee_bps_per_side quoted_spread_bps slippage_bps_per_side decision_buffer_bps",
    "journal": "sqlite_path",
    "reporting": "write_json write_markdown",
}


class UniqueKeysLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        if len(mapping) != len(node.value):
            raise ValueError("Duplicate YAML mapping keys are forbidden.")
        return mapping


def fields(value: object, required: str, optional: str = "") -> None:
    keys = set(required.split())
    if not isinstance(value, dict) or not keys <= value.keys() <= keys | set(
        optional.split()
    ):
        raise ValueError(f"Expected configuration fields: {required}.")


def integer(section: dict, key: str, low: int = 1, high: int = 10**9) -> None:
    value = section[key]
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{key} must be an integer from {low} through {high}.")


def number(section: dict, key: str, low: float, high: float) -> None:
    value = section[key]
    if (
        type(value) not in (int, float)
        or not low <= value <= high
        or not isfinite(value)
    ):
        raise ValueError(f"{key} must be a finite number from {low} through {high}.")


def exact(section: dict, key: str, expected: object) -> None:
    if type(section[key]) is not type(expected) or section[key] != expected:
        raise ValueError(f"M0 requires {key}={expected!r}.")


def string(section: dict, key: str) -> None:
    if not isinstance(section[key], str) or not section[key].strip():
        raise ValueError(f"{key} must be a nonempty string.")


def load(path: Path) -> tuple[dict, Path]:
    try:
        config = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeysLoader)
    except (yaml.YAMLError, TypeError) as error:
        raise ValueError("Configuration is not valid YAML.") from error
    fields(config, " ".join(SECTIONS))
    for section, keys in SECTIONS.items():
        optional = {"project": "path_base", "resource_governor": "memory_mode"}.get(
            section, ""
        )
        fields(config[section], keys, optional)

    project, market, research = (
        config[key] for key in ("project", "market", "research")
    )
    project.setdefault("path_base", ".")
    for key in ("name", "artifact_dir", "path_base"):
        string(project, key)
    integer(project, "seed", 0, 2**32 - 1)
    for key, value in {
        "source": "synthetic",
        "scenario": "null",
        "timezone": "UTC",
    }.items():
        exact(market, key, value)
    string(market, "symbol")
    integer(market, "n_bars", 20, 100_000)
    integer(market, "bar_minutes", 1, 1440)
    for key in ("horizon_bars", "train_bars", "validation_bars", "walk_forward_folds"):
        integer(research, key, 1, 100_000)
    number(research, "final_holdout_fraction", 0.01, 0.90)
    validate_candidates(research["candidates"])
    validate_governor(config["resource_governor"])

    execution = config["execution_simulation"]
    exact(execution, "price_reference", "next_bar_open")
    exact(execution, "exit_after_horizon_bars", True)
    exact(execution, "max_open_positions", 1)
    if type(execution["allow_short"]) is not bool:
        raise ValueError("allow_short must be boolean.")
    number(execution, "notional_per_trade", 1e-12, 1e9)
    for key in config["costs"]:
        number(config["costs"], key, 0, 10_000)
    string(config["journal"], "sqlite_path")
    for key in config["reporting"]:
        exact(config["reporting"], key, True)
    return config, (path.resolve().parent / project["path_base"]).resolve()


def validate_candidates(candidates: object) -> None:
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("Configure at least one explicit Ridge candidate.")
    seen = set()
    for candidate in candidates:
        fields(candidate, "id model features")
        string(candidate, "id")
        exact(candidate, "model", "ridge")
        features = candidate["features"]
        if (
            not isinstance(features, list)
            or not features
            or any(name not in FEATURE_NAMES for name in features)
            or len(features) != len(set(features))
        ):
            raise ValueError(
                "Candidate features must be a unique subset of supported names."
            )
        if candidate["id"] in seen:
            raise ValueError("Candidate IDs must be unique.")
        seen.add(candidate["id"])


def validate_governor(limits: dict) -> None:
    limits.setdefault("memory_mode", "observed_rss")
    if limits["memory_mode"] not in ("observed_rss", "strict"):
        raise ValueError("memory_mode must be observed_rss or strict.")
    exact(limits, "enabled", True)
    exact(limits, "fail_closed_on_unenforceable_limits", True)
    exact(limits, "auto_retry_count", 0)
    exact(limits, "max_parallel_trials", 1)
    for key in (
        "max_research_trials_per_campaign",
        "max_model_fits_per_campaign",
        "max_seeds",
    ):
        integer(limits, key)
    for key in ("max_wall_seconds_per_trial", "max_wall_seconds_per_campaign"):
        number(limits, key, 0.01, 86_400)
    number(limits, "max_peak_rss_mb_per_trial", 1, 1e6)
    preflight = limits["preflight"]
    fields(
        preflight,
        "enabled require_explicit_fit_count measure_representative_pilot "
        "runtime_estimate_safety_factor reject_if_estimated_over_budget",
    )
    for key in (
        "enabled",
        "require_explicit_fit_count",
        "reject_if_estimated_over_budget",
    ):
        exact(preflight, key, True)
    if type(preflight["measure_representative_pilot"]) is not bool:
        raise ValueError("measure_representative_pilot must be boolean.")
    number(preflight, "runtime_estimate_safety_factor", 1, 100)
