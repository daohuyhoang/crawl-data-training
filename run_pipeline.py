"""
Pipeline tự động: Crawl → Gán nhãn
Chạy file này để tự động crawl và gán nhãn liên tục
"""
import subprocess
import sys
from colorama import init, Fore, Style

init()

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{description}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Lỗi khi chạy: {e}{Style.RESET_ALL}")
        return False

def main():
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║     PIPELINE TỰ ĐỘNG: CRAWL → GÁN NHÃN BẰNG AI      ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print("Chọn chế độ:")
    print("1. Chỉ crawl dữ liệu")
    print("2. Chỉ gán nhãn (cho data đã crawl)")
    print("3. Crawl + Gán nhãn (pipeline đầy đủ)")
    
    choice = input("\nNhập lựa chọn (1/2/3): ").strip()
    
    if choice == '1':
        run_command("python fb_scraper.py", "BƯỚC 1: CRAWL DỮ LIỆU TỪ FACEBOOK")
        
    elif choice == '2':
        run_command("python auto_label_bert.py", "BƯỚC 2: GÁN NHÃN TỰ ĐỘNG BẰNG PHOBERT")
        
    elif choice == '3':
        print(f"\n{Fore.YELLOW}Bắt đầu pipeline đầy đủ...{Style.RESET_ALL}")
        
        if run_command("python fb_scraper.py", "BƯỚC 1: CRAWL DỮ LIỆU TỪ FACEBOOK"):
            print(f"\n{Fore.GREEN}✓ Crawl hoàn thành!{Style.RESET_ALL}")
            
            proceed = input(f"\n{Fore.YELLOW}Tiếp tục gán nhãn? (y/n): {Style.RESET_ALL}").strip().lower()
            
            if proceed == 'y':
                if run_command("python auto_label_bert.py", "BƯỚC 2: GÁN NHÃN TỰ ĐỘNG BẰNG PHOBERT"):
                    print(f"\n{Fore.GREEN}✓ Pipeline hoàn thành!{Style.RESET_ALL}")
                    print(f"\n{Fore.CYAN}Dữ liệu đã được lưu vào: labeled_data_bert.csv{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}✗ Gán nhãn thất bại!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}Dừng pipeline. Bạn có thể chạy gán nhãn sau bằng: python auto_label_bert.py{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}✗ Crawl thất bại!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Lựa chọn không hợp lệ!{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Đã dừng pipeline.{Style.RESET_ALL}")
        sys.exit(0)
