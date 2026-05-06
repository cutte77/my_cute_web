from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import streamlit as st


@dataclass(frozen=True)
class Scenario:
    name: str
    label: str
    core_task: str
    environment: tuple[str, ...]
    hard_constraints: tuple[str, ...]
    wishlist_category: str
    default_sitting: bool = False
    default_walking: bool = False
    default_standing: bool = False


SCENARIOS: dict[str, Scenario] = {
    "exam_sprint": Scenario(
        name="考证冲刺 / 防御态",
        label="🟢 考证冲刺 / 防御态",
        core_task="长时间静坐学习，维持专注和身体稳定",
        environment=("空调房", "图书馆", "自习室", "久坐8小时"),
        hard_constraints=("腹部压迫", "温度不可调", "频繁整理衣物"),
        wishlist_category="未来低任务密度社交",
        default_sitting=True,
    ),
    "city_walk": Scenario(
        name="城市游荡 / 观察态",
        label="🔵 城市游荡 / 观察态",
        core_task="长距离步行、观察城市、保持身体自由",
        environment=("户外", "地铁", "街道", "河边", "长线步道"),
        hard_constraints=("鞋底无支撑", "包容量不足", "衣物行动受限"),
        wishlist_category="短时拍照或低步行场景",
        default_walking=True,
    ),
    "social_defense": Scenario(
        name="社交防御 / 武装态",
        label="🟣 社交防御 / 武装态",
        core_task="维持边界感、体面感和心理安全区",
        environment=("社交场合", "咖啡店", "聚会", "陌生人环境"),
        hard_constraints=("过度暴露", "需要持续端着", "行动不自在"),
        wishlist_category="高能量日社交",
        default_standing=True,
    ),
    "low_energy_day": Scenario(
        name="低能量日 / 保命态",
        label="⚪ 低能量日 / 保命态",
        core_task="减少决策疲劳和身体噪音",
        environment=("通勤", "短途出门", "低社交需求"),
        hard_constraints=("频繁整理衣物", "明显身体压迫", "温度失控"),
        wishlist_category="高能量日再评估",
    ),
}


DURATION_WEIGHTS = {
    "2小时以内": 1,
    "4小时左右": 2,
    "8小时以上": 3,
}

BODY_STATES = ["正常", "胃胀", "经期", "睡眠不足", "低能量", "怕冷", "怕热", "脚痛/膝盖疲劳"]
WEATHER_STATES = ["冷", "热", "温差大", "空调房", "雨天", "强日晒", "拥挤通勤"]

WAIST_TAGS = ["高腰压腹/硬腰头", "紧身裤/无弹力牛仔", "硬质腰带", "松紧腰/软腰头", "宽松直筒/半裙"]
SHOE_TAGS = ["薄底鞋", "硬底小皮鞋", "无缓冲平底鞋", "新鞋", "高跟鞋", "运动鞋/足弓支撑"]
THERMAL_TAGS = ["单件厚衣", "无法叠穿", "闷汗材质", "露肤偏多", "可叠穿/可脱卸", "透气材质"]
MOBILITY_TAGS = ["窄裙/迈不开步", "紧身上衣/抬手受限", "肩带易滑/包带打架", "包容量不足", "无口袋", "行动自由"]
MAINTENANCE_TAGS = ["需要频繁整理", "容易走光", "容易皱", "浅色易脏", "贵重怕刮/怕雨", "低维护"]
SOCIAL_TAGS = ["高识别度/吸睛", "需要持续端着", "过度暴露/边界感不足", "低饱和/人群隐蔽", "有外套/边界感"]

ABORT = "ABORT"
WARNING = "WARNING"
PASS = "PASS"

