# snowflake/ingestion/embedding_generator.py
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from typing import List, Dict
import json

class EmbeddingGenerator:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model_name = model_name
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
    
    def create_text_embedding(self, text: str) -> List[float]:
        """Generate embedding for text description"""
        inputs = self.tokenizer(text, return_tensors="pt", 
                              padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
            return embeddings.cpu().numpy().flatten().tolist()
    
    def create_svg_embedding(self, svg_data: Dict) -> List[float]:
        """Generate embedding for SVG based on metadata and content"""
        # Combine text features
        text_features = [
            svg_data.get('title', ''),
            svg_data.get('description', ''),
            ' '.join(svg_data.get('tags', [])),
            json.dumps(svg_data.get('metadata', {}))
        ]
        
        combined_text = ' '.join(filter(None, text_features))
        return self.create_text_embedding(combined_text)
    
    def find_similar_assets(self, query_embedding: List[float], 
                          asset_embeddings: List[Dict], 
                          top_k: int = 10) -> List[Dict]:
        """Find similar assets using cosine similarity"""
        query_vec = np.array(query_embedding)
        similarities = []
        
        for asset in asset_embeddings:
            asset_vec = np.array(asset['embedding'])
            similarity = np.dot(query_vec, asset_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(asset_vec)
            )
            similarities.append({
                'asset_id': asset['asset_id'],
                'similarity': similarity
            })
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]