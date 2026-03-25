let counter = 0;
let allIdeas = [];
let usedIdeas = new Set();
let favoriteIdeas = new Set();
let isDarkTheme = false;

const categories = [
    'Accounting', 'Acting', 'Advertising', 'AI', 'Art', 'Books', 'Cars', 'Cooking', 
    'Crypto', 'Customer Service', 'Data Analysis', 'E-commerce', 'Education', 'Fashion', 
    'Finance', 'Fitness', 'Food', 'Gaming', 'Health', 'Marketing', 'Music', 'Photography', 
    'Real Estate', 'Social Media', 'Sports', 'Technology', 'Travel', 'Video'
];

const ideaTemplates = {
    'Accounting': [
        {name: "Expense Tracker", description: "Automated expense tracking with AI categorization", targetAudience: "Small business owners", monthlyRevenue: 25000},
        {name: "Tax Assistant", description: "AI-powered tax preparation and filing system", targetAudience: "Freelancers and contractors", monthlyRevenue: 18000}
    ],
    'Acting': [
        {name: "Audition Coach", description: "Virtual acting coach with personalized feedback", targetAudience: "Aspiring actors", monthlyRevenue: 12000},
        {name: "Script Analyzer", description: "AI tool for script analysis and character development", targetAudience: "Theater professionals", monthlyRevenue: 15000}
    ],
    'Advertising': [
        {name: "Ad Optimizer", description: "AI-powered advertising campaign optimization platform", targetAudience: "Marketing agencies", monthlyRevenue: 35000},
        {name: "Creative Generator", description: "Automated ad creative generation using machine learning", targetAudience: "Digital marketers", monthlyRevenue: 28000}
    ],
    'AI': [
        {name: "Model Trainer", description: "No-code AI model training platform for businesses", targetAudience: "Non-technical business users", monthlyRevenue: 45000},
        {name: "Data Labeler", description: "Crowdsourced data labeling platform with quality control", targetAudience: "AI companies", monthlyRevenue: 32000}
    ],
    'Art': [
        {name: "NFT Marketplace", description: "Curated digital art marketplace with blockchain verification", targetAudience: "Digital artists and collectors", monthlyRevenue: 40000},
        {name: "Art Generator", description: "AI-powered art creation tool for designers", targetAudience: "Graphic designers", monthlyRevenue: 22000}
    ],
    'Books': [
        {name: "Reading Companion", description: "AI-powered reading recommendations and discussion platform", targetAudience: "Book enthusiasts", monthlyRevenue: 16000},
        {name: "Author Assistant", description: "Writing and editing assistant for aspiring authors", targetAudience: "Writers and authors", monthlyRevenue: 20000}
    ],
    'Cars': [
        {name: "Maintenance Tracker", description: "Smart car maintenance scheduling and reminder system", targetAudience: "Car owners", monthlyRevenue: 18000},
        {name: "Fleet Manager", description: "AI-powered fleet management and optimization platform", targetAudience: "Fleet operators", monthlyRevenue: 55000}
    ],
    'Cooking': [
        {name: "Recipe Assistant", description: "Smart cooking companion with ingredient-based suggestions", targetAudience: "Home cooks", monthlyRevenue: 15000},
        {name: "Meal Planner", description: "Personalized meal planning with nutritional analysis", targetAudience: "Health-conscious individuals", monthlyRevenue: 12000}
    ],
    'Crypto': [
        {name: "Portfolio Tracker", description: "Advanced cryptocurrency investment tracking platform", targetAudience: "Crypto investors", monthlyRevenue: 25000},
        {name: "DeFi Analyzer", description: "Risk analysis tool for decentralized finance protocols", targetAudience: "DeFi users", monthlyRevenue: 30000}
    ],
    'Technology': [
        {name: "Code Reviewer", description: "AI-powered code review and quality analysis tool", targetAudience: "Software developers", monthlyRevenue: 38000},
        {name: "API Manager", description: "Comprehensive API management and monitoring platform", targetAudience: "Tech companies", monthlyRevenue: 42000}
    ],
    'Health': [
        {name: "Symptom Checker", description: "AI-powered symptom analysis and health recommendations", targetAudience: "Health-conscious consumers", monthlyRevenue: 28000},
        {name: "Fitness Tracker", description: "Personalized fitness coaching with wearable integration", targetAudience: "Fitness enthusiasts", monthlyRevenue: 22000}
    ],
    'Finance': [
        {name: "Budget Planner", description: "Intelligent budgeting and financial planning assistant", targetAudience: "Young professionals", monthlyRevenue: 20000},
        {name: "Investment Advisor", description: "Robo-advisor for automated investment management", targetAudience: "Retail investors", monthlyRevenue: 35000}
    ],
    'Education': [
        {name: "Learning Platform", description: "Adaptive learning system with personalized curricula", targetAudience: "Students and educators", monthlyRevenue: 30000},
        {name: "Skill Assessor", description: "AI-powered skill assessment and certification platform", targetAudience: "Job seekers", monthlyRevenue: 25000}
    ]
};

