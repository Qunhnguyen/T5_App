import streamlit as st
from happytransformer import HappyTextToText, TTSettings
import pandas as pd
import os
# 🛠 GỌI NGAY ĐẦU TIÊN
st.set_page_config(page_title="Grammar Correction", page_icon="📝")

# Cache mô hình để không load lại mỗi lần nhấn nút
@st.cache_resource
def load_model():
    return HappyTextToText("T5", "vennify/t5-base-grammar-correction")

# Khởi tạo mô hình
happy_tt = load_model()
args = TTSettings(num_beams=5, min_length=1)

# Giao diện web
st.title("📝 Grammar Correction App")
st.markdown("Nhập câu sai ngữ pháp vào bên dưới và nhấn **Sửa lỗi**:")

input_text = st.text_area("✍️ Câu cần sửa:", height=150)

if st.button("Sửa lỗi"):
    if input_text.strip():
        with st.spinner("⏳ Đang xử lý..."):
            prompt = f"grammar: {input_text}"
            result = happy_tt.generate_text(prompt, args=args)
        st.success("✅ Câu sau khi sửa:")
        st.write(result.text)
        csv_file = "grammar_corrections.csv"
        new_data = {"Original": input_text, "Corrected": result.text}

        # Nếu file đã tồn tại, nối thêm dòng mới
        if os.path.exists(csv_file):
            df_old = pd.read_csv(csv_file)
            df_new = pd.concat([df_old, pd.DataFrame([new_data])], ignore_index=True)
        else:
            df_new = pd.DataFrame([new_data])

        df_new.to_csv(csv_file, index=False, encoding="utf-8-sig")
        st.info("📁 Kết quả đã được lưu vào 'grammar_corrections.csv'")
        
    else:
        st.warning("⚠️ Bạn chưa nhập nội dung.")