NOTE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "高腰压腹/硬腰头": ("高腰", "压腹", "硬腰头", "腰很紧", "腰紧"),
    "紧身裤/无弹力牛仔": ("紧身裤", "无弹力", "牛仔裤", "牛仔"),
    "硬质腰带": ("腰带", "皮带"),
    "松紧腰/软腰头": ("松紧腰", "软腰头"),
    "宽松直筒/半裙": ("宽松", "直筒", "半裙"),
    "薄底鞋": ("薄底", "薄底鞋"),
    "硬底小皮鞋": ("硬底", "小皮鞋", "皮鞋"),
    "无缓冲平底鞋": ("平底鞋", "无缓冲"),
    "新鞋": ("新鞋", "第一次穿"),
    "高跟鞋": ("高跟", "高跟鞋"),
    "运动鞋/足弓支撑": ("运动鞋", "足弓", "支撑"),
    "单件厚衣": ("厚卫衣", "厚毛衣", "厚外套", "单件厚"),
    "无法叠穿": ("无法叠穿", "不能脱", "不好脱"),
    "闷汗材质": ("闷汗", "不透气", "皮革", "涤纶"),
    "露肤偏多": ("露肤", "短上衣", "吊带", "低领"),
    "可叠穿/可脱卸": ("开衫", "外套", "可脱", "叠穿"),
    "透气材质": ("棉", "亚麻", "透气"),
    "窄裙/迈不开步": ("窄裙", "包臀裙", "迈不开"),
    "紧身上衣/抬手受限": ("抬手", "紧身上衣", "肩膀紧"),
    "肩带易滑/包带打架": ("肩带滑", "包带", "背包打架"),
    "包容量不足": ("小包", "包太小", "装不下"),
    "无口袋": ("无口袋", "没有口袋"),
    "行动自由": ("行动自由", "好走", "方便"),
    "需要频繁整理": ("频繁整理", "总要整理", "需要整理"),
    "容易走光": ("走光", "怕露", "担心露"),
    "容易皱": ("容易皱", "皱"),
    "浅色易脏": ("浅色", "易脏", "白裤", "白裙"),
    "贵重怕刮/怕雨": ("怕刮", "怕雨", "贵", "真皮"),
    "低维护": ("低维护", "不用管", "耐脏"),
    "高识别度/吸睛": ("吸睛", "亮色", "夸张", "高识别"),
    "需要持续端着": ("端着", "不自在", "需要气场"),
    "过度暴露/边界感不足": ("过度暴露", "暴露", "边界感不足"),
    "低饱和/人群隐蔽": ("低饱和", "隐蔽", "不吸睛"),
    "有外套/边界感": ("外套", "边界感", "遮挡"),
}


def clamp(value: int | float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, int(round(value))))


def has_any(values: set[str], candidates: tuple[str, ...] | list[str]) -> bool:
    return any(candidate in values for candidate in candidates)


def label_for_risk(percent: int) -> str:
    if percent >= 85:
        return "高危摩擦"
    if percent >= 65:
        return "高摩擦"
    if percent >= 40:
        return "中摩擦"
    return "低摩擦"


def label_for_protection(percent: int) -> str:
    if percent >= 80:
        return "强保护"
    if percent >= 60:
        return "可用"
    if percent >= 40:
        return "偏低"
    return "失守"


def format_tags(tags: set[str], fallback: str = "未标记明显风险") -> str:
    return "、".join(sorted(tags)) if tags else fallback


def infer_tags_from_notes(notes: str) -> set[str]:
    if not notes:
        return set()

    normalized = notes.lower()
    inferred: set[str] = set()
    for tag, keywords in NOTE_KEYWORDS.items():
        if any(keyword.lower() in normalized for keyword in keywords):
            inferred.add(tag)
    return inferred


def build_constraint(
    name: str,
    status: str,
    evidence: str,
    impact: str,
    fix: str,
) -> dict[str, str]:
    icon = {ABORT: "🔴", WARNING: "🟡", PASS: "🟢"}[status]
    return {
        "name": name,
        "status": status,
        "status_icon": icon,
        "evidence": evidence,
        "impact": impact,
        "fix": fix,
    }


