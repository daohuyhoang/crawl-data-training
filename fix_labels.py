"""
Sửa lại nhãn sai trong labeled_data_bert.csv
Dùng rule-based thông minh để gán lại nhãn chính xác hơn
"""
import pandas as pd
import re
from colorama import init, Fore, Style

init()

def smart_label(text):
    """
    Gán nhãn thông minh dựa trên từ khóa
    0: Tiêu cực
    1: Khác (Trung lập/Không rõ)
    2: Tích cực
    """
    if not text or len(str(text).strip()) < 5:
        return 1
    
    text = str(text).lower()
    
    # Từ khóa TÍCH CỰC mạnh
    positive_strong = [
        'ngon', 'tuyệt', 'đỉnh', 'xuất sắc', 'tốt lắm', 'rất tốt', 'quá tốt',
        'rất ngon', 'quá ngon', 'siêu ngon', 'ngon lắm', 'ngon vl', 'ngon vcl',
        'đáng thử', 'nên thử', 'recommend', 'đáng tiền', 'rẻ mà ngon',
        'thích', 'mê', 'yêu thích', 'fan', 'ủng hộ', 'quay lại',
        'tươi', 'mềm mướt', 'thơm', 'đậm đà', 'béo ngậy', 'vừa miệng',
        'xinh', 'đẹp', 'chuẩn', 'ok', 'ổn', 'hay', 'cuốn'
    ]
    
    # Từ khóa TIÊU CỰC mạnh
    negative_strong = [
        'dở', 'tệ', 'chán', 'kém', 'tồi', 'thất vọng', 'không ngon', 'ko ngon',
        'không bao giờ quay lại', 'ko bao giờ quay lại', 'không quay lại',
        'sợ', 'kinh khủng', 'đắt mà chán', 'đắt mà dở', 'đắt mà không ngon',
        'lừa đảo', 'vô trách nhiệm', 'xấu', 'fake', 'không đáng tiền',
        'phí tiền', 'hỏng', 'sai', 'thiếu', 'nhạt nhẽo', 'khô', 'tanh',
        'hôi', 'bẩn', 'không tươi', 'drama', 'bóc phốt', 'cạch',
        'ức chế', 'ám ảnh', 'lèo tèo', 'vớ vẩn', 'dở ẹc', 'chả ngon'
    ]
    
    # Từ TRUNG LẬP
    neutral_words = [
        'bình thường', 'tạm', 'được', 'cũng được', 'tạm được',
        'không có gì đặc biệt', 'bth', 'bt'
    ]
    
    # Từ phủ định
    negation = ['không', 'ko', 'chưa', 'chẳng', 'chả', 'đừng', 'né']
    
    score = 0
    words = text.split()
    
    # Kiểm tra pattern đặc biệt trước
    if re.search(r'(không bao giờ|ko bao giờ|chưa bao giờ).*(quay lại|ăn|mua)', text):
        return 0  # Tiêu cực chắc chắn
    
    if re.search(r'(rất|cực kỳ|quá|siêu).*(ngon|tốt|đẹp|thích|hay)', text):
        return 2  # Tích cực chắc chắn
    
    if re.search(r'(rất|cực kỳ|quá|siêu).*(dở|tệ|chán|xấu|kém)', text):
        return 0  # Tiêu cực chắc chắn
    
    # Đếm từ khóa
    for i, word in enumerate(words):
        has_negation = i > 0 and words[i-1] in negation
        
        # Kiểm tra từ tích cực
        for pos in positive_strong:
            if pos in text:
                if has_negation:
                    score -= 3  # "không ngon"
                else:
                    score += 2
                break
        
        # Kiểm tra từ tiêu cực
        for neg in negative_strong:
            if neg in text:
                if has_negation:
                    score += 1  # "không dở"
                else:
                    score -= 3
                break
        
        # Kiểm tra từ trung lập
        for neu in neutral_words:
            if neu in text:
                score += 0
                break
    
    # Quyết định nhãn
    if score >= 2:
        return 2  # Tích cực
    elif score <= -2:
        return 0  # Tiêu cực
    else:
        return 1  # Khác

def fix_labels(input_file='labeled_data_bert.csv', output_file='labeled_data_fixed.csv'):
    """Sửa lại nhãn trong file"""
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║          SỬA LẠI NHÃN SAI TRONG DATA         ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    # Đọc data
    df = pd.read_csv(input_file)
    print(f"Đã tải {len(df)} dòng từ {input_file}")
    
    # Thống kê nhãn cũ
    old_counts = df['label'].value_counts().sort_index()
    print(f"\n{Fore.YELLOW}Phân bố nhãn CŨ:{Style.RESET_ALL}")
    for label, count in old_counts.items():
        label_name = ['Tiêu cực', 'Khác', 'Tích cực'][label]
        print(f"  {label} ({label_name}): {count} ({count/len(df)*100:.1f}%)")
    
    # Gán lại nhãn
    print(f"\n{Fore.YELLOW}Đang gán lại nhãn...{Style.RESET_ALL}")
    df['label_old'] = df['label']  # Backup nhãn cũ
    df['label'] = df['text'].apply(smart_label)
    
    # Thống kê nhãn mới
    new_counts = df['label'].value_counts().sort_index()
    print(f"\n{Fore.GREEN}Phân bố nhãn MỚI:{Style.RESET_ALL}")
    for label, count in new_counts.items():
        label_name = ['Tiêu cực', 'Khác', 'Tích cực'][label]
        print(f"  {label} ({label_name}): {count} ({count/len(df)*100:.1f}%)")
    
    # Đếm số nhãn thay đổi
    changed = (df['label'] != df['label_old']).sum()
    print(f"\n{Fore.CYAN}Số nhãn đã thay đổi: {changed} ({changed/len(df)*100:.1f}%){Style.RESET_ALL}")
    
    # Hiển thị mẫu thay đổi
    changed_samples = df[df['label'] != df['label_old']].head(10)
    if len(changed_samples) > 0:
        print(f"\n{Fore.CYAN}=== MẪU NHÃN ĐÃ THAY ĐỔI ==={Style.RESET_ALL}")
        for idx, row in changed_samples.iterrows():
            text = row['text'][:80] + '...' if len(row['text']) > 80 else row['text']
            old_label = ['Tiêu cực', 'Khác', 'Tích cực'][int(row['label_old'])]
            new_label = ['Tiêu cực', 'Khác', 'Tích cực'][int(row['label'])]
            print(f"\n{text}")
            print(f"  {Fore.RED}{old_label}{Style.RESET_ALL} → {Fore.GREEN}{new_label}{Style.RESET_ALL}")
    
    # Lưu file
    df_final = df[['text', 'label']]  # Bỏ cột label_old
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n{Fore.GREEN}✓ Đã lưu vào: {output_file}{Style.RESET_ALL}")
    
    # Hỏi có muốn thay thế file gốc không
    choice = input(f"\n{Fore.YELLOW}Thay thế file gốc '{input_file}'? (y/n): {Style.RESET_ALL}").strip().lower()
    if choice == 'y':
        df_final.to_csv(input_file, index=False, encoding='utf-8-sig')
        print(f"{Fore.GREEN}✓ Đã cập nhật {input_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    fix_labels()
