import streamlit as st
import itertools

def eval_expression(expression):
    try:
        return eval(expression)
    except ZeroDivisionError:
        return None

def can_make_24(cards):
    operations = ['+', '-', '*', '/']
    # Generate all value combinations for the cards including A as 1 and 14
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

def card_values(card):
    """Return possible numerical values for a card."""
    if card == 'A':
        return [1, 14]  # A can be 1 or 14
    elif card in ['J', 'Q', 'K']:
        return [11, 12, 13][['J', 'Q', 'K'].index(card):['J', 'Q', 'K'].index(card)+1]
    else:
        return [int(card)]

# Initialize session state for selected cards and result
if 'selected_cards' not in st.session_state:
    st.session_state.selected_cards = []
if 'result' not in st.session_state:
    st.session_state.result = (False, "")

# Load card images
card_images = {card: f"Spade_{card}.png" for card in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]}

st.title("24点游戏")

cards = list(card_images.keys())
rows = [cards[i*4:(i+1)*4] for i in range(3)] + [cards[12:]]  # Create rows of cards

for row in rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        with cols[i]:
            img_path = card_images[card]
            if st.button('', key=card):
                if card in st.session_state.selected_cards:
                    st.session_state.selected_cards.remove(card)
                else:
                    if len(st.session_state.selected_cards) < 4:
                        st.session_state.selected_cards.append(card)
            if card in st.session_state.selected_cards:
                st.image(img_path, caption=f"{card} (Selected)", width=100)
            else:
                st.image(img_path, caption=card, width=100)

if len(st.session_state.selected_cards) == 4:
    if st.button("确认你的选择"):
        st.session_state.result = can_make_24(st.session_state.selected_cards)
        st.write("可以组合成24点!" if st.session_state.result[0] else "不能组合成24点.")

if st.session_state.result[0]:
    if st.button("查看运算方法"):
        st.write(f"一个成功的表达式是：{st.session_state.result[1]}")
