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
    "core_advice": "#### \u6838\u5fc3\u5efa\u8bae",
    "reference": "#### \u53c2\u8003\u8bf4\u660e",
    "prototype_note": (
        "\u5f53\u524d\u7248\u672c\u4e3a\u57fa\u7840 UI \u793a\u4f8b\uff0c"
        "\u6682\u672a\u63a5\u5165\u771f\u5b9e\u4eba\u4f53\u5173\u952e\u70b9"
        "\u8bc6\u522b\u6216\u56fe\u50cf\u6d4b\u91cf\u6a21\u578b\u3002"
    ),
}


def build_suggestion(height_cm: int, upper_lower_ratio: float) -> dict[str, str]:
    if upper_lower_ratio >= 0.62:
        waistline_cm = 1
        ratio_comment = (
            "\u4f60\u7684\u6bd4\u4f8b\u5df2\u7ecf\u6bd4\u8f83\u63a5\u8fd1"
            "\u9ad8\u8170\u663e\u817f\u957f\u7684\u89c6\u89c9\u6548\u679c\u3002"
        )
    elif upper_lower_ratio >= 0.56:
        waistline_cm = 3
        ratio_comment = (
            "\u5f53\u524d\u6bd4\u4f8b\u4e2d\u7b49\uff0c"
            "\u53ef\u4ee5\u901a\u8fc7\u8170\u7ebf\u4f4d\u7f6e"
            "\u548c\u989c\u8272\u5ef6\u4f38\u6765\u4f18\u5316\u3002"
        )
    else:
        waistline_cm = 5
        ratio_comment = (
            "\u5f53\u524d\u89c6\u89c9\u8170\u7ebf\u504f\u4f4e\uff0c"
            "\u5efa\u8bae\u4f18\u5148\u62c9\u9ad8\u8170\u7ebf\u5e76"
            "\u51cf\u5c11\u4e0a\u4e0b\u88c5\u622a\u65ad\u3002"
        )

    ideal_waistline = round(height_cm * 0.43)

    return {
        "waistline": (
            f"\u5efa\u8bae\u63d0\u9ad8\u8170\u7ebf\u7ea6 {waistline_cm}cm"
        ),
        "color": (
            "\u5efa\u8bae\u5185\u642d\u987a\u8272\uff0c"
            "\u51cf\u5c11\u8170\u8179\u5904\u5206\u5272\u611f"
        ),
        "fit": (
            "\u4f18\u5148\u9009\u62e9\u9ad8\u8170\u4e0b\u88c5\u3001"
            "\u77ed\u6b3e\u5916\u5957\u6216\u585e\u8863\u89d2\u7684\u7a7f\u6cd5"
        ),
        "detail": (
            f"\u53ef\u628a\u89c6\u89c9\u8170\u7ebf\u63a7\u5236\u5728"
            f"\u8ddd\u5934\u9876\u7ea6 {ideal_waistline}cm \u9644\u8fd1\uff0c"
            "\u518d\u6839\u636e\u7167\u7247\u5fae\u8c03\u3002"
        ),
        "ratio_comment": ratio_comment,
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
        if uploaded_file is None:
            st.warning(TEXT["upload_warning"])
        else:
            suggestion = build_suggestion(height_cm, upper_lower_ratio)

            st.success(suggestion["ratio_comment"])

            metric_col_1, metric_col_2 = st.columns(2)
            metric_col_1.metric(TEXT["height_metric"], f"{height_cm}cm")
            metric_col_2.metric(TEXT["ratio_metric"], f"{upper_lower_ratio:.2f}")

            st.markdown(TEXT["core_advice"])
            st.write(f"- {suggestion['waistline']}")
            st.write(f"- {suggestion['color']}")
            st.write(f"- {suggestion['fit']}")

            st.markdown(TEXT["reference"])
            st.write(suggestion["detail"])

            st.divider()
            st.caption(TEXT["prototype_note"])
    else:
        st.info(TEXT["click_hint"])
