import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from tqdm import tqdm
from colorama import init, Fore, Style

init()

class VietnameseSentimentLabeler:
    def __init__(self, model_name="wonrax/phobert-base-vietnamese-sentiment"):
        """
        Khởi tạo model PhoBERT cho sentiment analysis tiếng Việt
        Model: wonrax/phobert-base-vietnamese-sentiment
        - 0: Negative (tiêu cực)
        - 1: Neutral (trung lập)  
        - 2: Positive (tích cực)
        """
        print(f"{Fore.CYAN}=== KHỞI TẠO MODEL PHOBERT ==={Style.RESET_ALL}")
        print(f"Đang tải model: {model_name}...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval()
            
            device_name = "GPU" if torch.cuda.is_available() else "CPU"
            print(f"{Fore.GREEN}✓ Model đã sẵn sàng! (Chạy trên {device_name}){Style.RESET_ALL}\n")
        except Exception as e:
            print(f"{Fore.RED}Lỗi khi tải model: {e}{Style.RESET_ALL}")
            raise
    
    def predict_sentiment(self, text):
        """
        Dự đoán sentiment cho một đoạn text
        Returns: 0 (Negative), 1 (Neutral), 2 (Positive)
        """
        if not text or len(str(text).strip()) < 3:
            return 1 
        
        try:
            inputs = self.tokenizer(
                str(text), 
                return_tensors="pt", 
                truncation=True, 
                max_length=256,
                padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_class = torch.argmax(predictions, dim=-1).item()
            
            return predicted_class
        except Exception as e:
            print(f"{Fore.YELLOW}Cảnh báo: Lỗi khi xử lý text, trả về Neutral. Lỗi: {e}{Style.RESET_ALL}")
            return 1
    
    def label_dataframe(self, df, text_column='text', batch_size=32):
        """
        Gán nhãn cho toàn bộ DataFrame
        """
        print(f"{Fore.CYAN}=== BẮT ĐẦU GÁN NHÃN ==={Style.RESET_ALL}")
        print(f"Tổng số dòng: {len(df)}")
        print(f"Đang xử lý...\n")
        
        labels = []
        
        for text in tqdm(df[text_column], desc="Gán nhãn", unit="dòng"):
            label = self.predict_sentiment(text)
            labels.append(label)
        
        df['label'] = labels
        return df

def auto_label_with_bert(input_file='crawled_fb.csv', output_file='labeled_data_bert.csv'):
    """
    Tự động gán nhãn bằng PhoBERT và append vào file output
    Sau đó xóa data đã xử lý khỏi file input
    """
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║  TỰ ĐỘNG GÁN NHÃN BẰNG PHOBERT (AI MODEL)   ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    try:
        print(f"Đang đọc file: {input_file}...")
        df_new = pd.read_csv(input_file)
        
        if len(df_new) == 0:
            print(f"{Fore.YELLOW}File {input_file} trống! Không có gì để gán nhãn.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}✓ Đã tải {len(df_new)} dòng dữ liệu mới{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}Lỗi khi đọc file: {e}{Style.RESET_ALL}")
        return
    
    labeler = VietnameseSentimentLabeler()
    
    df_new = labeler.label_dataframe(df_new, text_column='text')
    
    label_counts = df_new['label'].value_counts().sort_index()
    print(f"\n{Fore.GREEN}✓ HOÀN THÀNH GÁN NHÃN!{Style.RESET_ALL}")
    print(f"\n{Fore.CYAN}=== THỐNG KÊ NHÃN (DATA MỚI) ==={Style.RESET_ALL}")
    print(f"  {Fore.RED}Negative (0): {label_counts.get(0, 0)} bình luận ({label_counts.get(0, 0)/len(df_new)*100:.1f}%){Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Neutral (1): {label_counts.get(1, 0)} bình luận ({label_counts.get(1, 0)/len(df_new)*100:.1f}%){Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Positive (2): {label_counts.get(2, 0)} bình luận ({label_counts.get(2, 0)/len(df_new)*100:.1f}%){Style.RESET_ALL}")
    
    try:
        import os
        if os.path.exists(output_file):
            print(f"\n{Fore.YELLOW}Đang append vào file hiện có: {output_file}...{Style.RESET_ALL}")
            df_existing = pd.read_csv(output_file)
            
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined = df_combined.drop_duplicates(subset=['text'], keep='first')
            
            print(f"  • Data cũ: {len(df_existing)} dòng")
            print(f"  • Data mới: {len(df_new)} dòng")
            print(f"  • Sau khi gộp (loại trùng): {len(df_combined)} dòng")
            
            df_combined.to_csv(output_file, index=False, encoding='utf-8-sig')
        else:
            print(f"\n{Fore.YELLOW}Tạo file mới: {output_file}...{Style.RESET_ALL}")
            df_new.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"{Fore.GREEN}✓ Đã lưu vào: {output_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Lỗi khi lưu file: {e}{Style.RESET_ALL}")
        return
    
    try:
        print(f"\n{Fore.YELLOW}Đang xóa data đã xử lý khỏi {input_file}...{Style.RESET_ALL}")
        empty_df = pd.DataFrame(columns=['text', 'label'])
        empty_df.to_csv(input_file, index=False, encoding='utf-8-sig')
        print(f"{Fore.GREEN}✓ Đã xóa {len(df_new)} dòng đã xử lý khỏi {input_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Lỗi khi xóa data: {e}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}=== MẪU DỮ LIỆU VỪA GÁN NHÃN ==={Style.RESET_ALL}")
    for label in [0, 1, 2]:
        samples = df_new[df_new['label'] == label].head(2)
        if len(samples) > 0:
            label_name = ['NEGATIVE', 'NEUTRAL', 'POSITIVE'][label]
            label_color = [Fore.RED, Fore.YELLOW, Fore.GREEN][label]
            print(f"\n{label_color}[{label_name}]{Style.RESET_ALL}")
            for idx, row in samples.iterrows():
                text_preview = row['text'][:100] + '...' if len(row['text']) > 100 else row['text']
                print(f"  • {text_preview}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'labeled_data_bert.csv'
    else:
        input_file = 'crawled_fb.csv'
        output_file = 'labeled_data_bert.csv'
    
    auto_label_with_bert(input_file, output_file)
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Xong! Bạn có thể dùng file '{output_file}' để train model.{Style.RESET_ALL}")
