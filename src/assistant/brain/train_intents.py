from pathlib import Path
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


def main():
    # path do dataset
    BASE_DIR = Path(__file__).resolve().parents[1]
    DATASET_PATH = BASE_DIR / "datasets" / "intents.json"

    # carregar dataset
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        DATASET = json.load(f)

    # montar dataset
    texts = []
    labels = []

    for intent, examples in DATASET.items():
        for ex in examples:
            texts.append(ex)
            labels.append(intent)

    # treino
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        lowercase=True
    )

    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=200)
    model.fit(X, labels)

    # salvar modelo
    MODEL_DIR = BASE_DIR / "brain"

    with open(MODEL_DIR / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    with open(MODEL_DIR / "intent_model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Modelo treinado com sucesso")


if __name__ == "__main__":
    main()
