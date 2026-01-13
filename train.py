import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import joblib
from preprocess import clean_text
from colorama import init, Fore, Style

init()

def train_model(data_path):
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║           TRAIN SENTIMENT MODEL              ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚═══════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    # 1. Load data
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} samples.")
    
    # Thống kê phân bố nhãn
    print(f"\n{Fore.CYAN}Phân bố nhãn:{Style.RESET_ALL}")
    label_counts = df['label'].value_counts().sort_index()
    for label, count in label_counts.items():
        label_name = ['Tiêu cực', 'Khác', 'Tích cực'][label]
        print(f"  {label} ({label_name}): {count} ({count/len(df)*100:.1f}%)")
    
    # 2. Preprocess
    print(f"\n{Fore.YELLOW}Preprocessing text...{Style.RESET_ALL}")
    df['clean_text'] = df['text'].apply(clean_text)
    
    # 3. Split data
    X = df['clean_text']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 4. Vectorization (TF-IDF)
    print(f"{Fore.YELLOW}Vectorizing...{Style.RESET_ALL}")
    tfidf = TfidfVectorizer(
        ngram_range=(1, 3),  # Tăng lên 3-gram để bắt pattern tốt hơn
        max_features=10000,   # Tăng features
        min_df=2,             # Bỏ từ xuất hiện quá ít
        max_df=0.8            # Bỏ từ xuất hiện quá nhiều
    )
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)
    
    # 5. Tính class weights để cân bằng
    class_weights = compute_class_weight(
        'balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weight_dict = {i: w for i, w in enumerate(class_weights)}
    
    print(f"\n{Fore.CYAN}Class weights (để cân bằng):{Style.RESET_ALL}")
    for label, weight in class_weight_dict.items():
        label_name = ['Tiêu cực', 'Khác', 'Tích cực'][label]
        print(f"  {label} ({label_name}): {weight:.2f}")
    
    # 6. Train Model với class_weight
    print(f"\n{Fore.YELLOW}Training model...{Style.RESET_ALL}")
    model = LogisticRegression(
        max_iter=2000,
        class_weight=class_weight_dict,  # Cân bằng classes
        C=1.0,                            # Regularization
        solver='lbfgs',
        random_state=42
    )
    model.fit(X_train_tfidf, y_train)
    
    # 7. Evaluate
    y_pred = model.predict(X_test_tfidf)
    
    print(f"\n{Fore.GREEN}=== KẾT QUẢ ĐÁNH GIÁ ==={Style.RESET_ALL}")
    print("\nClassification Report:")
    target_names = ['Tiêu cực (0)', 'Khác (1)', 'Tích cực (2)']
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    print(f"\n{Fore.GREEN}Accuracy: {accuracy_score(y_test, y_pred):.4f}{Style.RESET_ALL}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n{Fore.CYAN}Confusion Matrix:{Style.RESET_ALL}")
    print("              Predicted")
    print("              Tiêu cực  Khác  Tích cực")
    for i, row in enumerate(cm):
        label_name = ['Tiêu cực', 'Khác    ', 'Tích cực'][i]
        print(f"Actual {label_name}  {row[0]:6d}  {row[1]:4d}  {row[2]:6d}")
    
    # 8. Save model and vectorizer
    joblib.dump(model, 'sentiment_model.pkl')
    joblib.dump(tfidf, 'tfidf_vectorizer.pkl')
    print(f"\n{Fore.GREEN}✓ Model saved to sentiment_model.pkl{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Vectorizer saved to tfidf_vectorizer.pkl{Style.RESET_ALL}")
    
    # 9. Test với vài mẫu
    print(f"\n{Fore.CYAN}=== TEST VỚI MẪU ==={Style.RESET_ALL}")
    test_samples = [
        "Quán này ngon lắm, rất đáng thử!",
        "Dở tệ, không bao giờ quay lại",
        "Bình thường thôi",
        "Ngon",
        "Chán"
    ]
    
    for sample in test_samples:
        cleaned = clean_text(sample)
        vec = tfidf.transform([cleaned])
        pred = model.predict(vec)[0]
        proba = model.predict_proba(vec)[0]
        
        label_name = ['Tiêu cực', 'Khác', 'Tích cực'][pred]
        color = [Fore.RED, Fore.YELLOW, Fore.GREEN][pred]
        
        print(f"\n'{sample}'")
        print(f"  → {color}{label_name}{Style.RESET_ALL} (Tiêu cực: {proba[0]:.2f}, Khác: {proba[1]:.2f}, Tích cực: {proba[2]:.2f})")

if __name__ == "__main__":
    train_model('labeled_data_bert.csv')
