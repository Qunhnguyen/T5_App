from happytransformer import HappyTextToText, TTSettings
import pandas as pd

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

# Danh sách lưu kết quả
results = []

while True:
    text_to_correct = input("Nhập câu cần sửa (hoặc gõ 'exit' để kết thúc): ")
    if text_to_correct.lower() == "exit":
        break

    prompt = f"grammar: {text_to_correct}"
    result = happy_tt.generate_text(prompt, args=args)

    print("✅ Câu sau khi sửa:", result.text)
    print("-----------")

    # Thêm vào danh sách
    results.append({
        "Original": text_to_correct,
        "Corrected": result.text
    })

# Ghi file CSV sau khi kết thúc
df = pd.DataFrame(results)
df.to_csv("grammar_corrections.csv", index=False, encoding='utf-8-sig')
print("📁 Đã lưu kết quả vào file: grammar_corrections.csv")
