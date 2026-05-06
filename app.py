from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import streamlit as st


@dataclass(frozen=True)
class Scenario:
    title: str
    stance: str
    core_task: str
    must_not_break: tuple[str, ...]
    default_needs: tuple[str, ...]
    delay_bucket: str


@dataclass(frozen=True)
class Blocker:
    code: str
    title: str
    severity: int
    evidence: str
    reason: str
    replacements: tuple[str, ...]
    keep_condition: str


SCENARIOS: dict[str, Scenario] = {
    "exam_sprint": Scenario(
        title="考证冲刺",
        stance="防御态",
        core_task="长时间坐下学习，身体必须安静，注意力不能被衣服拉走。",
        must_not_break=("腰腹呼吸", "久坐稳定", "温度可调", "低整理成本"),
        default_needs=("久坐", "空调房", "8小时以上"),
        delay_bucket="考证后低任务密度社交",
    ),
    "city_walk": Scenario(
        title="城市游荡",
        stance="观察态",
        core_task="长距离移动、换乘、观察城市，脚和动作自由优先。",
        must_not_break=("脚底支撑", "迈步幅度", "包容量", "天气适配"),
        default_needs=("大量步行", "背包/携带物", "4小时左右"),
        delay_bucket="短时拍照或低步行场景",
    ),
    "social_defense": Scenario(
        title="社交防御",
        stance="武装态",
        core_task="保持边界、体面和心理安全，不被衣服迫使持续自我监控。",
        must_not_break=("边界感", "行动自如", "坐立切换", "情绪稳定"),
        default_needs=("长时间站立/排队", "陌生人环境", "4小时左右"),
        delay_bucket="高能量社交日",
    ),
    "low_energy_day": Scenario(
        title="低能量日",
        stance="保命态",
        core_task="减少身体噪音和决策疲劳，衣服不能再制造额外任务。",
        must_not_break=("无压迫", "不用整理", "温度不失控", "低存在感"),
        default_needs=("低能量", "短途出门", "2小时以内"),
        delay_bucket="状态恢复后再评估",
    ),
}


ITEM_TYPES = ("整套穿搭", "上衣", "下装", "鞋", "外套", "包", "配饰")

FACT_OPTIONS: dict[str, tuple[str, ...]] = {
    "整套穿搭": (
        "腰腹有压迫",
        "鞋底薄/硬",
        "需要频繁整理",
        "温度不能快速调节",
        "走路受限",
        "高识别度/吸睛",
        "低维护",
        "行动自由",
    ),
    "上衣": (
        "紧身/抬手受限",
        "短上衣/露肤多",
        "闷汗材质",
        "容易皱",
        "需要频繁整理",
        "透气",
        "低维护",
    ),
    "下装": (
        "高腰压腹",
        "硬腰头",
        "无弹力牛仔",
        "紧身裤",
        "窄裙/迈不开步",
        "松紧腰/软腰头",
        "宽松直筒",
        "垂感半裙",
    ),
    "鞋": (
        "薄底",
        "硬底小皮鞋",
        "无缓冲平底鞋",
        "新鞋未磨合",
        "高跟",
        "运动鞋/足弓支撑",
        "已磨合",
    ),
    "外套": (
        "单件厚衣",
        "不好穿脱",
        "闷汗材质",
        "怕雨/怕刮",
        "可脱卸",
        "可叠穿",
        "有边界感",
    ),
    "包": (
        "容量不足",
        "肩带易滑",
        "和衣服打架",
        "无口袋辅助",
        "能装通勤物",
        "肩带稳定",
        "可解放双手",
    ),
    "配饰": (
        "贵重怕刮",
        "怕雨",
        "容易勾衣服",
        "声音明显",
        "低维护",
        "不影响动作",
    ),
}

GENERAL_FACTS = (
    "容易走光",
    "浅色易脏",
    "需要持续端着",
    "低饱和/人群隐蔽",
    "有外套/边界感",
)