function initializeApp() {
    populateCategories();
    setupEventListeners();
}

function populateCategories() {
    const categorySelect = document.getElementById('categorySelect');
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.toLowerCase();
        option.textContent = category;
        categorySelect.appendChild(option);
    });
}

function setupEventListeners() {
    document.getElementById('generateBtn').addEventListener('click', generateIdea);
    document.getElementById('searchInput').addEventListener('input', filterIdeas);
    document.getElementById('categorySelect').addEventListener('change', filterIdeas);
    document.getElementById('minRevenue').addEventListener('input', filterIdeas);
    document.getElementById('maxRevenue').addEventListener('input', filterIdeas);
    document.getElementById('sortOrder').addEventListener('change', filterIdeas);
    document.getElementById('exportBtn').addEventListener('click', exportIdeas);
    document.getElementById('clearBtn').addEventListener('click', clearAllIdeas);
    document.getElementById('themeBtn').addEventListener('click', toggleTheme);
    document.getElementById('favoriteBtn').addEventListener('click', showFavorites);
}

function generateRandomIdea() {
    const selectedCategory = document.getElementById('categorySelect').value;
    let availableCategories = Object.keys(ideaTemplates);
    
    if (selectedCategory) {
        const categoryName = categories.find(cat => cat.toLowerCase() === selectedCategory);
        if (categoryName && ideaTemplates[categoryName]) {
            availableCategories = [categoryName];
        }
    }
    
    let attempts = 0;
    let newIdea;
    
    do {
        const randomCategory = availableCategories[Math.floor(Math.random() * availableCategories.length)];
        const categoryTemplates = ideaTemplates[randomCategory];
        const template = categoryTemplates[Math.floor(Math.random() * categoryTemplates.length)];
        
        const variations = [
            "Smart", "AI-Powered", "Automated", "Digital", "Virtual", "Mobile", "Cloud-Based", "Next-Gen"
        ];
        
        const variation = variations[Math.floor(Math.random() * variations.length)];
        const ideaKey = `${variation}-${template.name}-${randomCategory}`;
        
        if (!usedIdeas.has(ideaKey)) {
            usedIdeas.add(ideaKey);
            newIdea = {
                name: `${variation} ${template.name}`,
                description: template.description,
                category: randomCategory,
                targetAudience: template.targetAudience,
                monthlyRevenue: template.monthlyRevenue + Math.floor(Math.random() * 20000) - 10000
            };
            break;
        }
        attempts++;
    } while (attempts < 50);
    
    return newIdea;
}

