import pandas as pd
import os

def clean_csv(file_path):
    if not os.path.exists(file_path):
        print("File không tồn tại!")
        return

    df = pd.read_csv(file_path)
    initial_count = len(df)
    
    # 1. Loại bỏ khoảng trắng thừa ở đầu/cuối
    df['text'] = df['text'].str.strip()
    
    # 2. Xóa các dòng rác (quảng cáo, sim, số điện thoại)
    # Tìm các từ khóa rác
    junk_keywords = ['hotline', 'zalo', '096', 'sim', 'iphone', 'auto ios', 'miễn phí']
    df = df[~df['text'].str.contains('|'.join(junk_keywords), case=False, na=False)]
    
    # 3. Sắp xếp theo độ dài giảm dần
    # Mục đích: Nếu có 2 câu trùng nhau nhưng 1 câu bị "... See more" (ngắn hơn) 
    # thì ta giữ lại câu dài hơn (bản đầy đủ).
    df['length'] = df['text'].str.len()
    df = df.sort_values('length', ascending=False)
    
    # 4. Loại bỏ trùng lặp nội dung
    df = df.drop_duplicates(subset=['text'], keep='first')
    
    # 5. Xử lý trường hợp "See more": 
    # Nếu câu A là tập con khởi đầu của câu B, thì xóa câu A.
    final_indices = []
    texts = df['text'].tolist()
    for i in range(len(texts)):
        is_substring = False
        for j in range(len(texts)):
            if i != j and texts[i] in texts[j]:
                is_substring = True
                break
        if not is_substring:
            final_indices.append(df.index[i])
            
    df = df.loc[final_indices]
    
    # Dọn dẹp lại cấu hình file
    df = df.drop(columns=['length'])
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    
    print(f"Bắt đầu: {initial_count} dòng")
    print(f"Hiện tại: {len(df)} dòng (Đã xoá {initial_count - len(df)} dòng trùng/rác)")

if __name__ == "__main__":
    clean_csv('crawled_fb.csv')
