import joblib
from preprocess import clean_text
from colorama import init, Fore, Style

init()

def predict_sentiment(text, verbose=True):
    model = joblib.load('sentiment_model.pkl')
    tfidf = joblib.load('tfidf_vectorizer.pkl')
    
    cleaned_text = clean_text(text)
    if verbose:
        print(f"Text gốc: {text}")
        print(f"Text đã xử lý: {cleaned_text}")
    
    vectorized_text = tfidf.transform([cleaned_text])
    
    prediction = model.predict(vectorized_text)[0]
    proba = model.predict_proba(vectorized_text)[0]
    
    label_map = {0: "Tiêu cực", 1: "Khác", 2: "Tích cực"}
    label_color = {0: Fore.RED, 1: Fore.YELLOW, 2: Fore.GREEN}
    
    result = label_map.get(prediction, "Không xác định")
    color = label_color.get(prediction, Fore.WHITE)
    
    if verbose:
        print(f"\n{color}Dự đoán: {result}{Style.RESET_ALL}")
        print(f"Độ tin cậy:")
        print(f"  • Tiêu cực: {proba[0]*100:.1f}%")
        print(f"  • Trung lập: {proba[1]*100:.1f}%")
        print(f"  • Tích cực: {proba[2]*100:.1f}%")
    
    return result, prediction, proba

if __name__ == "__main__":
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║       DỰ ĐOÁN SENTIMENT TIẾNG VIỆT          ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    test_samples = [
        "Quán này ngon lắm, rất đáng thử!",
        "Dở tệ, không bao giờ quay lại",
        "Bình thường thôi, tạm được"
    ]
    
    print(f"{Fore.CYAN}=== TEST VỚI MẪU ==={Style.RESET_ALL}\n")
    for sample in test_samples:
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        predict_sentiment(sample)
        print()
    
    print(f"\n{Fore.CYAN}=== CHẾ ĐỘ TƯƠNG TÁC ==={Style.RESET_ALL}")
    print("Nhập 'q' để thoát\n")
    
    while True:
        text = input(f"{Fore.YELLOW}Nhập câu cần kiểm tra: {Style.RESET_ALL}")
        if text.lower() == 'q':
            print(f"\n{Fore.GREEN}Tạm biệt!{Style.RESET_ALL}")
            break
        if text.strip():
            predict_sentiment(text)
            print()
