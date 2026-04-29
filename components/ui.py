import streamlit as st


def cp_hero(title: str, subtitle: str | None = None, icon: str = "⭐"):
    st.markdown(f"""
    <div class='cp-hero'>
      <div class='cp-hero-icon'>{icon}</div>
      <div>
        <div class='cp-hero-title'>{title}</div>
        {f"<div class='cp-sub'>{subtitle}</div>" if subtitle else ''}
      </div>
    </div>
    """, unsafe_allow_html=True)


def cp_card(start=True, end=True):
    if start:
        st.markdown("<div class='cp-card'>", unsafe_allow_html=True)
    else:
        return
    # caller must call cp_card_end()


def cp_card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def cp_primary_button(label: str, key: str | None = None):
    key = key or label
    return st.button(label, key=key)


def cp_secondary_button(label: str, key: str | None = None):
    key = key or label + "_sec"
    return st.button(label, key=key)


def cp_card_back():
    """Start a background card that will stay visually behind a data panel.

    Use `cp_card_back()` then render the background content (e.g. summary/filters),
    then call `cp_data_panel_start()` to open the front table container and
    finish with `cp_data_panel_end()`. The helper now renders the background
    card closed immediately so the data panel (a sibling) can be placed after
    and visually overlay it.
    """
    # open a background card; caller should close it with `cp_card_back_end()`
    st.markdown("<div class='cp-card back-card'>", unsafe_allow_html=True)


def cp_card_back_end():
    st.markdown("</div>", unsafe_allow_html=True)


def cp_data_panel_start():
    st.markdown("<div class='data-panel'><div class='data-table-surface'>", unsafe_allow_html=True)


def cp_data_panel_end():
    st.markdown("</div></div>", unsafe_allow_html=True)
