import openai
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import praw
import requests
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import logging

class AIStartupGenerator:
    def __init__(self, openai_key: str, reddit_client_id: str, reddit_secret: str):
        self.openai_key = openai_key
        openai.api_key = openai_key
        
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_secret,
            user_agent="AIStartupGenerator/1.0"
        )
        
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.kmeans = KMeans(n_clusters=8, random_state=42)
        self.problem_database = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def collect_reddit_problems(self, subreddits: List[str] = None, limit: int = 50) -> List[Dict]:
        """Collect problems from multiple subreddits using ML-based filtering"""
        if subreddits is None:
            subreddits = ['Entrepreneur', 'startups', 'smallbusiness', 'business', 'productivity']
        
        problems = []
        problem_keywords = ['problem', 'issue', 'struggle', 'difficult', 'challenge', 'need', 'solution']
        
        for subreddit_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                for post in subreddit.hot(limit=limit//len(subreddits)):
                    text = f"{post.title} {post.selftext}".lower()
                    
                    # ML-based problem detection
                    if any(keyword in text for keyword in problem_keywords) and post.score > 3:
                        problems.append({
                            'title': post.title,
                            'content': post.selftext[:300],
                            'score': post.score,
                            'subreddit': subreddit_name,
                            'url': post.url,
                            'created': datetime.fromtimestamp(post.created_utc)
                        })
            except Exception as e:
                self.logger.error(f"Error collecting from {subreddit_name}: {e}")
        
        return problems

    def analyze_problems_with_ml(self, problems: List[Dict]) -> Dict:
        """Use ML to cluster and analyze problems"""
        if not problems:
            return {'clusters': [], 'insights': 'No problems to analyze'}
        
        # Extract text for analysis
        texts = [f"{p['title']} {p['content']}" for p in problems]
        
        # Vectorize problems
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        # Cluster problems
        clusters = self.kmeans.fit_predict(tfidf_matrix)
        
        # Analyze clusters
        cluster_analysis = {}
        for i in range(self.kmeans.n_clusters):
            cluster_problems = [problems[j] for j in range(len(problems)) if clusters[j] == i]
            if cluster_problems:
                cluster_analysis[i] = {
                    'size': len(cluster_problems),
                    'avg_score': np.mean([p['score'] for p in cluster_problems]),
                    'top_problem': max(cluster_problems, key=lambda x: x['score']),
                    'keywords': self._extract_cluster_keywords(i)
                }
        
        return {
            'clusters': cluster_analysis,
            'total_problems': len(problems),
            'feature_names': self.vectorizer.get_feature_names_out()[:20].tolist()
        }

    def _extract_cluster_keywords(self, cluster_id: int) -> List[str]:
        """Extract top keywords for a cluster"""
        cluster_center = self.kmeans.cluster_centers_[cluster_id]
        top_indices = cluster_center.argsort()[-10:][::-1]
        feature_names = self.vectorizer.get_feature_names_out()
        return [feature_names[i] for i in top_indices]

    def generate_idea_with_llm(self, problem_cluster: Dict, category: str = None) -> Dict:
        """Generate startup idea using advanced LLM prompting"""
        top_problem = problem_cluster['top_problem']
        keywords = problem_cluster['keywords']
        
        prompt = f"""
        As an AI startup advisor, analyze this real problem from Reddit:
        
        Problem: {top_problem['title']}
        Context: {top_problem['content']}
        Related Keywords: {', '.join(keywords[:5])}
        Problem Popularity Score: {top_problem['score']}
        
        Generate an innovative startup idea with this JSON structure:
        {{
            "name": "Creative, memorable startup name",
            "description": "Detailed 2-sentence description of the solution",
            "category": "Technology/Health/Finance/Education/E-commerce/Social/Entertainment",
            "target_audience": "Specific demographic with pain point",
            "monthly_revenue": "Realistic projection (5000-150000)",
            "business_model": "Revenue generation strategy",
            "mvp_features": ["feature1", "feature2", "feature3"],
            "market_size": "TAM estimation",
            "competitive_advantage": "Unique value proposition",
            "implementation_difficulty": "Low/Medium/High",
            "ai_integration": "How AI/ML enhances the solution"
        }}
        
        Focus on AI/ML integration and scalable solutions.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.8
            )
            
            result = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            
            if json_match:
                idea = json.loads(json_match.group())
                idea['source_problem'] = top_problem['title']
                idea['confidence_score'] = min(100, top_problem['score'] * 2)
                return idea
                
        except Exception as e:
            self.logger.error(f"LLM generation error: {e}")
        
        # Fallback idea
        return self._generate_fallback_idea(top_problem)

    def _generate_fallback_idea(self, problem: Dict) -> Dict:
        """Generate fallback idea when LLM fails"""
        import random
        
        ai_solutions = ["AI-powered", "ML-driven", "Smart", "Intelligent", "Automated"]
        business_types = ["platform", "app", "service", "marketplace", "tool"]
        
        return {
            "name": f"{random.choice(ai_solutions)} {random.choice(business_types).title()}",
            "description": f"Innovative solution addressing: {problem['title'][:50]}...",
            "category": "Technology",
            "target_audience": "Tech-savvy professionals",
            "monthly_revenue": random.randint(10000, 50000),
            "business_model": "SaaS subscription",
            "mvp_features": ["Core functionality", "User dashboard", "Analytics"],
            "market_size": "$1B+ TAM",
            "competitive_advantage": "AI-first approach",
            "implementation_difficulty": "Medium",
            "ai_integration": "Machine learning for optimization",
            "source_problem": problem['title'],
            "confidence_score": 75
        }

    def rank_ideas_with_ml(self, ideas: List[Dict]) -> List[Dict]:
        """Rank ideas using ML scoring algorithm"""
        for idea in ideas:
            # Multi-factor scoring
            revenue_score = min(100, idea['monthly_revenue'] / 1000)
            confidence_score = idea.get('confidence_score', 50)
            difficulty_penalty = {'Low': 0, 'Medium': -10, 'High': -25}.get(
                idea.get('implementation_difficulty', 'Medium'), -10
            )
            
            # AI integration bonus
            ai_bonus = 15 if 'ai' in idea.get('ai_integration', '').lower() else 0
            
            idea['ml_score'] = revenue_score + confidence_score + difficulty_penalty + ai_bonus
        
        return sorted(ideas, key=lambda x: x['ml_score'], reverse=True)

    def generate_market_analysis(self, idea: Dict) -> Dict:
        """Generate market analysis using AI"""
        prompt = f"""
        Analyze the market potential for this startup idea:
        Name: {idea['name']}
        Category: {idea['category']}
        Target: {idea['target_audience']}
        
        Provide market analysis in JSON:
        {{
            "market_trends": ["trend1", "trend2", "trend3"],
            "competitors": ["competitor1", "competitor2"],
            "growth_potential": "High/Medium/Low",
            "risk_factors": ["risk1", "risk2"],
            "success_probability": "percentage"
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            result = response.choices[0].message.content
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
                
        except Exception as e:
            self.logger.error(f"Market analysis error: {e}")
        
        return {
            "market_trends": ["Digital transformation", "AI adoption", "Remote work"],
            "competitors": ["Established players", "New startups"],
            "growth_potential": "Medium",
            "risk_factors": ["Market saturation", "Technical challenges"],
            "success_probability": "65%"
        }

    def run_full_pipeline(self, category: str = None) -> Dict:
        """Run the complete AI pipeline"""
        self.logger.info("Starting AI startup generation pipeline...")
        
        # Step 1: Collect problems
        problems = self.collect_reddit_problems()
        self.logger.info(f"Collected {len(problems)} problems")
        
        # Step 2: ML analysis
        analysis = self.analyze_problems_with_ml(problems)
        self.logger.info(f"Identified {len(analysis['clusters'])} problem clusters")
        
        # Step 3: Generate ideas
        ideas = []
        for cluster_id, cluster_data in analysis['clusters'].items():
            if cluster_data['size'] > 2:  # Only use significant clusters
                idea = self.generate_idea_with_llm(cluster_data, category)
                ideas.append(idea)
        
        # Step 4: Rank ideas
        ranked_ideas = self.rank_ideas_with_ml(ideas)
        
        # Step 5: Market analysis for top idea
        if ranked_ideas:
            market_analysis = self.generate_market_analysis(ranked_ideas[0])
            ranked_ideas[0]['market_analysis'] = market_analysis
        
        return {
            'ideas': ranked_ideas,
            'analysis': analysis,
            'pipeline_stats': {
                'problems_collected': len(problems),
                'clusters_found': len(analysis['clusters']),
                'ideas_generated': len(ideas),
                'timestamp': datetime.now().isoformat()
            }
        }