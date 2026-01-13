import re
import string
import unicodedata
from underthesea import word_tokenize

normalization_dict = {
    "ko": "không", "k": "không", "khum": "không", "n": "không",
    "m": "mình", "dc": "được", "đc": "được", "ok": "tốt", "oke": "tốt",
    "v": "vậy", "r": "rồi", "fb": "facebook", "cmt": "bình luận",
    "stt": "trạng thái", "rùi": "rồi", "ùi": "rồi",
    "vcl": "rất", "vl": "rất", "tks": "cảm ơn", "rep": "trả lời",
    "h": "giờ", "sp": "sản phẩm", "bn": "bao nhiêu",
}

def clean_text(text):
    if not isinstance(text, str): return ""
    text = unicodedata.normalize('NFC', text.lower())
    text = re.sub(r'https?://\S+|www\.\S+ search', '', text)
    words = text.split()
    text = " ".join([normalization_dict.get(w, w) for w in words])
    text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ]', ' ', text)
    text = word_tokenize(text, format="text")
    return text.strip()

if __name__ == "__main__":
    sample_texts = [
        "Phim này coi chán ghê :(",
        "Sản phẩm dùng ok lắm, rất đáng tiền",
        "Ủa shop này còn bán không? khum thấy rep",
        "Ship nhanh vcl, tks shop"
    ]
    
    for t in sample_texts:
        print(f"Original: {t}")
        print(f"Cleaned:  {clean_text(t)}")
        print("-" * 20)