def analyze_outfit(inputs: dict[str, Any]) -> dict[str, Any]:
    scenario = SCENARIOS[inputs["scenario"]]
    duration_weight = DURATION_WEIGHTS[inputs["duration"]]
    body_states = set(inputs["body_states"])
    weather_states = set(inputs["weather_states"])
    if len(body_states) > 1:
        body_states.discard("正常")

    inferred_tags = infer_tags_from_notes(inputs.get("notes", ""))
    tags = set(inputs["tags"]) | inferred_tags

    sitting = inputs["sitting"]
    walking = inputs["walking"]
    standing = inputs["standing"]
    backpack = inputs["backpack"]

    pressure_tags = {
        "高腰压腹/硬腰头",
        "紧身裤/无弹力牛仔",
        "硬质腰带",
    }
    support_risk_tags = {
        "薄底鞋",
        "硬底小皮鞋",
        "无缓冲平底鞋",
        "新鞋",
        "高跟鞋",
    }
    thermal_risk_tags = {
        "单件厚衣",
        "无法叠穿",
        "闷汗材质",
        "露肤偏多",
    }
    mobility_risk_tags = {
        "窄裙/迈不开步",
        "紧身上衣/抬手受限",
        "肩带易滑/包带打架",
        "包容量不足",
        "无口袋",
    }
    maintenance_risk_tags = {
        "需要频繁整理",
        "容易走光",
        "容易皱",
        "浅色易脏",
        "贵重怕刮/怕雨",
    }
    boundary_risk_tags = {
        "高识别度/吸睛",
        "需要持续端着",
        "过度暴露/边界感不足",
    }

    constraints: list[dict[str, str]] = []

    pressure_hit = tags & pressure_tags
    pressure_sensitive = sitting or duration_weight == 3 or has_any(body_states, ("胃胀", "经期"))
    if pressure_hit and pressure_sensitive:
        status = ABORT if scenario.name in ("考证冲刺 / 防御态", "低能量日 / 保命态") or has_any(body_states, ("胃胀", "经期")) else WARNING
        constraints.append(
            build_constraint(
                "腹部压迫感",
                status,
                f"{format_tags(pressure_hit)}，腰腹区域存在持续压力源",
                "当前任务需要身体稳定。腹部压迫会占用注意力，可能影响呼吸、胃肠舒适度和久坐耐受。",
                "替换为松紧腰裤、软腰头长裤、垂感运动裤或宽松半裙。",
            )
        )
    elif pressure_hit:
        constraints.append(
            build_constraint(
                "腹部压迫感",
                WARNING,
                f"{format_tags(pressure_hit)}，但当前久坐压力较低",
                "短时可以执行，但外出时间一旦拉长，腰腹会先开始抗议。",
                "保留上装，优先替换腰头结构。",
            )
        )
    else:
        constraints.append(
            build_constraint(
                "腹部压迫感",
                PASS,
                "未标记硬腰头、压腹或无弹力下装",
                "腰腹区域不会成为当前任务的主要中断点。",
                "保持低压腰腹结构。",
            )
        )

    shoe_hit = tags & support_risk_tags
    foot_sensitive = walking or standing or duration_weight == 3 or "脚痛/膝盖疲劳" in body_states
    if shoe_hit and foot_sensitive:
        status = ABORT if scenario.name == "城市游荡 / 观察态" or walking or "脚痛/膝盖疲劳" in body_states else WARNING
        constraints.append(
            build_constraint(
                "脚部支撑",
                status,
                f"{format_tags(shoe_hit)}，足底缓冲和稳定性不足",
                "当前场景需要移动或站立。鞋底不支撑会把任务提前变成找座位、找车、想回家。",
                "替换为运动休闲鞋、厚底乐福鞋、有足弓支撑的短靴或已磨合鞋。",
            )
        )
    elif shoe_hit:
        constraints.append(
            build_constraint(
                "脚部支撑",
                WARNING,
                f"{format_tags(shoe_hit)}，但当前移动需求不高",
                "可短时执行，不适合临时加路程或长时间排队。",
                "把步行路线压短，或直接换成有缓冲的鞋。",
            )
        )
    else:
        constraints.append(
            build_constraint(
                "脚部支撑",
                PASS,
                "未标记薄底、硬底、新鞋或高跟风险",
                "脚部不太可能成为任务中断点。",
                "保持已磨合、可长时间移动的鞋。",
            )
        )

    thermal_hit = tags & thermal_risk_tags
    climate_sensitive = bool(weather_states & {"冷", "热", "温差大", "空调房", "雨天", "强日晒"}) or has_any(body_states, ("怕冷", "怕热"))
    if thermal_hit and climate_sensitive:
        status = ABORT if scenario.name in ("考证冲刺 / 防御态", "低能量日 / 保命态") and duration_weight == 3 and has_any(tags, ("单件厚衣", "无法叠穿")) else WARNING
        constraints.append(
            build_constraint(
                "温度调节",
                status,
                f"{format_tags(thermal_hit)}，今日环境为：{format_tags(weather_states, '未填写环境')}",
                "温度不可调会持续制造烦躁、怕冷或闷汗，直接削弱专注和行动效率。",
                "改成薄打底 + 开衫/衬衫外套/马甲，保证可穿脱和可散热。",
            )
        )
    elif thermal_hit:
        constraints.append(
            build_constraint(
                "温度调节",
                WARNING,
                f"{format_tags(thermal_hit)}，但环境波动不大",
                "如果当天出现空调、日晒或转场，舒适度会快速下降。",
                "增加一件可脱卸层，或替换为透气材质。",
            )
        )
    else:
        constraints.append(
            build_constraint(
                "温度调节",
                PASS,
                "未标记明显闷热、失温或无法叠穿问题",
                "温度不会明显干扰当前任务。",
                "继续保持可调节层次。",
            )
        )

    mobility_hit = tags & mobility_risk_tags
    if mobility_hit and (walking or backpack or standing or scenario.name == "城市游荡 / 观察态"):
        status = ABORT if has_any(mobility_hit, ("窄裙/迈不开步", "包容量不足")) and scenario.name == "城市游荡 / 观察态" else WARNING
        constraints.append(
            build_constraint(
                "行动效率",
                status,
                f"{format_tags(mobility_hit)}，与移动、背包或站立任务冲突",
                "行动受限会把普通转场变成持续摩擦：上楼、赶车、拿东西、坐下起身都会变慢。",
                "替换为可跨步下装、稳定肩带、足够容量的包，保留不影响动作的单品。",
            )
        )
    elif mobility_hit:
        constraints.append(
            build_constraint(
                "行动效率",
                WARNING,
                f"{format_tags(mobility_hit)}，但当前行动强度有限",
                "短时可用，任务密度上升后会变成负担。",
                "减少随身物品，或换掉限制最大的一件。",
            )
        )
    else:
        constraints.append(
            build_constraint(
                "行动效率",
                PASS,
                "未标记迈不开步、抬手受限、包带冲突或容量不足",
                "动作自由度可以支撑当前生活流。",
                "保持低摩擦动作结构。",
            )
        )

    self_monitor_hit = tags & (maintenance_risk_tags | boundary_risk_tags)
    low_energy_sensitive = scenario.name == "低能量日 / 保命态" or has_any(body_states, ("睡眠不足", "低能量"))
    if self_monitor_hit and low_energy_sensitive:
        status = ABORT if scenario.name == "低能量日 / 保命态" and has_any(self_monitor_hit, ("需要频繁整理", "容易走光", "需要持续端着")) else WARNING
        constraints.append(
            build_constraint(
                "情绪监控成本",
                status,
                f"{format_tags(self_monitor_hit)}，会要求你持续检查自己",
                "低能量状态下，衣服不能再向你索要注意力。频繁整理会增加精神噪音。",
                "替换为低维护面料、稳定领口/下摆、低饱和颜色和不需要端着的版型。",
            )
        )
    elif self_monitor_hit:
        constraints.append(
            build_constraint(
                "情绪监控成本",
                WARNING,
                f"{format_tags(self_monitor_hit)}，存在自我监控需求",
                "它不会立刻失败，但会增加一路上反复确认衣服状态的次数。",
                "优先换掉最需要整理或最怕脏的一件。",
            )
        )
    else:
        constraints.append(
            build_constraint(
                "情绪监控成本",
                PASS,
                "未标记走光、易皱、易脏、端着或高识别度压力",
                "这套不会向你索要太多精神维护。",
                "保持低维护和低自我监控。",
            )
        )

    sitting_friction = 18
    sitting_friction += 22 if sitting else 0
    sitting_friction += 14 if duration_weight == 3 else 6 if duration_weight == 2 else 0
    sitting_friction += 32 if pressure_hit else 0
    sitting_friction += 14 if has_any(body_states, ("胃胀", "经期")) else 0

    walking_friction = 16
    walking_friction += 26 if walking else 0
    walking_friction += 14 if scenario.name == "城市游荡 / 观察态" else 0
    walking_friction += 34 if shoe_hit else 0
    walking_friction += 18 if mobility_hit else 0
    walking_friction += 12 if "脚痛/膝盖疲劳" in body_states else 0

    temperature_friction = 18
    temperature_friction += 22 if climate_sensitive else 0
    temperature_friction += 30 if thermal_hit else 0
    temperature_friction += 10 if duration_weight == 3 else 0
    temperature_friction += 10 if has_any(body_states, ("怕冷", "怕热")) else 0

    maintenance_friction = 14
    maintenance_friction += len(tags & maintenance_risk_tags) * 14
    maintenance_friction += 18 if low_energy_sensitive else 0
    maintenance_friction += 10 if "雨天" in weather_states and has_any(tags, ("浅色易脏", "贵重怕刮/怕雨")) else 0

    emotion_friction = 16
    emotion_friction += len(self_monitor_hit) * 11
    emotion_friction += 18 if low_energy_sensitive else 0
    emotion_friction += 12 if scenario.name == "社交防御 / 武装态" and "过度暴露/边界感不足" in tags else 0

    risk_metrics = [
        {
            "name": "久坐摩擦",
            "percent": clamp(sitting_friction),
            "label": label_for_risk(clamp(sitting_friction)),
            "reason": "由久坐、外出时长、腰腹压力和当前身体状态共同决定。",
        },
        {
            "name": "步行摩擦",
            "percent": clamp(walking_friction),
            "label": label_for_risk(clamp(walking_friction)),
            "reason": "由步行强度、鞋底支撑、动作受限和脚部状态共同决定。",
        },
        {
            "name": "温度摩擦",
            "percent": clamp(temperature_friction),
            "label": label_for_risk(clamp(temperature_friction)),
            "reason": "由天气、空调/温差、材质和叠穿能力共同决定。",
        },
        {
            "name": "维护摩擦",
            "percent": clamp(maintenance_friction),
            "label": label_for_risk(clamp(maintenance_friction)),
            "reason": "由易皱、易脏、怕雨、频繁整理等维护任务决定。",
        },
        {
            "name": "情绪监控摩擦",
            "percent": clamp(emotion_friction),
            "label": label_for_risk(clamp(emotion_friction)),
            "reason": "由走光、端着、高识别度和低能量状态共同决定。",
        },
    ]

    crowd_stealth = 58
    crowd_stealth += 25 if "低饱和/人群隐蔽" in tags else 0
    crowd_stealth += 12 if "有外套/边界感" in tags else 0
    crowd_stealth -= 26 if "高识别度/吸睛" in tags else 0
    crowd_stealth -= 16 if "过度暴露/边界感不足" in tags else 0

    temperature_adaptability = 100 - clamp(temperature_friction)
    temperature_adaptability += 22 if has_any(tags, ("可叠穿/可脱卸", "透气材质")) else 0
    temperature_adaptability -= 8 if has_any(tags, ("单件厚衣", "无法叠穿")) else 0

    emotion_stability = 100 - clamp(emotion_friction)
    emotion_stability += 14 if "低维护" in tags else 0
    emotion_stability += 10 if "有外套/边界感" in tags else 0

    hard_abort_count = sum(1 for constraint in constraints if constraint["status"] == ABORT)
    task_continuity = 88
    task_continuity -= max(metric["percent"] for metric in risk_metrics) // 3
    task_continuity -= hard_abort_count * 20
    task_continuity += 8 if has_any(tags, ("运动鞋/足弓支撑", "松紧腰/软腰头", "低维护")) else 0

    protection_metrics = [
        {
            "name": "人群隐蔽性",
            "percent": clamp(crowd_stealth),
            "label": label_for_protection(clamp(crowd_stealth)),
            "reason": "低饱和、外套和边界感会提高保护；吸睛和暴露会降低保护。",
        },
        {
            "name": "温度适配性",
            "percent": clamp(temperature_adaptability),
            "label": label_for_protection(clamp(temperature_adaptability)),
            "reason": "可叠穿、可脱卸和透气材质会提升温度适配。",
        },
        {
            "name": "情绪稳定性",
            "percent": clamp(emotion_stability),
            "label": label_for_protection(clamp(emotion_stability)),
            "reason": "低维护、稳定覆盖和低自我监控会提升情绪稳定。",
        },
        {
            "name": "任务连续性",
            "percent": clamp(task_continuity),
            "label": label_for_protection(clamp(task_continuity)),
            "reason": "风险越少，当前任务越不容易被衣服打断。",
        },
    ]

    max_risk = max(metric["percent"] for metric in risk_metrics)
    warnings = [constraint for constraint in constraints if constraint["status"] == WARNING]
    aborts = [constraint for constraint in constraints if constraint["status"] == ABORT]
    performative = has_any(tags, ("高识别度/吸睛", "需要持续端着", "过度暴露/边界感不足"))

    if len(aborts) >= 2 or max_risk >= 92:
        code = "REJECTED"
        summary = "当前穿搭会打断核心任务，不建议购买或穿出门。"
        instruction = (
            f"{scenario.name} 的核心任务是：{scenario.core_task}。"
            "这套存在多个红灯项，美感不能抵消身体痛苦。建议拔草，或完全重组后再测。"
        )
    elif len(aborts) == 1:
        code = "MODIFY"
        summary = "主体可以保留，但红灯单品必须替换后才可执行。"
        instruction = (
            f"当前红灯是「{aborts[0]['name']}」。"
            f"处理方式：{aborts[0]['fix']}替换前不要硬穿。"
        )
    elif performative and scenario.name in ("考证冲刺 / 防御态", "低能量日 / 保命态") and emotion_friction >= 48:
        code = "DELAY"
        summary = "它更像服务于被观看的场景，不服务于今天的任务。"
        instruction = (
            f"今天需要的是低噪音、低维护、低自我监控。"
            f"建议存入「{scenario.wishlist_category}」，不要让幻想场景接管当前身体。"
        )
    elif max_risk >= 70 or len(warnings) >= 2:
        code = "MODIFY"
        summary = "可以救，但需要先降低摩擦最高的部位。"
        highest_metric = max(risk_metrics, key=lambda item: item["percent"])
        instruction = (
            f"最高摩擦项是「{highest_metric['name']}」{highest_metric['percent']}%。"
            "先替换对应单品，再执行当前任务。"
        )
    else:
        code = "APPROVED"
        summary = "可直接执行。此穿搭不会显著消耗当前任务能量。"
        instruction = "这套不会制造额外任务。允许美，但它没有压过身体舒适和任务连续性。"

    verdict = {
        "code": code,
        "summary": summary,
        "instruction": instruction,
        "wishlist_category": scenario.wishlist_category,
    }

    return {
        "scenario": inputs["scenario"],
        "mode_label": scenario.label,
        "core_task": scenario.core_task,
        "inferred_tags": sorted(inferred_tags),
        "physical_constraints": constraints,
        "risk_metrics": risk_metrics,
        "protection_metrics": protection_metrics,
        "verdict": verdict,
    }