async function generateIdea() {
    const generateBtn = document.getElementById('generateBtn');
    generateBtn.disabled = true;
    generateBtn.textContent = '🤖 Generating 3 Ideas...';
    
    for (let i = 0; i < 3; i++) {
        try {
            const response = await fetch('http://localhost:8000/api/generate-idea', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    use_ml_pipeline: true,
                    include_market_analysis: true
                })
            });
            
            if (!response.ok) {
                throw new Error('AI API request failed');
            }
            
            const aiIdea = await response.json();
            
            const newIdea = {
                name: aiIdea.name,
                description: aiIdea.description,
                category: aiIdea.category,
                targetAudience: aiIdea.target_audience,
                monthlyRevenue: aiIdea.monthly_revenue,
                businessModel: aiIdea.business_model,
                mvpFeatures: aiIdea.mvp_features,
                marketSize: aiIdea.market_size,
                competitiveAdvantage: aiIdea.competitive_advantage,
                aiIntegration: aiIdea.ai_integration,
                sourceProblem: aiIdea.source_problem,
                confidenceScore: aiIdea.confidence_score,
                marketAnalysis: aiIdea.market_analysis
            };
            
            allIdeas.push(newIdea);
            counter++;
            
        } catch (error) {
            console.error('AI Error:', error);
            
            const newIdea = generateRandomIdea();
            allIdeas.push(newIdea);
            counter++;
        }
    }
    
    document.getElementById('counter').textContent = counter;
    updateStats();
    filterIdeas();
    
    generateBtn.disabled = false;
    generateBtn.textContent = '🚀 Generate AI Idea';
}

function filterIdeas() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const selectedCategory = document.getElementById('categorySelect').value;
    const minRevenue = parseInt(document.getElementById('minRevenue').value) || 0;
    const maxRevenue = parseInt(document.getElementById('maxRevenue').value) || Infinity;
    const sortOrder = document.getElementById('sortOrder').value;
    
    let filteredIdeas = allIdeas.filter(idea => {
        const matchesSearch = idea.name.toLowerCase().includes(searchTerm) || 
                            idea.category.toLowerCase().includes(searchTerm);
        const matchesCategory = !selectedCategory || idea.category.toLowerCase() === selectedCategory;
        const matchesRevenue = idea.monthlyRevenue >= minRevenue && idea.monthlyRevenue <= maxRevenue;
        
        return matchesSearch && matchesCategory && matchesRevenue;
    });
    
    switch(sortOrder) {
        case 'revenue-high':
            filteredIdeas.sort((a, b) => b.monthlyRevenue - a.monthlyRevenue);
            break;
        case 'revenue-low':
            filteredIdeas.sort((a, b) => a.monthlyRevenue - b.monthlyRevenue);
            break;
        case 'name':
            filteredIdeas.sort((a, b) => a.name.localeCompare(b.name));
            break;
    }
    
    displayIdeas(filteredIdeas);
}

function displayIdeas(ideas) {
    const container = document.getElementById('ideasContainer');
    if (!container) {
        console.error('Ideas container not found');
        return;
    }
    
    container.innerHTML = '';
    
    if (ideas.length === 0) {
        container.innerHTML = '<p style="color: white; text-align: center;">No ideas generated yet. Click "Generate 3 AI Ideas" to start!</p>';
        return;
    }
    
    ideas.forEach(idea => {
        const ideaCard = document.createElement('div');
        ideaCard.className = 'idea-card';
        
        const aiFeatures = idea.aiIntegration ? `
            <div class="detail-item">
                <span class="detail-label">🤖 AI Integration:</span>
                <span class="detail-value">${idea.aiIntegration}</span>
            </div>
        ` : '';
        
        const businessModel = idea.businessModel ? `
            <div class="detail-item">
                <span class="detail-label">💼 Business Model:</span>
                <span class="detail-value">${idea.businessModel}</span>
            </div>
        ` : '';
        
        const sourceProblem = idea.sourceProblem ? `
            <div class="detail-item">
                <span class="detail-label">📊 Source Problem:</span>
                <span class="detail-value">${idea.sourceProblem.substring(0, 50)}...</span>
            </div>
        ` : '';
        
        const confidenceScore = idea.confidenceScore ? `
            <div class="detail-item">
                <span class="detail-label">🎯 Confidence:</span>
                <span class="detail-value">${idea.confidenceScore}%</span>
            </div>
        ` : '';
        
        const isFavorite = favoriteIdeas.has(idea.name);
        
        ideaCard.innerHTML = `
            <button class="favorite-btn ${isFavorite ? 'active' : ''}" onclick="toggleFavorite('${idea.name}')">
                <i class="fas fa-heart"></i>
            </button>
            <div class="idea-name">${idea.name || 'Unnamed Idea'}</div>
            <div class="idea-description">${idea.description || 'No description available'}</div>
            <div class="idea-details">
                <div class="detail-item">
                    <span class="detail-label"><i class="fas fa-tag"></i> Category:</span>
                    <span class="detail-value">${idea.category || 'General'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label"><i class="fas fa-users"></i> Target Audience:</span>
                    <span class="detail-value">${idea.targetAudience || 'General audience'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label"><i class="fas fa-dollar-sign"></i> Monthly Revenue:</span>
                    <span class="detail-value revenue">$${(idea.monthlyRevenue || 0).toLocaleString()}</span>
                </div>
                ${businessModel}
                ${aiFeatures}
                ${sourceProblem}
                ${confidenceScore}
            </div>
            <div class="tags">
                <span class="tag">${idea.category || 'General'}</span>
                ${idea.aiIntegration ? '<span class="tag">🤖 AI-Powered</span>' : ''}
            </div>
        `;
        
        container.appendChild(ideaCard);
    });
}

