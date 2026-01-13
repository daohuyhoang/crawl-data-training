"""
Kiểm tra trạng thái hệ thống và dữ liệu
"""
import pandas as pd
import os
from colorama import init, Fore, Style

init()

def check_file_status(filename):
    """Kiểm tra trạng thái file"""
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            return True, len(df)
        except:
            return True, 0
    return False, 0

def main():
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║        TRẠNG THÁI HỆ THỐNG DỮ LIỆU          ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    # Kiểm tra crawled_fb.csv
    exists, count = check_file_status('crawled_fb.csv')
    if exists:
        if count > 0:
            print(f"{Fore.YELLOW}📥 crawled_fb.csv: {count} dòng chưa gán nhãn{Style.RESET_ALL}")
            print(f"   → Chạy 'python auto_label_bert.py' để gán nhãn")
        else:
            print(f"{Fore.GREEN}✓ crawled_fb.csv: Trống (đã xử lý hết){Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ crawled_fb.csv: Không tồn tại{Style.RESET_ALL}")
    
    # Kiểm tra labeled_data_bert.csv
    exists, count = check_file_status('labeled_data_bert.csv')
    if exists:
        if count > 0:
            df = pd.read_csv('labeled_data_bert.csv')
            neg = (df['label'] == 0).sum()
            neu = (df['label'] == 1).sum()
            pos = (df['label'] == 2).sum()
            
            print(f"\n{Fore.GREEN}✓ labeled_data_bert.csv: {count} dòng đã gán nhãn{Style.RESET_ALL}")
            print(f"   {Fore.RED}• Negative: {neg} ({neg/count*100:.1f}%){Style.RESET_ALL}")
            print(f"   {Fore.YELLOW}• Neutral: {neu} ({neu/count*100:.1f}%){Style.RESET_ALL}")
            print(f"   {Fore.GREEN}• Positive: {pos} ({pos/count*100:.1f}%){Style.RESET_ALL}")
            print(f"   → Sẵn sàng để train model!")
        else:
            print(f"\n{Fore.YELLOW}⚠ labeled_data_bert.csv: Trống{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}✗ labeled_data_bert.csv: Không tồn tại{Style.RESET_ALL}")
    
    # Kiểm tra model files
    print(f"\n{Fore.CYAN}--- Model Files ---{Style.RESET_ALL}")
    model_files = ['sentiment_model.pkl', 'tfidf_vectorizer.pkl']
    for mf in model_files:
        if os.path.exists(mf):
            size_mb = os.path.getsize(mf) / (1024 * 1024)
            print(f"{Fore.GREEN}✓ {mf}: {size_mb:.2f} MB{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ {mf}: Chưa train{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}💡 Gợi ý tiếp theo:{Style.RESET_ALL}")
    
    crawl_exists, crawl_count = check_file_status('crawled_fb.csv')
    labeled_exists, labeled_count = check_file_status('labeled_data_bert.csv')
    
    if crawl_count > 0:
        print(f"   1. Chạy 'python auto_label_bert.py' để gán nhãn {crawl_count} dòng mới")
    else:
        print(f"   1. Chạy 'python fb_scraper.py' để crawl thêm dữ liệu")
    
    if labeled_count > 100:
        print(f"   2. Chạy 'python train.py' để train model với {labeled_count} dòng data")
    elif labeled_count > 0:
        print(f"   2. Cần thêm data (hiện có {labeled_count}, nên có ít nhất 100 dòng)")

if __name__ == "__main__":
    main()