def render_constraint_card(constraint: dict[str, str]) -> None:
    message = (
        f"{constraint['status_icon']} {constraint['status']}｜{constraint['name']}\n\n"
        f"{constraint['evidence']}\n\n"
        f"{constraint['impact']}\n\n"
        f"修正：{constraint['fix']}"
    )
    if constraint["status"] == ABORT:
        st.error(message)
    elif constraint["status"] == WARNING:
        st.warning(message)
    else:
        st.success(message)


def render_metric(metric: dict[str, Any], kind: str) -> None:
    icon = "消耗" if kind == "risk" else "保护"
    st.write(f"{icon}｜{metric['name']}：{metric['percent']}% · {metric['label']}")
    st.progress(metric["percent"] / 100)
    st.caption(metric["reason"])


def render_verdict(verdict: dict[str, str]) -> None:
    text = f"""[{verdict["code"]}]

{verdict["summary"]}

{verdict["instruction"]}

存档建议：{verdict["wishlist_category"]}
"""
    st.code(text, language="text")


st.set_page_config(
    page_title="生活流压力测试仪",
    page_icon="🧭",
    layout="wide",
)

st.title("生活流压力测试仪")
st.caption("Pre-flight Checklist for Real Life Outfits")

scenario_label_to_key = {scenario.label: key for key, scenario in SCENARIOS.items()}
selected_label = st.radio(
    "当前任务协议",
    list(scenario_label_to_key.keys()),
    horizontal=True,
)
selected_scenario_key = scenario_label_to_key[selected_label]
selected_scenario = SCENARIOS[selected_scenario_key]