function toggleFavorite(ideaName) {
    if (favoriteIdeas.has(ideaName)) {
        favoriteIdeas.delete(ideaName);
    } else {
        favoriteIdeas.add(ideaName);
    }
    document.getElementById('favoriteCount').textContent = favoriteIdeas.size;
    displayIdeas(allIdeas.filter(idea => {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const selectedCategory = document.getElementById('categorySelect').value;
        const minRevenue = parseInt(document.getElementById('minRevenue').value) || 0;
        const maxRevenue = parseInt(document.getElementById('maxRevenue').value) || Infinity;
        
        const matchesSearch = idea.name.toLowerCase().includes(searchTerm) || 
                            idea.category.toLowerCase().includes(searchTerm);
        const matchesCategory = !selectedCategory || idea.category.toLowerCase() === selectedCategory;
        const matchesRevenue = idea.monthlyRevenue >= minRevenue && idea.monthlyRevenue <= maxRevenue;
        
        return matchesSearch && matchesCategory && matchesRevenue;
    }));
}

function exportIdeas() {
    const dataStr = JSON.stringify(allIdeas, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'startup-ideas.json';
    link.click();
}

function clearAllIdeas() {
    if (confirm('Are you sure you want to clear all ideas?')) {
        allIdeas = [];
        usedIdeas.clear();
        favoriteIdeas.clear();
        counter = 0;
        document.getElementById('counter').textContent = 0;
        document.getElementById('favoriteCount').textContent = 0;
        updateStats();
        displayIdeas([]);
    }
}

function toggleTheme() {
    isDarkTheme = !isDarkTheme;
    document.body.classList.toggle('dark-theme', isDarkTheme);
    const themeBtn = document.getElementById('themeBtn');
    themeBtn.innerHTML = isDarkTheme ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
}

function showFavorites() {
    const favoritesList = allIdeas.filter(idea => favoriteIdeas.has(idea.name));
    displayIdeas(favoritesList);
}

function updateStats() {
    if (allIdeas.length === 0) {
        document.getElementById('avgRevenue').textContent = '0';
        document.getElementById('topCategory').textContent = 'None';
        return;
    }
    
    const avgRevenue = Math.round(allIdeas.reduce((sum, idea) => sum + idea.monthlyRevenue, 0) / allIdeas.length);
    document.getElementById('avgRevenue').textContent = avgRevenue.toLocaleString();
    
    const categoryCount = {};
    allIdeas.forEach(idea => {
        categoryCount[idea.category] = (categoryCount[idea.category] || 0) + 1;
    });
    
    const topCategory = Object.keys(categoryCount).reduce((a, b) => 
        categoryCount[a] > categoryCount[b] ? a : b, Object.keys(categoryCount)[0] || 'None'
    );
    
    document.getElementById('topCategory').textContent = topCategory;
}



// Initialize the app when page loads
document.addEventListener('DOMContentLoaded', initializeApp);