def translate_emoji(text):
    emoji_map = {
        "😀": "Happy",
        "😢": "Sad",
        "🔥": "Cool",
        "🚀": "Fast",
        "🐍": "Python",
        "💻": "Code"
    }
    
    words = text.split()
    translated = []
    
    for word in words:
        translated.append(emoji_map.get(word, word))
        
    return " ".join(translated)

def analyze_sentiment(text):
    positives = ["😀", "🔥", "🚀"]
    negatives = ["😢", "😡", "👎"]
    
    pos_count = sum(text.count(e) for e in positives)
    neg_count = sum(text.count(e) for e in negatives)
    
    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    return "Neutral"

def main():
    user_input = input("Enter a message with emojis: ")
    
    translation = translate_emoji(user_input)
    sentiment = analyze_sentiment(user_input)
    
    print("-" * 20)
    print(f"Original: {user_input}")
    print(f"Translation: {translation}")
    print(f"Sentiment: {sentiment}")

if __name__ == "__main__":
    main()