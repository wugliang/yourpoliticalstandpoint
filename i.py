# -*- coding: utf-8 -*-

import time
import json
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

def calculate_mbti_type(scores):
    mbti_type = ""
    score_1 = 0
    score_2 = 0
    for question_number, question_scores in scores.items():
        score_1 += question_scores[0]
        score_2 += question_scores[1]

    if score_1 > 2:
        mbti_type += "T"
    elif 2 >= score_1 >= -2:
        mbti_type += "M"
    else:
        mbti_type += "C"
    mbti_type += "P" if score_2 > 0 else "S"
    return mbti_type


if 'page' not in st.session_state:
    st.session_state['page'] = 0

def personality_test():
    captions = ["早上起床，你按照慣例打開電視...", 
                "出門前，你看到信箱裡的選舉公報...",
                "你和一群朋友一起吃早餐時...",
                "你隨手拿起一旁的報紙",
                "放學之後，在運動場看到即將代表出戰巴黎奧運的國手同學",
                ]
    
    questions = {
        "在新聞上看到共機繞台的新聞": {
            "太可惡了!中國一天到晚打台灣的壞主意!": (1,1),
            "也不是第一次了，共機在哪裡飛跟我沒關係吧…": (0.5,-1),
            "以前就不會被騷擾，這幾年越來越多，是執政黨的問題吧?": (-0.5,-0.5),
            "台灣是中國的領土，這很正常吧!": (-1,-1)
        },
        "這次的選舉主軸還是圍繞著兩岸關係吧": {
            "我覺得這樣很重要，中國的威脅關乎台灣的安全與未來發展。": (1,0.5),
            "感覺這只是政客們的舞台表演，真正解決問題的方式是什麼？": (0,1),
            "這是理所當然的，我們不能和中國切割開來。": (-1,1)
        },
        "發現身邊的朋友非常熱忠政治，你們的立場又很類似，你決定…": {
            "和他一起大談政治、參與政治活動，表達自己的理念。": (0,1),
            "不習慣和別人談論政治，默默聽他談論時事議題。": (0,-1),
            "嘗試將政治討論轉化為建設性的對話，探討彼此立場的來源和可能的共通點。":(0,0)
        },
        "看到許多來自台灣的歌手在春晚上合唱「我的祖國」的報導": {
            "可以理解他們只是在遵守政治要求，表達對中國的尊重。": (-0.5,0),
            "和他們一樣真心希望祖國繁盛昌隆。": (-1,0),
            "我覺得這種行為有點虛偽，只是在迎合觀眾或政治壓力。": (0.5,0),
            "在利益面前矮化自己出生的國家，真是忘恩負義。": (1,0)
        },
        "今年的選手還是身披中華台北的旗幟": {
            "每屆都這樣已經習慣了~還是別惹隔壁的老大哥。": (-0.5,-1), 
            "這些來自中國的打壓真是沒完沒了，但不妨礙選手讓台灣站上世界的舞台!": (1,1),
            "我認為這是台灣選手的驕傲，真是可惜。": (0.5,-0.5), 
            "這是一個和對岸友好的姿態，表達對於和平與合作的願望，值得肯定。": (-1,1)
        },
    }
    
    questions_info = [
        { 
            "question": "在新聞上看到共機繞台的新聞",
            "options": ["太可惡了!中國一天到晚打台灣的壞主意!", "也不是第一次了，共機在哪裡飛跟我沒關係吧…", "以前就不會被騷擾，這幾年越來越多，是執政黨的問題吧?", "台灣是中國的領土，這很正常吧!"]
        },
        {
            "question": "這次的選舉主軸還是圍繞著兩岸關係吧",
            "options": ["我覺得這樣很重要，中國的威脅關乎台灣的安全與未來發展。", "感覺這只是政客們的舞台表演，真正解決問題的方式是什麼？", "這是理所當然的，我們不能和中國切割開來。"]
        },
        {
            "question": "發現身邊的朋友非常熱忠政治，你們的立場又很類似，你決定…",
            "options": ["和他一起大談政治、參與政治活動，表達自己的理念。","不習慣和別人談論政治，默默聽他談論時事議題。", "嘗試將政治討論轉化為建設性的對話，探討彼此立場的來源和可能的共通點。"]
        },
        {
            "question": "看到許多來自台灣的歌手在春晚上合唱「我的祖國」的報導",
            "options": ["可以理解他們只是在遵守政治要求，表達對中國的尊重。","和他們一樣真心希望祖國繁盛昌隆。","我覺得這種行為有點虛偽，只是在迎合觀眾或政治壓力。", "在利益面前矮化自己出生的國家，真是忘恩負義。"]
        },
        {
            "question": "今年的選手還是身披中華台北的旗幟",
            "options": ["每屆都這樣已經習慣了~還是別惹隔壁的老大哥。","這些來自中國的打壓真是沒完沒了，但不妨礙選手讓台灣站上世界的舞台!","我認為這是台灣選手的驕傲，真是可惜。", "這是一個和對岸友好的姿態，表達對於和平與合作的願望，值得肯定。"]
        },
    ]

    def update_score(selected_option=None, question_number=None):
        if selected_option is not None and question_number is not None:
            option_scores = questions[questions_info[question_number-1]['question']][selected_option]
            score_change = option_scores  # 將選擇的分數設置為該問題的分數
            st.session_state.scores[question_number] = score_change

    place_image = {
        "Q1_Q": "https://i.imgur.com/wlH7amz.png",  # for Q1
        "Q2_Q": "https://i.imgur.com/fnNhIkj.png",  # for Q2
        "Q3_Q": "https://i.imgur.com/weN1w3H.png",  # for Q3
        "Q4_Q": "https://i.imgur.com/k2xhZxs.png",  # for Q4
        "Q5_Q": "https://i.imgur.com/yPWkUP9.png",  # for Q5
    }
    personality_trans = {
    "TP": "台灣黑熊",
    "MP": "石虎",
    "CP": "台灣獼猴",
    "TS": "梅花鹿",
    "MS": "櫻花鉤吻鮭",
    "CS": "穿山甲",
    }
    if 'scores' not in st.session_state:
        st.session_state['scores'] = {i + 1: (0, 0) for i in range(len(questions_info))}  # 初始化 scores

    if 'selected_option' not in st.session_state:
        st.session_state['selected_option'] = None

    def next_page():
        st.session_state['page'] += 1 

    def go_back():
        st.session_state['page'] -= 1

    st.title("選民的奇妙冒險：找出你的政治替身")

    if st.session_state['page'] < len(questions_info):
        index = st.session_state['page']
        
        # 加上圖片
        image_key = f"Q{index + 1}_Q"
        if image_key in place_image:
            st.image(place_image[image_key], use_column_width=True)

        st.subheader(captions[index])
        q = questions_info[index]['question']
        st.write(q)
        
        for i, option in enumerate(questions_info[index]["options"], start=1):
            weight = 1 if st.session_state.get("selected_option") == i else 0.5
            if st.button(option, type="secondary", key=i, help=str(weight), use_container_width=True):
                st.session_state['selected_option'] = i
                selected_index = i - 1
                selected_option = questions_info[index]["options"][selected_index]
                update_score(selected_option=selected_option, question_number=index+1)  # 調用更新分數函數

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            if st.session_state['page'] == 0:
                st.button("上一題", on_click=go_back, disabled=True, use_container_width=True)
            else:
                st.button("上一題", on_click=go_back, use_container_width=True)
        with col2:
            st.button("下一題", on_click=next_page, use_container_width=True)

    else:
        st.title("測驗結果")
        Type=calculate_mbti_type(st.session_state['scores'])
        st.write("你的 MBTI 類型是：", personality_trans[Type])  # Assuming you have a function to calculate MBTI type

personality_test()