BODY_OPTIONS = ("正常", "胃胀", "经期", "睡眠不足", "低能量", "怕冷", "怕热", "脚痛/膝盖疲劳")
ENV_OPTIONS = ("冷", "热", "温差大", "空调房", "雨天", "强日晒", "拥挤通勤", "陌生人环境")
NEED_OPTIONS = ("久坐", "大量步行", "长时间站立/排队", "背包/携带物", "短途出门", "试穿/拍照")
DURATION_OPTIONS = ("2小时以内", "4小时左右", "8小时以上")

KEYWORD_FACTS: dict[str, tuple[str, ...]] = {
    "高腰压腹": ("高腰", "压腹", "勒肚子", "勒腹", "腰紧"),
    "硬腰头": ("硬腰", "硬腰头", "硬质腰"),
    "无弹力牛仔": ("无弹力", "牛仔", "牛仔裤"),
    "紧身裤": ("紧身裤", "贴腿"),
    "窄裙/迈不开步": ("窄裙", "包臀裙", "迈不开"),
    "薄底": ("薄底", "薄底鞋"),
    "硬底小皮鞋": ("硬底", "小皮鞋", "皮鞋"),
    "无缓冲平底鞋": ("平底鞋", "无缓冲"),
    "新鞋未磨合": ("新鞋", "第一次穿", "没磨合"),
    "高跟": ("高跟", "高跟鞋"),
    "单件厚衣": ("厚卫衣", "厚毛衣", "厚外套", "单件厚"),
    "不好穿脱": ("不好脱", "不好穿脱", "不能脱"),
    "闷汗材质": ("闷汗", "不透气", "皮革", "涤纶"),
    "短上衣/露肤多": ("短上衣", "露肤", "低领", "吊带"),
    "容量不足": ("小包", "包太小", "装不下"),
    "肩带易滑": ("肩带滑", "总滑"),
    "需要频繁整理": ("频繁整理", "总要整理", "需要整理"),
    "容易走光": ("走光", "怕露", "担心露"),
    "容易皱": ("容易皱", "皱"),
    "浅色易脏": ("浅色", "易脏", "白裤", "白裙"),
    "贵重怕刮": ("贵", "怕刮", "真皮"),
    "怕雨": ("怕雨", "下雨不能"),
    "需要持续端着": ("端着", "不自在", "需要气场"),
    "高识别度/吸睛": ("吸睛", "亮色", "夸张", "高识别"),
    "低维护": ("低维护", "不用管", "耐脏"),
    "运动鞋/足弓支撑": ("运动鞋", "足弓", "支撑"),
    "松紧腰/软腰头": ("松紧腰", "软腰头"),
    "宽松直筒": ("宽松", "直筒"),
    "可脱卸": ("可脱", "能脱", "开衫"),
    "可叠穿": ("叠穿", "外搭"),
    "有外套/边界感": ("外套", "边界感", "遮挡"),
}

STEP_ORDER = ("protocol", "item", "life", "result")
STEP_LABELS = {
    "protocol": "01 任务",
    "item": "02 单品",
    "life": "03 今日",
    "result": "04 建议",
}


