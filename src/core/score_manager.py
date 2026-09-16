import json
import os

class ScoreManager:
    def __init__(self, file_path="data/scores.json"):
        self.file_path = file_path

    def load_scores(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar pontuações: {e}")
        return []

    def save_score(self, player_name, score):
        scores = self.load_scores()
        name = player_name.strip() if player_name.strip() else "Jogador"
        
        scores.append({"name": name, "score": score})
        scores.sort(key=lambda x: x["score"], reverse=True)
        scores = scores[:10]
        
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(scores, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar pontuação: {e}")