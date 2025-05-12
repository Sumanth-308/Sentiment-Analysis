import tkinter as tk
from tkinter import messagebox, font
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import wordnet

# Ensure required NLTK resources are downloaded
nltk.download('vader_lexicon')
nltk.download('wordnet')

class SentimentApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sentiment Analysis")
        self.geometry("600x700")
        self.configure(bg="#e8f0f2")  # Soft blue background

        # Set custom fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Arial", size=14)
        self.button_font = font.Font(family="Arial", size=12)

        # Frame for input and output
        self.frame = tk.Frame(self, bg="#ffffff", bd=10, relief=tk.RAISED)
        self.frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.frame, text="Enter text:", font=self.label_font, bg="#ffffff")
        self.label.pack(pady=10)

        self.text_entry = tk.Text(self.frame, height=10, width=60, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        self.text_entry.pack(pady=10)

        # Analyze Button
        self.analyze_button = tk.Button(self.frame, text="Analyze Sentiment", command=self.analyze_sentiment, 
                                         bg="#4CAF50", fg="white", font=self.button_font, padx=10, pady=5)
        self.analyze_button.pack(pady=10)

        # Improve Sentence Button
        self.improve_button = tk.Button(self.frame, text="Improve Sentence", command=self.improve_sentence,
                                         bg="#2196F3", fg="white", font=self.button_font, padx=10, pady=5)
        self.improve_button.pack(pady=10)

        self.result_label = tk.Label(self.frame, text="", font=("Arial", 14), bg="#ffffff")
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(self.frame, text="", font=("Arial", 10), bg="#ffffff")
        self.score_label.pack(pady=10)

        self.improved_label = tk.Label(self.frame, text="", font=("Arial", 14), bg="#ffffff", fg="green")
        self.improved_label.pack(pady=10)

        self.sia = SentimentIntensityAnalyzer()

        # External word suggestions for improvement
        self.external_replacements = {
            "bad": "suboptimal",
            "good": "excellent",
            "happy": "joyful",
            "sad": "melancholic",
            "angry": "frustrated",
            "hate": "strongly dislike",
            "love": "deeply appreciate",
            "okay": "satisfactory",
            "problem": "challenge",
            "difficult": "complex"
        }

    def analyze_sentiment(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            sentiment = self.sia.polarity_scores(text)
            result = "Neutral"
            if sentiment['compound'] >= 0.05:
                result = "Positive"
            elif sentiment['compound'] <= -0.05:
                result = "Negative"

            # Display the overall sentiment
            self.result_label.config(text=f"Sentiment: {result}")

            # Display the sentiment scores
            score_text = (f"Scores:\n"
                          f"Positive: {sentiment['pos']:.2f}\n"
                          f"Neutral: {sentiment['neu']:.2f}\n"
                          f"Negative: {sentiment['neg']:.2f}\n"
                          f"Compound: {sentiment['compound']:.2f}")
            self.score_label.config(text=score_text)
        else:
            messagebox.showwarning("Input Error", "Please enter some text")

    def improve_sentence(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            improved_text = self.rephrase_sentence(text)
            self.improved_label.config(text=f"Improved Sentence: {improved_text}")
        else:
            messagebox.showwarning("Input Error", "Please enter some text")

    def rephrase_sentence(self, text):
        words = text.split()
        improved_words = []

        for word in words:
            # Check if the word is in external replacements
            if word.lower() in self.external_replacements:
                improved_words.append(self.external_replacements[word.lower()])
            else:
                # Try to get a synonym using WordNet
                synonyms = wordnet.synsets(word)
                if synonyms:
                    improved_word = synonyms[0].lemmas()[0].name()
                    improved_words.append(improved_word)
                else:
                    improved_words.append(word)

        # Join the improved words into a sentence
        improved_sentence = ' '.join(improved_words)

        # Capitalize the first letter of the resulting sentence
        improved_sentence = improved_sentence.capitalize()

        return improved_sentence

if __name__ == "__main__":
    app = SentimentApp()
    app.mainloop()