st.info(
    f"核心任务：{selected_scenario.core_task} ｜ "
    f"硬约束：{'、'.join(selected_scenario.hard_constraints)}"
)

left_col, right_col = st.columns([1, 1.45], gap="large")

with left_col:
    st.subheader("目标图 + 现实条件补丁")

    uploaded_file = st.file_uploader(
        "上传目标穿搭图",
        type=["jpg", "jpeg", "png", "webp"],
    )
    if uploaded_file is not None:
        st.image(uploaded_file, caption="目标穿搭图", use_container_width=True)
    else:
        st.info("可上传网图或试穿图；当前版本的裁决主要依据下方补充信息。")

    st.markdown("#### 今日现实参数")
    duration = st.selectbox("预计外出时长", list(DURATION_WEIGHTS.keys()), index=2 if selected_scenario_key == "exam_sprint" else 1)
    sitting = st.toggle("是否长时间久坐", value=selected_scenario.default_sitting)
    walking = st.toggle("是否大量步行", value=selected_scenario.default_walking)
    standing = st.toggle("是否长时间站立/排队", value=selected_scenario.default_standing)
    backpack = st.toggle("是否背包/携带通勤物品", value=False)
    body_states = st.multiselect(
        "当前身体状态",
        BODY_STATES,
        default=["低能量"] if selected_scenario_key == "low_energy_day" else ["正常"],
    )
    weather_states = st.multiselect(
        "今日环境",
        WEATHER_STATES,
        default=["空调房"] if selected_scenario_key == "exam_sprint" else [],
    )

    st.markdown("#### 单品风险标签")
    waist_tags = st.multiselect("腰腹与下装", WAIST_TAGS)
    shoe_tags = st.multiselect("鞋履", SHOE_TAGS)
    thermal_tags = st.multiselect("温度与层次", THERMAL_TAGS)
    mobility_tags = st.multiselect("行动与携带", MOBILITY_TAGS)
    maintenance_tags = st.multiselect("维护与整理", MAINTENANCE_TAGS)
    social_tags = st.multiselect("可见度与边界", SOCIAL_TAGS)
    notes = st.text_area(
        "穿搭补充描述",
        placeholder="例：高腰牛仔裤 + 薄底小皮鞋 + 单件厚卫衣，今天要在图书馆坐 8 小时。",
        height=90,
    )

    analyze_clicked = st.button("执行压力测试", type="primary", use_container_width=True)

