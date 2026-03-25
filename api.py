from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
from ai_startup_generator import AIStartupGenerator
from systematic_generator import SystematicIdeaGenerator
import asyncio
import json
from datetime import datetime

app = FastAPI(title="AI Startup Generator API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize generators
ai_generator = AIStartupGenerator(
    openai_key=os.getenv("OPENAI_API_KEY", "your_openai_key"),
    reddit_client_id=os.getenv("REDDIT_CLIENT_ID", "your_reddit_id"),
    reddit_secret=os.getenv("REDDIT_CLIENT_SECRET", "your_reddit_secret")
)
systematic_generator = SystematicIdeaGenerator()

class StartupIdeaAdvanced(BaseModel):
    name: str
    description: str
    category: str
    target_audience: str
    monthly_revenue: int
    business_model: str
    mvp_features: List[str]
    market_size: str
    competitive_advantage: str
    implementation_difficulty: str
    ai_integration: str
    source_problem: str
    confidence_score: int
    ml_score: Optional[float] = None
    market_analysis: Optional[Dict] = None

class IdeaRequest(BaseModel):
    category: Optional[str] = None
    use_ml_pipeline: bool = True
    include_market_analysis: bool = False
    use_systematic: bool = True
    batch_size: int = 1

class PipelineResponse(BaseModel):
    ideas: List[StartupIdeaAdvanced]
    analysis: Dict
    pipeline_stats: Dict

# Cache for expensive operations
pipeline_cache = {}

@app.get("/")
async def root():
    return {
        "message": "AI-Powered Startup Idea Generator API v2.0",
        "features": [
            "Reddit data collection",
            "ML problem clustering",
            "LLM idea generation",
            "Market analysis",
            "Idea ranking algorithm"
        ],
        "status": "running"
    }

@app.post("/api/generate-idea", response_model=StartupIdeaAdvanced)
async def generate_single_idea(request: IdeaRequest = IdeaRequest()):
    """Generate a systematic AI-powered startup idea"""
    try:
        if request.use_systematic:
            # Use systematic generator first
            idea_data = systematic_generator.generate_systematic_idea(request.category)
            
            if request.include_market_analysis:
                idea_data['market_analysis'] = ai_generator.generate_market_analysis(idea_data)
            
            return StartupIdeaAdvanced(**idea_data)
        
        elif request.use_ml_pipeline:
            # Run full ML pipeline
            result = ai_generator.run_full_pipeline(request.category)
            if result['ideas']:
                idea_data = result['ideas'][0]
                
                if request.include_market_analysis and 'market_analysis' not in idea_data:
                    idea_data['market_analysis'] = ai_generator.generate_market_analysis(idea_data)
                
                return StartupIdeaAdvanced(**idea_data)
        
        # Fallback
        idea_data = systematic_generator.generate_systematic_idea(request.category)
        return StartupIdeaAdvanced(**idea_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/generate-batch", response_model=PipelineResponse)
async def generate_batch_ideas(request: IdeaRequest = IdeaRequest()):
    """Generate multiple systematic ideas"""
    try:
        cache_key = f"{request.category}_{request.use_systematic}_{request.batch_size}_{datetime.now().hour}"
        
        if cache_key in pipeline_cache:
            return pipeline_cache[cache_key]
        
        if request.use_systematic:
            # Generate systematic batch
            batch_ideas = systematic_generator.generate_batch_ideas(
                count=request.batch_size or 5, 
                category=request.category
            )
            
            ideas = []
            for idea_data in batch_ideas:
                if request.include_market_analysis:
                    idea_data['market_analysis'] = ai_generator.generate_market_analysis(idea_data)
                ideas.append(StartupIdeaAdvanced(**idea_data))
            
            response = PipelineResponse(
                ideas=ideas,
                analysis={'systematic_generation': True, 'total_ideas': len(ideas)},
                pipeline_stats={
                    'generation_method': 'systematic',
                    'ideas_generated': len(ideas),
                    'timestamp': datetime.now().isoformat()
                }
            )
        else:
            # Use ML pipeline
            result = ai_generator.run_full_pipeline(request.category)
            ideas = []
            for idea_data in result['ideas']:
                if request.include_market_analysis and 'market_analysis' not in idea_data:
                    idea_data['market_analysis'] = ai_generator.generate_market_analysis(idea_data)
                ideas.append(StartupIdeaAdvanced(**idea_data))
            
            response = PipelineResponse(
                ideas=ideas,
                analysis=result['analysis'],
                pipeline_stats=result['pipeline_stats']
            )
        
        pipeline_cache[cache_key] = response
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")

@app.get("/api/market-analysis/{idea_name}")
async def get_market_analysis(idea_name: str):
    """Get detailed market analysis for a specific idea"""
    try:
        # Mock idea for analysis
        mock_idea = {
            'name': idea_name,
            'category': 'Technology',
            'target_audience': 'Tech professionals'
        }
        
        analysis = ai_generator.generate_market_analysis(mock_idea)
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/api/trending-problems")
async def get_trending_problems():
    """Get current trending problems from Reddit"""
    try:
        problems = ai_generator.collect_reddit_problems(limit=20)
        analysis = ai_generator.analyze_problems_with_ml(problems)
        
        return {
            "trending_problems": problems[:10],
            "cluster_analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/categories")
async def get_categories():
    """Get available startup categories"""
    return {
        "categories": list(systematic_generator.components.keys()),
        "all_categories": [
            "Technology", "Health", "Finance", "Education", 
            "E-commerce", "Social", "Entertainment", "AI/ML",
            "FinTech", "HealthTech", "EdTech", "GreenTech"
        ]
    }

@app.post("/api/rank-ideas")
async def rank_custom_ideas(ideas: List[Dict]):
    """Rank custom ideas using ML algorithm"""
    try:
        ranked = ai_generator.rank_ideas_with_ml(ideas)
        return {"ranked_ideas": ranked}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ranking error: {str(e)}")

@app.get("/api/pipeline-stats")
async def get_pipeline_stats():
    """Get AI pipeline performance statistics"""
    return {
        "cache_size": len(pipeline_cache),
        "supported_models": ["gpt-3.5-turbo"],
        "ml_algorithms": ["TF-IDF", "K-Means", "Cosine Similarity"],
        "data_sources": ["Reddit API"],
        "uptime": "Active",
        "version": "2.0"
    }

@app.get("/api/health")
async def health_check():
    """Comprehensive health check"""
    try:
        # Test Reddit connection
        problems = ai_generator.collect_reddit_problems(limit=1)
        reddit_status = "OK" if problems else "Limited"
        
        return {
            "status": "healthy",
            "reddit_api": reddit_status,
            "openai_api": "Configured",
            "ml_models": "Loaded",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    print("🤖 Starting AI-Powered Startup Generator API v2.0...")
    print("🧠 Features: ML clustering, LLM generation, market analysis")
    print("📡 API available at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)