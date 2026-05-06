import streamlit as st


TEXT = {
    "page_title": "\u9ad8\u8170\u6bd4\u4f8b\u4f18\u5316\u5668",
    "caption": (
        "\u4e0a\u4f20\u4e00\u5f20\u5168\u8eab\u6216\u534a\u8eab\u7a7f\u642d\u56fe\uff0c"
        "\u8f93\u5165\u57fa\u7840\u6bd4\u4f8b\u4fe1\u606f\uff0c"
        "\u5feb\u901f\u751f\u6210\u8170\u7ebf\u4f18\u5316\u5efa\u8bae\u3002"
    ),
    "input_title": "\u8f93\u5165\u4fe1\u606f",
    "upload_label": "\u4e0a\u4f20\u56fe\u7247",
    "upload_help": (
        "\u5efa\u8bae\u4e0a\u4f20\u6b63\u9762\u3001\u7ad9\u59ff\u3001"
        "\u5149\u7ebf\u6e05\u6670\u7684\u7a7f\u642d\u7167\u7247\u3002"
    ),
    "uploaded_caption": "\u5df2\u4e0a\u4f20\u56fe\u7247",
    "upload_first": "\u8bf7\u5148\u4e0a\u4f20\u4e00\u5f20\u56fe\u7247\u3002",
    "height_label": "\u8eab\u9ad8\uff08cm\uff09",
    "ratio_label": "\u76ee\u524d\u7684\u4e0a\u4e0b\u8eab\u6bd4\u4f8b\u4f30\u8ba1",
    "ratio_help": (
        "\u53ef\u4ee5\u7406\u89e3\u4e3a\u4e0b\u534a\u8eab\u89c6\u89c9\u957f\u5ea6"
        "\u5360\u6574\u4f53\u8eab\u9ad8\u7684\u6bd4\u4f8b\uff0c"
        "\u6570\u503c\u8d8a\u9ad8\u901a\u5e38\u8d8a\u663e\u817f\u957f\u3002"
    ),
    "analyze": "\u5f00\u59cb\u5206\u6790",
    "result_title": "\u5206\u6790\u7ed3\u679c",
    "click_hint": (
        "\u586b\u5199\u5de6\u4fa7\u4fe1\u606f\u5e76\u70b9\u51fb"
        "\u201c\u5f00\u59cb\u5206\u6790\u201d\u540e\uff0c"
        "\u8fd9\u91cc\u4f1a\u5c55\u793a\u5efa\u8bae\u3002"
    ),
    "upload_warning": (
        "\u8bf7\u5148\u4e0a\u4f20\u56fe\u7247\uff0c\u518d\u70b9\u51fb\u5206\u6790\u3002"
    ),
    "height_metric": "\u8eab\u9ad8",
    "ratio_metric": "\u6bd4\u4f8b\u4f30\u8ba1",
    "target_ratio_metric": "\u76ee\u6807\u9ec4\u91d1\u6bd4\u4f8b",
    "adjustment_metric": "\u5efa\u8bae\u8c03\u6574",
    "core_advice": "#### \u6838\u5fc3\u5efa\u8bae",
    "adjustment_title": "#### \u8170\u7ebf\u8c03\u6574",
    "style_title": "#### \u7a7f\u642d\u5efa\u8bae",
    "reference": "#### \u53c2\u8003\u8bf4\u660e",
    "prototype_note": (
        "\u5f53\u524d\u7248\u672c\u4e3a\u57fa\u7840 UI \u793a\u4f8b\uff0c"
        "\u6682\u672a\u63a5\u5165\u771f\u5b9e\u4eba\u4f53\u5173\u952e\u70b9"
        "\u8bc6\u522b\u6216\u56fe\u50cf\u6d4b\u91cf\u6a21\u578b\u3002"
    ),
}

TARGET_RATIO = 0.618