all_tags = waist_tags + shoe_tags + thermal_tags + mobility_tags + maintenance_tags + social_tags
analysis_inputs = {
    "scenario": selected_scenario_key,
    "duration": duration,
    "sitting": sitting,
    "walking": walking,
    "standing": standing,
    "backpack": backpack,
    "body_states": body_states,
    "weather_states": weather_states,
    "tags": all_tags,
    "notes": notes,
}

if analyze_clicked:
    st.session_state["latest_analysis"] = analyze_outfit(analysis_inputs)

with right_col:
    if "latest_analysis" not in st.session_state:
        st.subheader("等待执行")
        st.info("选择任务协议，补齐现实参数和单品风险后，执行压力测试。")
        st.code(
            """[PENDING]

等待当前生活流参数。

裁决只服务于今天的身体、任务和环境。
""",
            language="text",
        )
    else:
        result = st.session_state["latest_analysis"]

        st.subheader("A. 生理约束锁定")
        for item in result["physical_constraints"]:
            render_constraint_card(item)

        st.subheader("B. 环境摩擦力扫描")
        risk_col, protection_col = st.columns(2, gap="large")
        with risk_col:
            st.markdown("##### 消耗型指标")
            for metric in result["risk_metrics"]:
                render_metric(metric, "risk")
        with protection_col:
            st.markdown("##### 保护型指标")
            for metric in result["protection_metrics"]:
                render_metric(metric, "protection")

        st.subheader("C. 最终裁决协议")
        render_verdict(result["verdict"])

        with st.expander("JSON 输出"):
            st.json(result)
