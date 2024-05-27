import streamlit as st
import itertools
import random
from st_clickable_images import clickable_images
import base64
import os

# Function to evaluate the expression
def eval_expression(expression):
    try:
        return eval(expression)
    except ZeroDivisionError:
        return None

# Function to check if the cards can make 24
def can_make_24(cards):
    operations = ['+', '-', '*', '/']
    value_combinations = itertools.product(*[card_values(card) for card in cards])
    for nums in value_combinations:
        for ops in itertools.product(operations, repeat=3):
            expressions = [
                f"({nums[0]}{ops[0]}{nums[1]}){ops[1]}({nums[2]}{ops[2]}{nums[3]})",
                f"(({nums[0]}{ops[0]}{nums[1]}){ops[1]}{nums[2]}){ops[2]}{nums[3]}",
                f"{nums[0]}{ops[0]}(({nums[1]}{ops[1]}{nums[2]}){ops[2]}{nums[3]})",
                f"{nums[0]}{ops[0]}({nums[1]}{ops[1]}({nums[2]}{ops[2]}{nums[3]}))",
                f"({nums[0]}{ops[0]}({nums[1]}{ops[1]}{nums[2]})){ops[2]}{nums[3]}"
            ]
            for expr in expressions:
                if eval_expression(expr) == 24:
                    return True, expr
    return False, ""

# Function to get card values
def card_values(card):
    if card == 'A':
        return [1, 14]  # A can be 1 or 14
    elif card in ['J', 'Q', 'K']:
        return [11, 12, 13][['J', 'Q', 'K'].index(card):['J', 'Q', 'K'].index(card)+1]
    else:
        return [int(card)]

def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# # 图片路径
# card_images = {
#     "A": "/content/Spade_A.png",
#     "2": "/content/Spade_2.png",
#     "3": "/content/Spade_3.png",
#     "4": "/content/Spade_4.png",
#     "5": "/content/Spade_5.png",
#     "6": "/content/Spade_6.png",
#     "7": "/content/Spade_7.png",
#     "8": "/content/Spade_8.png",
#     "9": "/content/Spade_9.png",
#     "10": "/content/Spade_10.png",
#     "J": "/content/Spade_J.png",
#     "Q": "/content/Spade_Q.png",
#     "K": "/content/Spade_K.png"
# }

# 图片路径
card_images = {
    "A": "Spade_A.png",
    "2": "Spade_2.png",
    "3": "Spade_3.png",
    "4": "Spade_4.png",
    "5": "Spade_5.png",
    "6": "Spade_6.png",
    "7": "Spade_7.png",
    "8": "Spade_8.png",
    "9": "Spade_9.png",
    "10": "Spade_10.png",
    "J": "Spade_J.png",
    "Q": "Spade_Q.png",
    "K": "Spade_K.png"
}

# 转换为Base64
base64_images = {card: f"data:image/png;base64,{get_image_as_base64(path)}" for card, path in card_images.items()}

st.title("24点游戏 - 选择卡牌")

# 初始化或获取session state
if 'clicked_cards' not in st.session_state:
    st.session_state.clicked_cards = []
if 'drawn_cards' not in st.session_state:
    st.session_state.drawn_cards = []
if 'card_counts' not in st.session_state:
    st.session_state.card_counts = {card: 0 for card in card_images}
if 'click_result' not in st.session_state:
    st.session_state.click_result = (False, "")
if 'draw_result' not in st.session_state:
    st.session_state.draw_result = (False, "")

tab1, tab2 = st.tabs(["点击选择", "随机抽取"])

with tab1:
    clicked = clickable_images(
        [base64_images[card] for card in base64_images],
        titles=list(base64_images.keys()),
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "150px"}
    )

    if 'selection_confirmed' not in st.session_state:
        st.session_state.selection_confirmed = False  # 初始化标志位

    if st.button("重置选择"):
        st.session_state.selection_confirmed = False
        st.session_state.clicked_cards = []
        st.session_state.card_counts = {card: 0 for card in card_images}
        st.session_state.click_result = (False, "")
    
    if len(st.session_state.clicked_cards) == 4:
        if st.button("确认你的选择"):
            st.session_state.selection_confirmed = True  # 设置标志位为True
            st.session_state.click_result = can_make_24(st.session_state.clicked_cards)
            st.write("可以组合成24点!" if st.session_state.click_result[0] else "不能组合成24点.")
        if st.session_state.click_result[0] and st.button("查看运算方法"):
            st.write(f"一个成功的表达式是：{st.session_state.click_result[1]}")

    if clicked > -1 and not st.session_state.selection_confirmed:
        selected_card = list(base64_images.keys())[clicked]
        if st.session_state.card_counts[selected_card] < 4:
            if len(st.session_state.clicked_cards) >= 4:
                oldest_card = st.session_state.clicked_cards.pop(0)
                st.session_state.card_counts[oldest_card] -= 1
            st.session_state.clicked_cards.append(selected_card)
            st.session_state.card_counts[selected_card] += 1
    
    if st.session_state.clicked_cards:
        cols = st.columns(len(st.session_state.clicked_cards))
        for idx, card in enumerate(st.session_state.clicked_cards):
            with cols[idx]:
                st.image(base64_images[card], caption=card, width=115)

with tab2:
    # 抽取卡牌按钮
    if st.button("抽取卡牌"):
        # 直接从所有卡牌中随机选取，允许重复
        st.session_state.drawn_cards = random.choices(list(card_images.keys()), k=4)

    # 清空选择按钮
    if st.button("清空抽取卡牌"):
        st.session_state.drawn_cards = []

    # 显示已抽取的卡牌
    if st.session_state.drawn_cards:
        st.write("抽取的卡牌:")
        cols = st.columns(4)
        for idx, card in enumerate(st.session_state.drawn_cards):
            with cols[idx]:
                st.image(base64_images[card], caption=card, width=115)
    else:
        st.write("未抽取任何卡牌")
    
    if st.session_state.drawn_cards and len(st.session_state.drawn_cards) == 4:
        if st.button("确认抽取卡牌"):
            st.session_state.draw_result = can_make_24(st.session_state.drawn_cards)
            st.write("可以组合成24点!" if st.session_state.draw_result[0] else "不能组合成24点.")
        
        if st.session_state.draw_result[0]:  # 确保结果已确认为True后显示查看按钮
            if st.button("查看运算方法"):
                st.write(f"一个成功的表达式是：{st.session_state.draw_result[1]}")
