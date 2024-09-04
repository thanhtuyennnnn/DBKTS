import pandas as pd
from googletrans import Translator

# Khởi tạo đối tượng Translator
translator = Translator()

# Đọc dữ liệu từ file CSV
file_path = r'D:\Downloads\DATA_IMF_BOP_API.csv'
df = pd.read_csv(file_path, encoding='latin1')

# Dịch văn bản trong cột 'Indicator Name'
def translate_text(text):
    if pd.isna(text):
        print(f"Skipping translation for NaN value.")
        return text
    try:
        print(f"Translating: {text}")
        translation = translator.translate(text, src='en', dest='vi')
        print(f"Translation result: {translation.text}")
        return translation.text
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

if 'Indicator Name' in df.columns:
    # Áp dụng dịch cho cột 'Indicator Name'
    df['Indicator Name (Vietnamese)'] = df['Indicator Name'].apply(translate_text)
    # Lưu DataFrame đã dịch vào file CSV mới với mã hóa UTF-8
    df.to_csv(r'D:\Downloads\DATA_WORLDBANK_ALL_API_translated.csv', index=False, encoding='utf-8')
else:
    print("Cột 'Indicator Name' không tồn tại trong DataFrame.")
