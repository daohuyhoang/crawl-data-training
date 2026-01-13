import pandas as pd
import os

def clean_csv(file_path):
    if not os.path.exists(file_path):
        print("File không tồn tại!")
        return

    df = pd.read_csv(file_path)
    initial_count = len(df)
    
    df['text'] = df['text'].str.strip()
    
    junk_keywords = ['hotline', 'zalo', '096', 'sim', 'iphone', 'auto ios', 'miễn phí']
    df = df[~df['text'].str.contains('|'.join(junk_keywords), case=False, na=False)]
    
    df['length'] = df['text'].str.len()
    df = df.sort_values('length', ascending=False)
    
    df = df.drop_duplicates(subset=['text'], keep='first')

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
    
    df = df.drop(columns=['length'])
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    
    print(f"Bắt đầu: {initial_count} dòng")
    print(f"Hiện tại: {len(df)} dòng (Đã xoá {initial_count - len(df)} dòng trùng/rác)")

if __name__ == "__main__":
    clean_csv('crawled_fb.csv')
