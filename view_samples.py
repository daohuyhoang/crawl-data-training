"""
Xem mẫu dữ liệu đã gán nhãn
"""
import pandas as pd
import sys
from colorama import init, Fore, Style

init()

def view_samples(filename='labeled_data_bert.csv', n_samples=5):
    """Hiển thị mẫu dữ liệu"""
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"{Fore.RED}Lỗi khi đọc file: {e}{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║          XEM MẪU DỮ LIỆU ĐÃ GÁN NHÃN         ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"File: {filename}")
    print(f"Tổng số: {len(df)} dòng\n")
    
    # Thống kê
    label_counts = df['label'].value_counts().sort_index()
    print(f"{Fore.CYAN}=== THỐNG KÊ ==={Style.RESET_ALL}")
    print(f"  {Fore.RED}Negative (0): {label_counts.get(0, 0)} ({label_counts.get(0, 0)/len(df)*100:.1f}%){Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Neutral (1): {label_counts.get(1, 0)} ({label_counts.get(1, 0)/len(df)*100:.1f}%){Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Positive (2): {label_counts.get(2, 0)} ({label_counts.get(2, 0)/len(df)*100:.1f}%){Style.RESET_ALL}")
    
    # Hiển thị mẫu
    print(f"\n{Fore.CYAN}=== MẪU DỮ LIỆU (Random {n_samples} dòng mỗi nhãn) ==={Style.RESET_ALL}")
    
    for label in [0, 1, 2]:
        samples = df[df['label'] == label].sample(min(n_samples, len(df[df['label'] == label])))
        
        if len(samples) > 0:
            label_name = ['NEGATIVE', 'NEUTRAL', 'POSITIVE'][label]
            label_color = [Fore.RED, Fore.YELLOW, Fore.GREEN][label]
            
            print(f"\n{label_color}{'='*60}{Style.RESET_ALL}")
            print(f"{label_color}[{label_name}]{Style.RESET_ALL}")
            print(f"{label_color}{'='*60}{Style.RESET_ALL}")
            
            for idx, row in samples.iterrows():
                text = row['text']
                # Hiển thị tối đa 150 ký tự
                if len(text) > 150:
                    text = text[:150] + '...'
                print(f"\n{idx+1}. {text}")

if __name__ == "__main__":
    # Lấy số lượng mẫu từ argument (mặc định 5)
    n = 5
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except:
            pass
    
    view_samples(n_samples=n)