def build_suggestion(height_cm: int, upper_lower_ratio: float) -> dict[str, str]:
    ratio_gap = abs(upper_lower_ratio - TARGET_RATIO)
    adjustment_cm = ratio_gap * height_cm

    if adjustment_cm < 0.1:
        adjustment_text = "\u5df2\u63a5\u8fd1\u9ec4\u91d1\u6bd4\u4f8b\uff0c\u57fa\u672c\u65e0\u9700\u8c03\u6574"
    elif upper_lower_ratio < TARGET_RATIO:
        adjustment_text = f"\u5efa\u8bae\u5c06\u8170\u7ebf\u4e0a\u63d0\u7ea6 {adjustment_cm:.1f}cm"
    else:
        adjustment_text = f"\u5efa\u8bae\u5c06\u8170\u7ebf\u4e0b\u653e\u7ea6 {adjustment_cm:.1f}cm"

    if upper_lower_ratio < 0.6:
        advice_text = (
            "\u5efa\u8bae\u91c7\u7528\u7edd\u5bf9\u9ad8\u8170\u5355\u54c1"
            "\uff08\u524d\u88c6>30cm\uff09\uff0c\u914d\u5408\u987a\u8272\u978b\u5b50\uff0c"
            "\u5f3a\u5236\u62c9\u5347\u89c6\u89c9\u8170\u7ebf\u3002"
        )
    elif upper_lower_ratio <= 0.65:
        advice_text = (
            "\u6bd4\u4f8b\u4f18\u8d8a\uff0c\u5e38\u89c4\u9ad8\u8170\u6216\u4e2d\u8170"
            "\u5355\u54c1\u5373\u53ef\uff0c\u91cd\u70b9\u4fdd\u6301\u8272\u5f69\u8fde\u8d2f\u3002"
        )
    else:
        advice_text = (
            "\u5f53\u524d\u4e0b\u534a\u8eab\u89c6\u89c9\u6bd4\u4f8b\u5df2\u9ad8\u4e8e"
            "\u5e38\u89c4\u9ec4\u91d1\u6bd4\u4f8b\uff0c\u53ef\u9009\u62e9\u4e2d\u8170"
            "\u6216\u7565\u5bbd\u677e\u4e0a\u88c5\uff0c\u8ba9\u6574\u4f53\u91cd\u5fc3\u66f4\u5e73\u8861\u3002"
        )

    return {
        "adjustment_cm": f"{adjustment_cm:.1f}cm",
        "adjustment": adjustment_text,
        "advice": advice_text,
        "detail": (
            f"\u5f53\u524d\u6bd4\u4f8b\u4e0e\u76ee\u6807 {TARGET_RATIO:.3f} "
            f"\u7684\u5dee\u8ddd\u4e3a {ratio_gap:.3f}\uff0c"
            f"\u6309 {height_cm}cm \u8eab\u9ad8\u6362\u7b97\u7ea6\u4e3a "
            f"{adjustment_cm:.1f}cm\u3002"
        ),
        "ratio_comment": (
            "\u5df2\u6839\u636e\u5de6\u4fa7\u8eab\u9ad8\u548c\u5f53\u524d\u6bd4\u4f8b"
            "\u751f\u6210\u8170\u7ebf\u4f18\u5316\u5efa\u8bae\u3002"
        ),
    }


st.set_page_config(
    page_title=TEXT["page_title"],
    page_icon=":dress:",
    layout="wide",
)

st.title(TEXT["page_title"])
st.caption(TEXT["caption"])

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    st.subheader(TEXT["input_title"])

    uploaded_file = st.file_uploader(
        TEXT["upload_label"],
        type=["jpg", "jpeg", "png", "webp"],
        help=TEXT["upload_help"],
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption=TEXT["uploaded_caption"], use_container_width=True)
    else:
        st.info(TEXT["upload_first"])

    height_cm = st.slider(
        TEXT["height_label"],
        min_value=140,
        max_value=200,
        value=165,
        step=1,
    )

    upper_lower_ratio = st.slider(
        TEXT["ratio_label"],
        min_value=0.45,
        max_value=0.70,
        value=0.56,
        step=0.01,
        help=TEXT["ratio_help"],
    )

    analyze_clicked = st.button(
        TEXT["analyze"],
        type="primary",
        use_container_width=True,
    )

with right_col:
    st.subheader(TEXT["result_title"])

    if analyze_clicked:
        suggestion = build_suggestion(height_cm, upper_lower_ratio)

        st.success(suggestion["ratio_comment"])

        metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
        metric_col_1.metric(TEXT["height_metric"], f"{height_cm}cm")
        metric_col_2.metric(TEXT["ratio_metric"], f"{upper_lower_ratio:.2f}")
        metric_col_3.metric(TEXT["target_ratio_metric"], f"{TARGET_RATIO:.3f}")

        st.markdown(TEXT["adjustment_title"])
        adjustment_box = st.container(border=True)
        adjustment_box.metric(
            TEXT["adjustment_metric"],
            suggestion["adjustment_cm"],
        )
        adjustment_box.write(suggestion["adjustment"])

        st.markdown(TEXT["style_title"])
        if upper_lower_ratio < 0.6:
            st.warning(suggestion["advice"])
        else:
            st.info(suggestion["advice"])

        st.markdown(TEXT["reference"])
        st.write(suggestion["detail"])

        st.divider()
        st.caption(TEXT["prototype_note"])
    else:
        st.info(TEXT["click_hint"])