def init_state() -> None:
    defaults = {
        "step": "protocol",
        "scenario_key": "",
        "item_type": "下装",
        "item_name": "",
        "item_notes": "",
        "facts": [],
        "duration": "4小时左右",
        "needs": [],
        "body_states": ["正常"],
        "env_states": [],
        "uploaded_name": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def go(step: str) -> None:
    st.session_state.step = step
    st.rerun()


def reset_flow() -> None:
    for key in (
        "step",
        "scenario_key",
        "item_type",
        "item_name",
        "item_notes",
        "facts",
        "duration",
        "needs",
        "body_states",
        "env_states",
        "uploaded_name",
    ):
        st.session_state.pop(key, None)
    init_state()
    st.rerun()


def next_step(current: str) -> str:
    index = STEP_ORDER.index(current)
    return STEP_ORDER[min(index + 1, len(STEP_ORDER) - 1)]


def previous_step(current: str) -> str:
    index = STEP_ORDER.index(current)
    return STEP_ORDER[max(index - 1, 0)]


def infer_facts(notes: str) -> set[str]:
    normalized = notes.lower()
    return {
        fact
        for fact, keywords in KEYWORD_FACTS.items()
        if any(keyword.lower() in normalized for keyword in keywords)
    }


def clean_body_states(states: list[str]) -> set[str]:
    cleaned = set(states)
    if len(cleaned) > 1:
        cleaned.discard("正常")
    return cleaned


def has_any(values: set[str], options: tuple[str, ...]) -> bool:
    return any(option in values for option in options)


def apply_default_needs(scenario_key: str) -> None:
    scenario = SCENARIOS[scenario_key]
    defaults = set(scenario.default_needs)
    st.session_state.needs = sorted(defaults & set(NEED_OPTIONS))
    st.session_state.env_states = sorted(defaults & set(ENV_OPTIONS))
    st.session_state.body_states = sorted(defaults & set(BODY_OPTIONS)) or ["正常"]
    duration_defaults = defaults & set(DURATION_OPTIONS)
    if duration_defaults:
        st.session_state.duration = sorted(duration_defaults)[-1]


def replacement_text(replacements: tuple[str, ...]) -> str:
    return " / ".join(replacements)


def render_progress() -> None:
    cols = st.columns(len(STEP_ORDER))
    active_step = st.session_state.step
    active_index = STEP_ORDER.index(active_step)
    for index, step in enumerate(STEP_ORDER):
        marker = "●" if index == active_index else "○"
        cols[index].caption(f"{marker} {STEP_LABELS[step]}")


def render_nav(back_to: str | None = None, next_to: str | None = None, next_label: str = "继续") -> None:
    left, middle, right = st.columns([1, 1, 1])
    if back_to and left.button("返回", use_container_width=True):
        go(back_to)
    if middle.button("重新开始", use_container_width=True):
        reset_flow()
    if next_to and right.button(next_label, type="primary", use_container_width=True):
        go(next_to)


def assess_item(data: dict[str, Any]) -> dict[str, Any]:
    scenario = SCENARIOS[data["scenario_key"]]
    item_type = data["item_type"]
    item_name = data["item_name"].strip() or item_type
    body_states = clean_body_states(data["body_states"])
    env_states = set(data["env_states"])
    needs = set(data["needs"])
    inferred = infer_facts(data["item_notes"])
    facts = set(data["facts"]) | inferred
    duration = data["duration"]

    long_day = duration == "8小时以上"
    sitting = "久坐" in needs
    walking = "大量步行" in needs
    standing = "长时间站立/排队" in needs
    carrying = "背包/携带物" in needs
    low_energy = has_any(body_states, ("睡眠不足", "低能量")) or data["scenario_key"] == "low_energy_day"
    climate_shift = bool(env_states & {"冷", "热", "温差大", "空调房", "雨天", "强日晒"})

    blockers: list[Blocker] = []

    waist_facts = {"腰腹有压迫", "高腰压腹", "硬腰头", "无弹力牛仔", "紧身裤"}
    if facts & waist_facts and (sitting or long_day or has_any(body_states, ("胃胀", "经期"))):
        severity = 95 if data["scenario_key"] in {"exam_sprint", "low_energy_day"} or has_any(body_states, ("胃胀", "经期")) else 78
        blockers.append(
            Blocker(
                code="waist_pressure",
                title="腰腹压迫会破坏今天的主任务",
                severity=severity,
                evidence=f"{item_name} 标记了：{', '.join(sorted(facts & waist_facts))}",
                reason="今天需要久坐或身体稳定，腰腹压迫会持续占用注意力，影响呼吸、胃肠舒适和坐姿耐受。",
                replacements=("软腰头直筒裤", "松紧腰半裙", "垂感运动裤"),
                keep_condition="只有在短时站立、无需久坐、胃腹状态稳定时才可保留。",
            )
        )

    shoe_facts = {"鞋底薄/硬", "薄底", "硬底小皮鞋", "无缓冲平底鞋", "新鞋未磨合", "高跟"}
    if facts & shoe_facts and (walking or standing or data["scenario_key"] == "city_walk" or "脚痛/膝盖疲劳" in body_states):
        blockers.append(
            Blocker(
                code="shoe_support",
                title="鞋会把出门任务改写成找座位",
                severity=96 if walking or data["scenario_key"] == "city_walk" else 76,
                evidence=f"{item_name} 标记了：{', '.join(sorted(facts & shoe_facts))}",
                reason="今天存在步行、排队或换乘需求，鞋底不支撑会优先击穿脚底、膝盖和耐心。",
                replacements=("已磨合运动鞋", "厚底乐福鞋", "有足弓支撑的短靴"),
                keep_condition="只有在打车直达、步行少于20分钟、且不排队时才可保留。",
            )
        )

    thermal_facts = {"温度不能快速调节", "单件厚衣", "不好穿脱", "闷汗材质", "短上衣/露肤多"}
    if facts & thermal_facts and (climate_shift or has_any(body_states, ("怕冷", "怕热")) or long_day):
        blockers.append(
            Blocker(
                code="temperature_control",
                title="温度不可调会持续制造烦躁",
                severity=88 if long_day and data["scenario_key"] in {"exam_sprint", "low_energy_day"} else 68,
                evidence=f"{item_name} 标记了：{', '.join(sorted(facts & thermal_facts))}",
                reason="今天的环境有温差、空调、日晒或长时间停留，不能快速穿脱会让冷、热、闷成为持续干扰。",
                replacements=("薄打底 + 开衫", "衬衫外套", "可脱卸马甲"),
                keep_condition="只有在温度稳定、室内外切换少时才可保留。",
            )
        )

    mobility_facts = {
        "走路受限",
        "窄裙/迈不开步",
        "紧身/抬手受限",
        "容量不足",
        "肩带易滑",
        "和衣服打架",
        "无口袋辅助",
    }
    if facts & mobility_facts and (walking or standing or carrying or data["scenario_key"] == "city_walk"):
        blockers.append(
            Blocker(
                code="mobility",
                title="行动摩擦会打断生活流",
                severity=90 if data["scenario_key"] == "city_walk" else 70,
                evidence=f"{item_name} 标记了：{', '.join(sorted(facts & mobility_facts))}",
                reason="今天需要走、拿、坐下起身或携带物品，动作受限会把小事变成连续卡顿。",
                replacements=("可跨步下装", "稳定肩带通勤包", "能解放双手的包"),
                keep_condition="只有在路线短、物品少、无需赶时间时才可保留。",
            )
        )

    maintenance_facts = {
        "需要频繁整理",
        "容易走光",
        "容易皱",
        "浅色易脏",
        "贵重怕刮",
        "怕雨",
        "容易勾衣服",
        "声音明显",
        "需要持续端着",
        "高识别度/吸睛",
    }
    if facts & maintenance_facts and (low_energy or data["scenario_key"] in {"exam_sprint", "social_defense"}):
        blockers.append(
            Blocker(
                code="self_monitoring",
                title="它会要求你持续管理自己",
                severity=92 if low_energy and has_any(facts, ("需要频繁整理", "容易走光", "需要持续端着")) else 66,
                evidence=f"{item_name} 标记了：{', '.join(sorted(facts & maintenance_facts))}",
                reason="今天的重点不是展示衣服，而是保持任务连续和情绪稳定。自我监控会消耗精神电量。",
                replacements=("稳定领口和下摆", "低饱和耐脏色", "抗皱低维护面料"),
                keep_condition="只有在高能量、低任务、可随时整理的场合才可保留。",
            )
        )

    positive_facts = {
        "松紧腰/软腰头",
        "宽松直筒",
        "垂感半裙",
        "运动鞋/足弓支撑",
        "已磨合",
        "可脱卸",
        "可叠穿",
        "透气",
        "能装通勤物",
        "肩带稳定",
        "可解放双手",
        "低维护",
        "不影响动作",
        "行动自由",
        "低饱和/人群隐蔽",
        "有外套/边界感",
    }

    blockers = sorted(blockers, key=lambda blocker: blocker.severity, reverse=True)
    top = blockers[0] if blockers else None
    severe_count = sum(1 for blocker in blockers if blocker.severity >= 88)
    performative = bool(facts & {"高识别度/吸睛", "需要持续端着"})

    if severe_count >= 2:
        verdict = "ABORT"
        action = f"{item_name} 今天不要穿出门，也不建议购买。"
        one_line = "它会连续破坏身体、行动或情绪，不是单点小问题。"
    elif top and top.severity >= 88:
        verdict = "ABORT"
        action = f"{item_name} 今天直接换掉。"
        one_line = top.title
    elif performative and data["scenario_key"] in {"exam_sprint", "low_energy_day"}:
        verdict = "DELAY"
        action = f"{item_name} 不服务于今天，存入未来场景。"
        one_line = "它更适合被观看，不适合低噪音执行任务。"
    elif blockers:
        verdict = "SWAP"
        action = f"{item_name} 可以保留风格，但必须替换高摩擦结构。"
        one_line = top.title if top else "存在可修正摩擦。"
    else:
        verdict = "APPROVED"
        action = f"{item_name} 今天可以穿。"
        one_line = "它不会明显打断当前任务。"

    replacements: list[str] = []
    for blocker in blockers[:2]:
        replacements.extend(blocker.replacements)
    if not replacements:
        replacements = ["保持当前低压结构", "不要临时加入新鞋或硬腰头", "保留可穿脱层次"]

    return {
        "scenario": scenario,
        "item_type": item_type,
        "item_name": item_name,
        "facts": sorted(facts),
        "inferred": sorted(inferred),
        "positive_facts": sorted(facts & positive_facts),
        "blockers": blockers,
        "verdict": verdict,
        "action": action,
        "one_line": one_line,
        "primary_replacements": tuple(dict.fromkeys(replacements))[:4],
        "keep_condition": top.keep_condition if top else "可以执行，但不要临时增加久坐、长走或高温差任务。",
        "delay_bucket": scenario.delay_bucket,
    }


def render_shell(title: str, subtitle: str) -> None:
    render_progress()
    st.markdown('<section class="slice">', unsafe_allow_html=True)
    st.caption(subtitle)
    st.title(title)


def close_shell() -> None:
    st.markdown("</section>", unsafe_allow_html=True)


def render_protocol_slice() -> None:
    render_shell("先选今天，不选幻想场景", "生活流压力测试仪")
    st.write("裁决只服务于当前身体和当前任务。美可以存在，但不能抵消身体痛苦。")

    cols = st.columns(2, gap="large")
    for index, (key, scenario) in enumerate(SCENARIOS.items()):
        with cols[index % 2]:
            st.markdown(
                f"""
                <div class="choice-card">
                    <div class="choice-title">{scenario.title}</div>
                    <div class="choice-stance">{scenario.stance}</div>
                    <div class="choice-copy">{scenario.core_task}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"进入：{scenario.title}", key=f"scenario_{key}", use_container_width=True):
                st.session_state.scenario_key = key
                apply_default_needs(key)
                go("item")

    close_shell()


def render_item_slice() -> None:
    scenario = SCENARIOS[st.session_state.scenario_key]
    render_shell("现在只判断一件具体衣服", f"{scenario.title} / {scenario.stance}")

    st.write("不要先问整套好不好看。先抓住最可能破坏生活流的那件单品。")

    uploaded_file = st.file_uploader("上传这件衣服或这套穿搭的图片", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file is not None:
        st.session_state.uploaded_name = uploaded_file.name
        st.image(uploaded_file, caption=uploaded_file.name, width=260)

    left, right = st.columns([0.85, 1.15], gap="large")
    with left:
        st.session_state.item_type = st.selectbox(
            "单品类型",
            ITEM_TYPES,
            index=ITEM_TYPES.index(st.session_state.item_type),
        )
        st.session_state.item_name = st.text_input(
            "给它一个具体名字",
            value=st.session_state.item_name,
            placeholder="例：高腰硬牛仔裤 / 薄底小皮鞋 / 单件厚卫衣",
        )
        st.session_state.item_notes = st.text_area(
            "事实描述",
            value=st.session_state.item_notes,
            placeholder="写事实，不写愿望。例：腰很紧、坐下压肚子、鞋底薄、今天要走很多路。",
            height=120,
        )

    with right:
        options = tuple(dict.fromkeys(FACT_OPTIONS[st.session_state.item_type] + GENERAL_FACTS))
        current = [fact for fact in st.session_state.facts if fact in options]
        st.session_state.facts = st.multiselect(
            "这件衣服的事实标签",
            options,
            default=current,
            help="这里不是审美标签，只记录会影响身体和任务的事实。",
        )

        inferred = infer_facts(st.session_state.item_notes)
        if inferred:
            st.caption("从描述中自动识别：" + " / ".join(sorted(inferred)))

    disable_next = not (st.session_state.item_name.strip() or st.session_state.item_notes.strip() or st.session_state.facts)
    left_nav, mid_nav, right_nav = st.columns([1, 1, 1])
    if left_nav.button("返回任务", use_container_width=True):
        go("protocol")
    if mid_nav.button("重新开始", use_container_width=True):
        reset_flow()
    if right_nav.button("继续到今日生活流", type="primary", disabled=disable_next, use_container_width=True):
        go("life")

    close_shell()


def render_life_slice() -> None:
    scenario = SCENARIOS[st.session_state.scenario_key]
    render_shell("今天它要服务什么任务", f"{scenario.title} / {scenario.stance}")

    st.markdown("#### 不能被衣服破坏的东西")
    st.write(" / ".join(scenario.must_not_break))

    duration_cols = st.columns(3)
    for index, option in enumerate(DURATION_OPTIONS):
        button_type = "primary" if st.session_state.duration == option else "secondary"
        if duration_cols[index].button(option, type=button_type, use_container_width=True):
            st.session_state.duration = option
            st.rerun()

    left, right = st.columns(2, gap="large")
    with left:
        st.session_state.needs = st.multiselect(
            "今天的任务动作",
            NEED_OPTIONS,
            default=st.session_state.needs,
        )
        st.session_state.body_states = st.multiselect(
            "当前身体状态",
            BODY_OPTIONS,
            default=st.session_state.body_states,
        )
    with right:
        st.session_state.env_states = st.multiselect(
            "今日环境",
            ENV_OPTIONS,
            default=st.session_state.env_states,
        )
        st.info("这一步决定裁决强度。同一件衣服，在考试日和拍照日会得到不同处理。")

    render_nav(back_to="item", next_to="result", next_label="生成单品建议")
    close_shell()


def render_result_slice() -> None:
    data = {
        "scenario_key": st.session_state.scenario_key,
        "item_type": st.session_state.item_type,
        "item_name": st.session_state.item_name,
        "item_notes": st.session_state.item_notes,
        "facts": st.session_state.facts,
        "duration": st.session_state.duration,
        "needs": st.session_state.needs,
        "body_states": st.session_state.body_states,
        "env_states": st.session_state.env_states,
    }
    result = assess_item(data)
    scenario = result["scenario"]

    render_shell("具体衣服建议", f"{scenario.title} / {scenario.stance}")

    verdict_class = result["verdict"].lower()
    st.markdown(
        f"""
        <div class="verdict {verdict_class}">
            <div class="verdict-code">[{result["verdict"]}]</div>
            <div class="verdict-action">{result["action"]}</div>
            <div class="verdict-line">{result["one_line"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 0.95], gap="large")
    with left:
        st.markdown("#### 立刻怎么改")
        for index, replacement in enumerate(result["primary_replacements"], start=1):
            st.write(f"{index}. {replacement}")

        st.markdown("#### 保留条件")
        st.write(result["keep_condition"])

        if result["verdict"] == "DELAY":
            st.markdown("#### 存入")
            st.write(result["delay_bucket"])

    with right:
        st.markdown("#### 阻断原因")
        blockers = result["blockers"][:3]
        if blockers:
            for blocker in blockers:
                st.markdown(f"**{blocker.title}**")
                st.write(blocker.reason)
                st.caption(blocker.evidence)
        else:
            st.success("没有发现会破坏当前主任务的硬伤。")

        if result["positive_facts"]:
            st.markdown("#### 可以保留的部分")
            st.write(" / ".join(result["positive_facts"]))

    with st.expander("本次识别到的事实"):
        st.write("手动 + 自动识别：" + (" / ".join(result["facts"]) if result["facts"] else "无"))
        if result["inferred"]:
            st.write("自动识别：" + " / ".join(result["inferred"]))

    nav_left, nav_mid, nav_right = st.columns([1, 1, 1])
    if nav_left.button("调整今日条件", use_container_width=True):
        go("life")
    if nav_mid.button("换一件衣服测", use_container_width=True):
        st.session_state.item_name = ""
        st.session_state.item_notes = ""
        st.session_state.facts = []
        go("item")
    if nav_right.button("重新开始", type="primary", use_container_width=True):
        reset_flow()

    close_shell()


st.set_page_config(page_title="生活流压力测试仪", layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1040px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .slice {
        min-height: 72vh;
        padding: 1.2rem 0 0.6rem;
    }
    .choice-card {
        border: 1px solid #d7d7d7;
        border-radius: 8px;
        padding: 1rem;
        min-height: 142px;
        margin-bottom: 0.65rem;
        background: #fbfbfa;
    }
    .choice-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .choice-stance {
        color: #555;
        font-size: 0.88rem;
        margin-bottom: 0.8rem;
    }
    .choice-copy {
        color: #242424;
        line-height: 1.5;
    }
    .verdict {
        border-radius: 8px;
        padding: 1rem 1.1rem;
        margin: 0.6rem 0 1.2rem;
        border: 1px solid #222;
        background: #101010;
        color: #f5f5f5;
    }
    .verdict-code {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.9rem;
        opacity: 0.82;
        margin-bottom: 0.35rem;
    }
    .verdict-action {
        font-size: 1.35rem;
        font-weight: 800;
        line-height: 1.35;
        margin-bottom: 0.35rem;
    }
    .verdict-line {
        color: #e2e2e2;
        line-height: 1.55;
    }
    .verdict.approved {
        background: #123326;
        border-color: #1e5b42;
    }
    .verdict.swap {
        background: #332710;
        border-color: #6f551c;
    }
    .verdict.delay {
        background: #1d2536;
        border-color: #3a4d70;
    }
    .verdict.abort {
        background: #381516;
        border-color: #7a2729;
    }
    div[data-testid="stMarkdownContainer"] p {
        line-height: 1.65;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_state()

if st.session_state.step == "protocol" or not st.session_state.scenario_key:
    render_protocol_slice()
elif st.session_state.step == "item":
    render_item_slice()
elif st.session_state.step == "life":
    render_life_slice()
else:
    render_result_slice()
