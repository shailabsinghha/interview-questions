let questionsData = [];
let filteredQuestions = [];
let currentPage = 1;
const questionsPerPage = 15;
let currentTopic = 'all';
let currentDifficulty = 'all';
let searchQuery = '';
let selectedQuestions = new Set();

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function renderMath(element) {
}

function latexToPlainText(text) {
    // Convert LaTeX to readable plain text for DOCX export
    return text
        // Remove displayed equation delimiters
        .replace(/\$\$/g, '')
        // Remove inline math delimiters  
        .replace(/\$/g, '')
        // Convert \frac{a}{b} → a/b
        .replace(/\\frac\{([^}]*)\}\{([^}]*)\}/g, '$1/$2')
        // Convert \sqrt{x} → sqrt(x)
        .replace(/\\sqrt(\[[^\]]*\])?\{([^}]*)\}/g, 'sqrt($2)')
        // Convert \sum → sum, \prod → prod, \int → int
        .replace(/\\(sum|prod|int|oint|iint|iiint)/g, '$1')
        // Convert \to → →, \rightarrow → →
        .replace(/\\(to|rightarrow|leftarrow|Rightarrow|Leftarrow)/g, '→')
        // Convert \ne → !=, \neq → !=
        .replace(/\\(neq|ne)/g, '!=')
        // Convert \le → <=, \ge → >=, \leq → <=, \geq → >=
        .replace(/\\(leq|le)/g, '<=')
        .replace(/\\(geq|ge)/g, '>=')
        // Convert \times → x, \cdot → ·
        .replace(/\\times/g, 'x')
        .replace(/\\cdot/g, '*')
        // Convert \pm → ±
        .replace(/\\pm/g, '±')
        // Convert \infty → ∞
        .replace(/\\infty/g, '∞')
        // Convert \ldots, \cdots → ...
        .replace(/\\(ldots|cdots|vdots|ddots)/g, '...')
        // Convert \text{...} → content
        .replace(/\\text\{([^}]*)\}/g, '$1')
        // Convert \mathrm{...} → content
        .replace(/\\mathrm\{([^}]*)\}/g, '$1')
        // Convert \mathbf{...} → content
        .replace(/\\mathbf\{([^}]*)\}/g, '$1')
        // Convert \binom{a}{b} → C(a,b)
        .replace(/\\binom\{([^}]*)\}\{([^}]*)\}/g, 'C($1,$2)')
        // Remove remaining \{ \}
        .replace(/\\\{/g, '{')
        .replace(/\\\}/g, '}')
        // Remove remaining backslash commands not caught above
        .replace(/\\([a-zA-Z]+)/g, '')
        // Remove single braces { } used for LaTeX grouping
        .replace(/\{([^{}]*)\}/g, '$1')
        // Clean up whitespace
        .replace(/\s+/g, ' ')
        .trim();
}

document.addEventListener('DOMContentLoaded', () => {
    loadQuestions();
    setupEventListeners();
});

function shuffleArray(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

async function loadQuestions() {
    try {
        const response = await fetch('questions.json');
        questionsData = await response.json();
        shuffleArray(questionsData);
        filteredQuestions = [...questionsData];
        buildTopicFilters();
        updateCounts();
        renderQuestions();
    } catch (error) {
        console.error('Error loading questions:', error);
    }
}

const TOPIC_ICONS = {
    'DSA': 'fa-code',
    'Spring Boot': 'fa-leaf',
    'AWS': 'fab fa-aws',
    'MongoDB': 'fa-leaf',
    'Troubleshooting': 'fa-wrench',
    'Kubernetes': 'fa-dharmachakra',
    'Docker': 'fab fa-docker',
    'System Design': 'fa-sitemap',
    'Security': 'fa-shield-alt',
    'Performance': 'fa-tachometer-alt',
    'HTML': 'fab fa-html5',
    'Microservices': 'fa-cubes',
    'Generative AI': 'fa-brain',
    'Behavioral': 'fa-users',
    'Puzzle': 'fa-puzzle-piece'
};

const TOPIC_COLORS = {
    'MongoDB': '#00AD3D',
    'Spring Boot': '#6BBF48',
    'AWS': '#FF9900',
    'DSA': '#818cf8',
    'Troubleshooting': '#f59e0b',
    'Kubernetes': '#3b82f6',
    'Docker': '#06b6d4',
    'System Design': '#8b5cf6',
    'Security': '#ef4444',
    'Performance': '#f59e0b',
    'HTML': '#e34f26',
    'Microservices': '#14b8a6',
    'Generative AI': '#a855f7',
    'Behavioral': '#f97316',
    'Puzzle': '#ec4899'
};

function getTopicIcon(topic) {
    return TOPIC_ICONS[topic] || 'fa-tag';
}

function getTopicColor(topic) {
    return TOPIC_COLORS[topic] || '#6366f1';
}

function buildTopicFilters() {
    const container = document.getElementById('topicFilters');
    container.innerHTML = '';

    // Compute topic counts from data
    const topicCounts = {};
    questionsData.forEach(q => {
        topicCounts[q.topic] = (topicCounts[q.topic] || 0) + 1;
    });

    const allLabel = document.createElement('label');
    allLabel.className = 'filter-option active';
    allLabel.dataset.topic = 'all';
    allLabel.innerHTML = `
        <input type="radio" name="topic" value="all" checked>
        <span class="filter-content">
            <i class="fas fa-globe"></i>
            All Topics
            <span class="count" id="countAll">${questionsData.length}</span>
        </span>
    `;
    container.appendChild(allLabel);

    const sortedTopics = Object.entries(topicCounts)
        .sort((a, b) => b[1] - a[1]);

    sortedTopics.forEach(([topic, count]) => {
        const label = document.createElement('label');
        label.className = 'filter-option';
        label.dataset.topic = topic;
        const icon = getTopicIcon(topic);
        const color = getTopicColor(topic);
        label.innerHTML = `
            <input type="radio" name="topic" value="${topic}">
            <span class="filter-content">
                <i class="${icon}" style="color:${color}"></i>
                ${topic}
                <span class="count" style="background:${color}">${count}</span>
            </span>
        `;
        container.appendChild(label);
    });

    // Always add Behavioral topic (built-in questions, not in questions.json)
    const behLabel = document.createElement('label');
    behLabel.className = 'filter-option';
    behLabel.dataset.topic = 'Behavioral';
    behLabel.innerHTML = `
        <input type="radio" name="topic" value="Behavioral">
        <span class="filter-content">
            <i class="fa-users" style="color:#f97316"></i>
            Behavioral
            <span class="count" style="background:#f97316">${BUILTIN_BEHAVIORAL_QUESTIONS.length}</span>
        </span>
    `;
    container.appendChild(behLabel);
}

function updateCounts() {
    document.getElementById('totalQuestions').textContent = questionsData.length;
    const topicCounts = {};
    questionsData.forEach(q => {
        topicCounts[q.topic] = (topicCounts[q.topic] || 0) + 1;
    });

    // Include Behavioral topic (built-in, shown in sidebar but not in questions.json)
    topicCounts['Behavioral'] = BUILTIN_BEHAVIORAL_QUESTIONS.length;

    document.getElementById('totalTopics').textContent = Object.keys(topicCounts).length;

    document.getElementById('countAll').textContent = questionsData.length + BUILTIN_BEHAVIORAL_QUESTIONS.length;
    document.querySelectorAll('#topicFilters .filter-option[data-topic]').forEach(label => {
        const topic = label.dataset.topic;
        if (topic === 'all') return;
        const countSpan = label.querySelector('.count');
        if (countSpan && topicCounts[topic] !== undefined) {
            countSpan.textContent = topicCounts[topic];
        }
    });
}

function setupEventListeners() {
    const difficultyFilters = document.querySelectorAll('input[name="difficulty"]');
    const searchInput = document.getElementById('searchInput');
    const clearSearch = document.getElementById('clearSearch');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const resetBtn = document.getElementById('resetFilters');
    const closeModal = document.getElementById('closeModal');
    const clearSelection = document.getElementById('clearSelection');
    const downloadSelected = document.getElementById('downloadSelected');
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const refreshBtn = document.getElementById('refreshBtn');
    const sidebar = document.querySelector('.sidebar');

    hamburgerBtn.addEventListener('click', () => {
        const isOpen = sidebar.classList.toggle('show');
        hamburgerBtn.classList.toggle('open', isOpen);
        const icon = hamburgerBtn.querySelector('i');
        icon.className = isOpen ? 'fas fa-times' : 'fas fa-bars';
    });

    refreshBtn.addEventListener('click', async () => {
        refreshBtn.classList.add('spinning');
        try {
            const response = await fetch('questions.json?_=' + Date.now());
            const freshData = await response.json();
            questionsData = freshData;
            shuffleArray(questionsData);

            document.getElementById('topicFilters').innerHTML = '';
            buildTopicFilters();
            updateCounts();

            // Restore current topic selection after rebuild
            const topicRadio = document.querySelector(`input[name="topic"][value="${currentTopic}"]`);
            if (topicRadio) {
                topicRadio.checked = true;
                document.querySelectorAll('.filter-option[data-topic]').forEach(opt => {
                    opt.classList.toggle('active', opt.dataset.topic === currentTopic);
                });
            }

            currentPage = 1;
            applyFilters();
        } catch (error) {
            console.error('Refresh failed:', error);
        }
        setTimeout(() => refreshBtn.classList.remove('spinning'), 600);
    });

    function closeSidebar() {
        sidebar.classList.remove('show');
        hamburgerBtn.classList.remove('open');
        hamburgerBtn.querySelector('i').className = 'fas fa-bars';
    }

    document.getElementById('sidebarOverlay').addEventListener('click', closeSidebar);

    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && sidebar.classList.contains('show') &&
            !sidebar.contains(e.target) && e.target !== hamburgerBtn && !hamburgerBtn.contains(e.target)) {
            closeSidebar();
        }
    });

    document.getElementById('topicFilters').addEventListener('change', (e) => {
        if (e.target.matches('input[name="topic"]')) {
            document.querySelectorAll('.filter-option[data-topic]').forEach(opt => {
                opt.classList.toggle('active', opt.dataset.topic === e.target.value);
            });
            currentTopic = e.target.value;
            currentPage = 1;
            applyFilters();
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('show');
            }
        }
    });

    difficultyFilters.forEach(filter => {
        filter.addEventListener('change', (e) => {
            document.querySelectorAll('.filter-option[data-difficulty]').forEach(opt => {
                opt.classList.toggle('active', opt.dataset.difficulty === e.target.value);
            });
            currentDifficulty = e.target.value;
            currentPage = 1;
            applyFilters();
        });
    });

    searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value.toLowerCase();
        currentPage = 1;
        clearSearch.style.display = searchQuery ? 'flex' : 'none';
        applyFilters();
    });

    clearSearch.addEventListener('click', () => {
        searchInput.value = '';
        searchQuery = '';
        clearSearch.style.display = 'none';
        currentPage = 1;
        applyFilters();
    });

    loadMoreBtn.addEventListener('click', () => {
        currentPage++;
        renderQuestions(false);
    });

    resetBtn.addEventListener('click', () => {
        currentTopic = 'all';
        currentDifficulty = 'all';
        searchQuery = '';
        
        document.querySelector('input[name="topic"][value="all"]').checked = true;
        document.querySelector('input[name="difficulty"][value="all"]').checked = true;
        
        document.querySelectorAll('.filter-option').forEach(opt => {
            if (opt.dataset.topic === 'all' || opt.dataset.difficulty === 'all') {
                opt.classList.add('active');
            } else {
                opt.classList.remove('active');
            }
        });

        document.getElementById('searchInput').value = '';
        document.getElementById('clearSearch').style.display = 'none';
        
        currentPage = 1;
        applyFilters();
    });

    closeModal.addEventListener('click', () => {
        document.getElementById('questionModal').classList.remove('show');
    });

    document.getElementById('questionModal').addEventListener('click', (e) => {
        if (e.target.id === 'questionModal') {
            document.getElementById('questionModal').classList.remove('show');
        }
    });

    clearSelection.addEventListener('click', () => {
        selectedQuestions.clear();
        document.querySelectorAll('.question-card').forEach(card => {
            card.classList.remove('selected');
            card.querySelector('.select-checkbox input').checked = false;
        });
        updateSelectionBar();
    });

    downloadSelected.addEventListener('click', () => {
        if (selectedQuestions.size === 0) {
            alert('Please select at least one question');
            return;
        }
        document.getElementById('downloadModal').classList.add('show');
    });

    document.getElementById('closeDownloadModal').addEventListener('click', () => {
        document.getElementById('downloadModal').classList.remove('show');
    });

    document.getElementById('downloadModal').addEventListener('click', (e) => {
        if (e.target.id === 'downloadModal') {
            document.getElementById('downloadModal').classList.remove('show');
        }
    });

    document.getElementById('confirmDownload').addEventListener('click', () => {
        const candidateName = document.getElementById('candidateName').value.trim();
        if (!candidateName) {
            alert('Please enter candidate name');
            return;
        }

        const viewType = document.querySelector('input[name="viewType"]:checked').value;
        downloadDOCXWithOptions(candidateName, viewType);
        document.getElementById('downloadModal').classList.remove('show');
    });
}

function updateSelectionBar() {
    const bar = document.getElementById('selectionBar');
    const count = document.getElementById('selectedCount');
    
    count.textContent = selectedQuestions.size;
    
    if (selectedQuestions.size > 0) {
        bar.classList.add('show');
    } else {
        bar.classList.remove('show');
    }
}

function downloadDOCXWithOptions(candidateName, viewType) {
    const selectedData = questionsData.filter(q => selectedQuestions.has(q.id));
    
    if (selectedData.length === 0) {
        alert('No questions selected');
        return;
    }
    
    const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = docx;
    
    const children = [];
    
    if (viewType === 'candidate') {
        children.push(
            new Paragraph({
                text: "INTERVIEW QUESTIONS - CANDIDATE VIEW",
                heading: HeadingLevel.HEADING_1,
                alignment: AlignmentType.CENTER
            }),
            new Paragraph({ text: "" }),
            new Paragraph({ text: `Candidate: ${candidateName}` }),
            new Paragraph({ text: `Total Questions: ${selectedData.length}` }),
            new Paragraph({ text: `Date: ${new Date().toLocaleDateString()}` }),
            new Paragraph({ text: "" }),
            new Paragraph({ text: "Answer the following questions:", heading: HeadingLevel.HEADING_2 }),
            new Paragraph({ text: "" })
        );
        
        selectedData.forEach((q, i) => {
            children.push(
                new Paragraph({
                    text: `Question ${i + 1}:`,
                    heading: HeadingLevel.HEADING_3
                }),
                new Paragraph({ text: latexToPlainText(q.question) }),
                new Paragraph({ text: "" })
            );
        });
        
        children.push(
            new Paragraph({ text: "" }),
            new Paragraph({
                text: "MASTER COPY (For Interviewer Use)",
                heading: HeadingLevel.HEADING_1,
                alignment: AlignmentType.CENTER
            }),
            new Paragraph({ text: "" })
        );
        
        selectedData.forEach((q, i) => {
            children.push(
                new Paragraph({ text: `Q${i + 1}. [${q.topic}] ${q.difficulty}` }),
                new Paragraph({ text: `Question: ${latexToPlainText(q.question)}` }),
                new Paragraph({ text: `Answer: ${latexToPlainText(q.answer)}` }),
                new Paragraph({ text: "" })
            );
        });
    } else {
        children.push(
            new Paragraph({
                text: "INTERVIEW QUESTIONS - INTERVIEWER VIEW",
                heading: HeadingLevel.HEADING_1,
                alignment: AlignmentType.CENTER
            }),
            new Paragraph({ text: "" }),
            new Paragraph({ text: `Candidate: ${candidateName}` }),
            new Paragraph({ text: `Total Questions: ${selectedData.length}` }),
            new Paragraph({ text: `Date: ${new Date().toLocaleDateString()}` }),
            new Paragraph({ text: "" })
        );
        
        selectedData.forEach((q, i) => {
            children.push(
                new Paragraph({ text: `Question ${i + 1}`, heading: HeadingLevel.HEADING_2 }),
                new Paragraph({ text: `Topic: ${q.topic}` }),
                new Paragraph({ text: `Difficulty: ${q.difficulty}` }),
                new Paragraph({ text: "" }),
                new Paragraph({ text: "Question:" }),
                new Paragraph({ text: latexToPlainText(q.question) }),
                new Paragraph({ text: "" }),
                new Paragraph({ text: "Answer:" }),
                new Paragraph({ text: latexToPlainText(q.answer) }),
                new Paragraph({ text: "" })
            );
        });
    }
    
    const doc = new Document({
        sections: [{
            properties: {},
            children: children
        }]
    });
    
    Packer.toBlob(doc).then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        const filename = `Interview_Questions_${candidateName.replace(/\s+/g, '_')}_${viewType}.docx`;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
}

function applyFilters() {
    let source = questionsData;

    // Behavioral questions come from the built-in list, not questions.json
    if (currentTopic === 'Behavioral') {
        source = BUILTIN_BEHAVIORAL_QUESTIONS.map((q, i) => ({
            ...q,
            id: q.id || `beh_${i}`
        }));
    }

    filteredQuestions = source.filter(q => {
        const matchesTopic = currentTopic === 'all' || q.topic === currentTopic;
        const matchesDifficulty = currentDifficulty === 'all' || q.difficulty === currentDifficulty;
        const matchesSearch = searchQuery === '' || 
            q.question.toLowerCase().includes(searchQuery) ||
            q.answer.toLowerCase().includes(searchQuery) ||
            q.topic.toLowerCase().includes(searchQuery);
        
        return matchesTopic && matchesDifficulty && matchesSearch;
    });

    shuffleArray(filteredQuestions);
    renderQuestions();
}

function renderQuestions(reset = true) {
    const container = document.getElementById('questionsContainer');
    const noResults = document.getElementById('noResults');
    const loadMoreSection = document.getElementById('loadMoreSection');
    
    if (reset) {
        container.innerHTML = '';
    }

    const startIndex = (currentPage - 1) * questionsPerPage;
    const endIndex = startIndex + questionsPerPage;
    const questionsToShow = filteredQuestions.slice(startIndex, endIndex);

    document.getElementById('showingResults').textContent = 
        `Showing ${Math.min(startIndex + questionsToShow.length, filteredQuestions.length)} of ${filteredQuestions.length} questions`;

    if (filteredQuestions.length === 0) {
        noResults.style.display = 'block';
        loadMoreSection.style.display = 'none';
        return;
    }

    noResults.style.display = 'none';
    loadMoreSection.style.display = filteredQuestions.length > endIndex ? 'block' : 'none';

    questionsToShow.forEach((q, index) => {
        const card = createQuestionCard(q, startIndex + index + 1);
        container.appendChild(card);
        renderMath(card);
    });
}

function createQuestionCard(q, number) {
    const card = document.createElement('div');
    card.className = 'question-card';
    card.style.animationDelay = `${(number % questionsPerPage) * 0.05}s`;

    const topicClass = q.topic.toLowerCase().replace(' ', '').replace('spring', 'springboot');
    const difficultyClass = q.difficulty.toLowerCase();

    const isSelected = selectedQuestions.has(q.id);

    card.innerHTML = `
        <div class="card-header">
            <label class="select-checkbox">
                <input type="checkbox" ${isSelected ? 'checked' : ''}>
                <span class="checkmark"></span>
            </label>
            <span class="topic-badge" data-topic="${escapeHtml(q.topic)}">${escapeHtml(q.topic)}</span>
            <span class="difficulty-badge ${difficultyClass}">${escapeHtml(q.difficulty)}</span>
        </div>
        <div class="card-body">
            <p class="question-text">${escapeHtml(latexToPlainText(q.question))}</p>
            <div class="answer-section">
                <button class="toggle-answer">
                    <span>Show Solution</span>
                    <i class="fas fa-chevron-down"></i>
                </button>
                <div class="answer-content">
                    <p>${escapeHtml(latexToPlainText(q.answer))}</p>
                </div>
            </div>
        </div>
    `;

    const checkbox = card.querySelector('.select-checkbox input');
    checkbox.addEventListener('change', (e) => {
        e.stopPropagation();
        
        if (e.target.checked) {
            selectedQuestions.add(q.id);
            card.classList.add('selected');
        } else {
            selectedQuestions.delete(q.id);
            card.classList.remove('selected');
        }
        
        updateSelectionBar();
    });

    const toggleBtn = card.querySelector('.toggle-answer');
    const answerContent = card.querySelector('.answer-content');

    toggleBtn.addEventListener('click', () => {
        toggleBtn.classList.toggle('active');
        answerContent.classList.toggle('show');
        toggleBtn.querySelector('span').textContent = 
            answerContent.classList.contains('show') ? 'Hide Solution' : 'Show Solution';
        if (answerContent.classList.contains('show')) {
            renderMath(answerContent);
        }
    });

    if (isSelected) {
        card.classList.add('selected');
    }

    return card;
}

function showModal(q) {
    const modal = document.getElementById('questionModal');
    const topicClass = q.topic.toLowerCase().replace(' ', '').replace('spring', 'springboot');
    const difficultyClass = q.difficulty.toLowerCase();

    document.getElementById('modalTopic').textContent = q.topic;
    document.getElementById('modalTopic').setAttribute('data-topic', q.topic);
    document.getElementById('modalDifficulty').textContent = q.difficulty;
    document.getElementById('modalDifficulty').className = `difficulty-badge ${difficultyClass}`;
    document.getElementById('modalQuestion').innerHTML = escapeHtml(latexToPlainText(q.question));
    document.getElementById('modalAnswer').innerHTML = escapeHtml(latexToPlainText(q.answer));

    renderMath(document.getElementById('modalQuestion'));
    renderMath(document.getElementById('modalAnswer'));

    modal.classList.add('show');
}

/* ═══════════════════════════════════════════
   RESUME-BASED QUESTION GENERATOR
   ═══════════════════════════════════════════ */

const RESUME_TOPIC_KEYWORDS = {
    'MongoDB': ['mongo', 'mongodb', 'nosql', 'document database', 'atlas', 'mongoose', 'unstructured data'],
    'Spring Boot': ['spring', 'spring boot', 'java', 'jpa', 'hibernate', 'rest api', 'restful', 'tomcat', 'servlet'],
    'AWS': ['aws', 'amazon web', 'ec2', 's3', 'lambda', 'cloudformation', 'cloudwatch', 'dynamodb', 'rds', 'route53', 'sns', 'sqs'],
    'DSA': ['algorithm', 'data structure', 'sorting', 'searching', 'complexity', 'leetcode', 'hackerrank', 'big o'],
    'Docker': ['docker', 'containerization', 'dockerfile', 'docker-compose', 'container image'],
    'Kubernetes': ['kubernetes', 'k8s', 'pod', 'deployment', 'service mesh', 'eks', 'aks', 'orchestration'],
    'System Design': ['system design', 'architecture', 'scalable', 'distributed', 'high availability', 'load balancer', 'microservices architecture'],
    'Security': ['security', 'authentication', 'authorization', 'oauth', 'jwt', 'encryption', 'cybersecurity', 'penetration'],
    'Performance': ['performance', 'optimization', 'latency', 'throughput', 'caching', 'bottleneck', 'profiling'],
    'Generative AI': ['ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt', 'openai', 'generative', 'deep learning', 'nlp'],
    'Microservices': ['microservice', 'service mesh', 'api gateway', 'event driven', 'circuit breaker'],
    'HTML': ['html', 'css', 'javascript', 'frontend', 'react', 'angular', 'vue', 'typescript', 'web development'],
    'Troubleshooting': ['debug', 'troubleshoot', 'incident', 'outage', 'monitoring', 'logging', 'error', 'root cause']
};

/* ── Available AI Models from OpenRouter (All Free Models) ──
   Fetched from openrouter.ai/api/v1/models where pricing = $0.
   Default is a capable free model for question generation. */
const AI_MODELS = [
    { group: '✅ FREE (No Credits Needed)', value: 'openrouter/free', label: 'Auto: Best Available (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'nousresearch/hermes-3-llama-3.1-405b:free', label: 'Hermes 3 405B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'openrouter/owl-alpha', label: 'Owl Alpha 773B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'nvidia/nemotron-3-super-120b-a12b:free', label: 'Nemotron 3 Super 120B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'openai/gpt-oss-120b:free', label: 'GPT-OSS 120B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'meta-llama/llama-3.3-70b-instruct:free', label: 'Llama 3.3 70B Instruct (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'qwen/qwen3-next-80b-a3b-instruct:free', label: 'Qwen3 Next 80B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'minimax/minimax-m2.5:free', label: 'MiniMax M2.5 (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'deepseek/deepseek-v4-flash:free', label: 'DeepSeek V4 Flash (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'nvidia/nemotron-3-nano-30b-a3b:free', label: 'Nemotron 3 Nano 30B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free', label: 'Nemotron Nano Omni Reasoning (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'google/gemma-4-31b-it:free', label: 'Gemma 4 31B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'google/gemma-4-26b-a4b-it:free', label: 'Gemma 4 26B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'openai/gpt-oss-20b:free', label: 'GPT-OSS 20B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'cognitivecomputations/dolphin-mistral-24b-venice-edition:free', label: 'Dolphin Mistral 24B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'poolside/laguna-m.1:free', label: 'Laguna M.1 (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'arcee-ai/trinity-large-thinking:free', label: 'Trinity Large Thinking (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'z-ai/glm-4.5-air:free', label: 'GLM 4.5 Air (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'poolside/laguna-xs.2:free', label: 'Laguna XS.2 (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'nvidia/nemotron-nano-12b-v2-vl:free', label: 'Nemotron Nano 12B VL (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'nvidia/nemotron-nano-9b-v2:free', label: 'Nemotron Nano 9B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'qwen/qwen3-coder:free', label: 'Qwen3 Coder (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'baidu/cobuddy:free', label: 'Baidu CoBuddy (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'google/lyria-3-pro-preview', label: 'Lyria 3 Pro (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'google/lyria-3-clip-preview', label: 'Lyria 3 Clip (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'meta-llama/llama-3.2-3b-instruct:free', label: 'Llama 3.2 3B (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'liquid/lfm-2.5-1.2b-thinking:free', label: 'LFM 2.5 1.2B Thinking (Free)' },
    { group: '✅ FREE (No Credits Needed)', value: 'liquid/lfm-2.5-1.2b-instruct:free', label: 'LFM 2.5 1.2B Instruct (Free)' },
];

const BUILTIN_BEHAVIORAL_QUESTIONS = [
    { topic: 'Behavioral', difficulty: 'Easy', question: 'Tell me about a time you had to work under a tight deadline. How did you handle it?', answer: 'Use STAR: Situation (tight deadline), Task (complete project), Action (prioritized, communicated, stayed focused), Result (delivered on time). Shows time management and composure under pressure.' },
    { topic: 'Behavioral', difficulty: 'Easy', question: 'Describe a situation where you had to learn a new technology quickly.', answer: 'Use STAR: Explain the context, what you needed to learn, steps you took (docs, tutorials, mentorship), and how you successfully applied it. Shows adaptability and learning agility.' },
    { topic: 'Behavioral', difficulty: 'Easy', question: 'How do you handle receiving constructive criticism about your code?', answer: 'Show openness to feedback. Explain that you view code reviews as learning opportunities, ask clarifying questions, and apply the feedback to improve.' },
    { topic: 'Behavioral', difficulty: 'Medium', question: 'Tell me about a conflict you had with a teammate. How was it resolved?', answer: 'Use STAR. Show emotional intelligence — listened to their perspective, found common ground, focused on the problem not the person. Emphasize the positive outcome.' },
    { topic: 'Behavioral', difficulty: 'Medium', question: 'Describe a project that failed or went wrong. What did you learn?', answer: 'Own the failure honestly. Explain what happened, your role, what you learned, and how you applied that lesson later. Shows accountability and growth mindset.' },
    { topic: 'Behavioral', difficulty: 'Medium', question: 'Tell me about a time you went above and beyond your job requirements.', answer: 'Describe a specific instance where you took initiative beyond your scope — automating a manual process, helping another team, etc. Quantify the impact.' },
    { topic: 'Behavioral', difficulty: 'Medium', question: 'How do you prioritize your tasks when everything feels urgent?', answer: 'Explain your framework: urgency vs importance matrix, stakeholder communication, saying no when needed. Give a concrete example of how you managed competing priorities.' },
    { topic: 'Behavioral', difficulty: 'Medium', question: 'Describe a time you had to explain a technical concept to a non-technical stakeholder.', answer: 'Show communication skills — how you simplified the concept, used analogies, focused on business impact rather than technical details. Good outcome shows bridging the gap.' },
    { topic: 'Behavioral', difficulty: 'Hard', question: 'Tell me about a time you disagreed with a technical decision made by a senior engineer or manager.', answer: 'Show respectful dissent — how you prepared data/evidence, presented alternatives, and ultimately how the decision was made. Focus on professional disagreement, not ego.' },
    { topic: 'Behavioral', difficulty: 'Hard', question: 'Describe a situation where you had to lead a team through a difficult technical migration.', answer: 'Use STAR: scope of migration, challenges (downtime, data loss risk), your leadership approach (planning, communication, rollback strategy), and the successful outcome.' },
    { topic: 'Behavioral', difficulty: 'Hard', question: 'Tell me about a time you made a decision that was technically correct but had negative business impact.', answer: 'Show that you now understand the tradeoff between technical purity and business needs. Explain what you would do differently. Demonstrates maturity and business acumen.' },
    { topic: 'Behavioral', difficulty: 'Easy', question: 'Why did you choose to become a software engineer / technologist?', answer: 'Share your genuine motivation — problem-solving, building things, impact. A personal story about what sparked your interest is more memorable than generic answers.' },
    { topic: 'Behavioral', difficulty: 'Medium', question: 'Describe a time you mentored or helped a junior team member grow.', answer: 'Use STAR: who you mentored, what specific guidance you provided (code reviews, pair programming), and the measurable improvement in their skills or confidence.' },
    { topic: 'Behavioral', difficulty: 'Hard', question: 'Tell me about a time you had to push back on a feature request that you felt was technically unwise.', answer: 'Show how you balanced technical concerns with business needs. Explain your approach — data-driven reasoning, proposing alternatives, finding compromise.' },
    { topic: 'Behavioral', difficulty: 'Easy', question: 'How do you stay current with new technologies and industry trends?', answer: 'Specific habits: blogs/newsletters you follow, side projects, conferences, open source contributions. Show genuine passion for learning, not just listing sources.' }
];

let resumeState = {
    file: null,
    text: '',
    candidateName: '',
    experienceYears: null,
    duration: 45,
    mode: 'bank',
    selectedModel: 'meta-llama/llama-3.3-70b-instruct:free',
    questions: [],
    selected: new Set()
};

function populateModelSelect() {
    const select = document.getElementById('aiModelSelect');
    if (!select) return;
    select.innerHTML = '';

    const groups = {};
    for (const model of AI_MODELS) {
        if (!groups[model.group]) groups[model.group] = [];
        groups[model.group].push(model);
    }

    const order = [
        '✅ FREE (No Credits Needed)',
        'DeepSeek (Paid)',
        'xAI (Paid)',
        'Mistral (Paid)',
        'OpenAI (Paid)',
        'Anthropic (Paid)',
        'Google (Paid)'
    ];
    for (const groupName of order) {
        if (!groups[groupName]) continue;
        const optgroup = document.createElement('optgroup');
        optgroup.label = groupName;
        for (const model of groups[groupName]) {
            const option = document.createElement('option');
            option.value = model.value;
            option.textContent = model.label;
            if (model.value === resumeState.selectedModel) option.selected = true;
            optgroup.appendChild(option);
        }
        select.appendChild(optgroup);
    }
}

function setupResumeFeature() {
    const resumeBtn = document.getElementById('resumeBtn');
    const resumeModal = document.getElementById('resumeModal');
    const closeBtn = document.getElementById('closeResumeModal');
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('resumeFile');
    const changeFileBtn = document.getElementById('resumeChangeFile');
    const durationSlider = document.getElementById('durationSlider');
    const durationDisplay = document.getElementById('durationDisplay');
    const toggleBank = document.getElementById('toggleBank');
    const toggleAI = document.getElementById('toggleAI');
    const generateBtn = document.getElementById('generateBtn');
    const modelSelect = document.getElementById('aiModelSelect');
    const modelSelectGroup = document.getElementById('modelSelectGroup');
    const apiKeyGroup = document.getElementById('apiKeyGroup');
    const apiKeyInput = document.getElementById('apiKeyInput');
    const toggleApiKeyBtn = document.getElementById('toggleApiKeyBtn');

    // Open modal
    resumeBtn.addEventListener('click', () => {
        resetResumeToStep1();
        // Load saved API key
        const savedKey = localStorage.getItem('openrouter_api_key') || '';
        if (apiKeyInput) apiKeyInput.value = savedKey;
        resumeModal.classList.add('show');
    });

    closeBtn.addEventListener('click', () => resumeModal.classList.remove('show'));
    resumeModal.addEventListener('click', (e) => {
        if (e.target === resumeModal) resumeModal.classList.remove('show');
    });

    // Upload zone: click to browse
    uploadZone.addEventListener('click', () => fileInput.click());

    // Drag-and-drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) handleResumeFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) handleResumeFile(e.target.files[0]);
    });

    changeFileBtn.addEventListener('click', () => resetResumeToStep1());

    // Duration slider
    durationSlider.addEventListener('input', () => {
        resumeState.duration = parseInt(durationSlider.value);
        durationDisplay.textContent = `${resumeState.duration} min`;
    });

    // Source toggle
    toggleBank.addEventListener('click', () => {
        toggleBank.classList.add('active');
        toggleAI.classList.remove('active');
        resumeState.mode = 'bank';
        if (modelSelectGroup) modelSelectGroup.style.display = 'none';
        if (apiKeyGroup) apiKeyGroup.style.display = 'none';
    });
    toggleAI.addEventListener('click', () => {
        toggleAI.classList.add('active');
        toggleBank.classList.remove('active');
        resumeState.mode = 'ai';
        if (modelSelectGroup) modelSelectGroup.style.display = 'block';
        if (apiKeyGroup) apiKeyGroup.style.display = 'block';
        // Auto-test default model on first show
        const status = document.getElementById('modelStatus');
        if (status && !status.dataset.tested) {
            testAIModel();
        }
    });

    // Model select change
    if (modelSelect) {
        modelSelect.addEventListener('change', () => {
            resumeState.selectedModel = modelSelect.value;
            // Clear previous test status when model changes
            const status = document.getElementById('modelStatus');
            if (status) {
                status.textContent = '';
                status.className = 'model-status';
                delete status.dataset.tested;
                delete status.dataset.valid;
            }
        });
    }

    // Test model button
    const testBtn = document.getElementById('testModelBtn');
    if (testBtn) {
        testBtn.addEventListener('click', testAIModel);
    }

    // API key input: save to localStorage on change
    if (apiKeyInput) {
        apiKeyInput.addEventListener('input', () => {
            localStorage.setItem('openrouter_api_key', apiKeyInput.value);
        });
    }

    // Toggle API key visibility
    if (toggleApiKeyBtn) {
        toggleApiKeyBtn.addEventListener('click', () => {
            if (!apiKeyInput) return;
            const isPassword = apiKeyInput.type === 'password';
            apiKeyInput.type = isPassword ? 'text' : 'password';
            toggleApiKeyBtn.innerHTML = isPassword
                ? '<i class="fas fa-eye-slash"></i>'
                : '<i class="fas fa-eye"></i>';
        });
    }

    // Populate model select dropdown
    populateModelSelect();

    // Generate
    generateBtn.addEventListener('click', generateResumeQuestions);

    // Download generated
    document.getElementById('downloadGenQuestions').addEventListener('click', downloadGeneratedQuestions);
    document.getElementById('resetGenQuestions').addEventListener('click', () => {
        resetResumeToStep1();
    });
}

function resetResumeToStep1() {
    resumeState.file = null;
    resumeState.text = '';
    resumeState.candidateName = '';
    resumeState.questions = [];
    resumeState.selected = new Set();

    document.getElementById('resumeStep1').style.display = 'block';
    document.getElementById('resumeStep2').style.display = 'none';
    document.getElementById('resumeStep3').style.display = 'none';
    document.getElementById('resumeFile').value = '';

    const zone = document.getElementById('uploadZone');
    zone.classList.remove('has-file');
    zone.querySelector('.upload-title').textContent = 'Drop your resume here';
    zone.querySelector('.upload-sub').textContent = 'or click to browse · PDF or DOCX';
}

function showResumeStep(step) {
    document.getElementById('resumeStep1').style.display = step === 1 ? 'block' : 'none';
    document.getElementById('resumeStep2').style.display = step === 2 ? 'block' : 'none';
    document.getElementById('resumeStep3').style.display = step === 3 ? 'block' : 'none';
}

async function handleResumeFile(file) {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const ext = file.name.split('.').pop().toLowerCase();

    if (!['pdf', 'docx'].includes(ext)) {
        alert('Please upload a PDF or DOCX file.');
        return;
    }

    resumeState.file = file;
    document.getElementById('resumeFileName').textContent = file.name;

    // Show file state in upload zone
    const zone = document.getElementById('uploadZone');
    zone.classList.add('has-file');
    zone.querySelector('.upload-title').textContent = '✓ Resume loaded';
    zone.querySelector('.upload-sub').textContent = file.name;

    try {
        let text = '';
        if (ext === 'pdf') {
            text = await extractTextFromPDF(file);
        } else {
            text = await extractTextFromDOCX(file);
        }

        resumeState.text = text;
        resumeState.candidateName = extractNameFromText(text);
        resumeState.experienceYears = extractExperienceYears(text);

        const nameInput = document.getElementById('candidateNameResume');
        nameInput.value = resumeState.candidateName;
        nameInput.placeholder = resumeState.candidateName || 'Enter candidate name...';

        showResumeStep(2);
    } catch (err) {
        console.error('Resume parsing error:', err);
        alert('Failed to parse resume. Please try again.');
        resetResumeToStep1();
    }
}

async function extractTextFromPDF(file) {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    let fullText = '';

    for (let i = 1; i <= Math.min(pdf.numPages, 20); i++) {
        const page = await pdf.getPage(i);
        const content = await page.getTextContent();
        const pageText = content.items.map(item => item.str).join(' ');
        fullText += pageText + '\n';
    }

    return fullText;
}

async function extractTextFromDOCX(file) {
    const arrayBuffer = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer });
    return result.value;
}

function extractNameFromText(text) {
    // Strategy 1: Look for "Name:" or "NAME" patterns
    const namePatterns = [
        /(?:^|\n)\s*Name\s*[:;]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)/,
        /(?:^|\n)\s*(?:Candidate|Applicant)\s*[:;]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)/,
        /(?:^|\n)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s*[|]/
    ];

    for (const pattern of namePatterns) {
        const match = text.match(pattern);
        if (match) return match[1].trim();
    }

    // Strategy 2: First non-empty line that looks like a name (2-4 words, capitalized)
    const lines = text.split('\n')
        .map(l => l.trim())
        .filter(l => l.length > 0);

    for (const line of lines.slice(0, 5)) {
        const words = line.split(/\s+/);
        if (words.length >= 2 && words.length <= 4) {
            const allCapped = words.every(w => /^[A-Z][a-z]/.test(w));
            const hasLower = words.some(w => /[a-z]/.test(w));
            if (allCapped || (hasLower && /^[A-Z]/.test(words[0]))) {
                return line;
            }
        }
    }

    return '';
}

function extractExperienceYears(text) {
    // Pattern 1: Direct experience phrases — covers years, yrs, yr, YOE, experience, exp
    const directPats = [
        /(\d+)\s*\+?\s*(?:years?|yrs?|YOE)\s+(?:of\s+)?(?:experience|exp|work)/i,
        /(?:experience|exp|work)\s*[:\s]+(\d+)\s*\+?\s*(?:years?|yrs?|YOE)/i,
        /(\d+)\s*\+\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)/i,
        /worked\s+(?:for|over|close to)\s+(\d+)\s*\+?\s*(?:years?|yrs?)/i,
        /(\d+)\s*(?:-|–|to)\s*\d+\s+(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)/i,
        /total\s+(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)\s*[:\s]+(\d+)/i,
        /(\d+)\s*\+?\s*(?:years?|yrs?)\s+in\s+(?:the\s+)?(?:industry|it|software|tech|engineering)/i
    ];
    for (const p of directPats) {
        const m = text.match(p);
        if (m) { const y = parseInt(m[1]); if (y > 0 && y < 50) return y; }
    }

    // Pattern 2: Graduation / degree year
    const gradPats = [
        /(?:graduated|graduate|completed|passed)\s*(?:in|:)?\s*((?:19|20)\d{2})/i,
        /(?:b\.?(?:tech|e|sc|a)|m\.?(?:tech|sc|a|ba)|ph\.?d|bachelor|master|phd)\s*[\)\]]?\s*((?:19|20)\d{2})/i,
        /(?:class|batch)\s+of\s+((?:19|20)\d{2})/i
    ];
    for (const p of gradPats) {
        const m = text.match(p);
        if (m) { const y = parseInt(m[1]); if (y > 1980 && y <= 2026) return Math.max(1, 2026 - y - 2); }
    }

    // Pattern 3: Date ranges in work history (e.g. "2018 - 2022", "2019 - Present")
    const rangePat = /((?:19|20)\d{2})\s*(?:-|–|to)\s*((?:19|20)\d{2}|present|now|current)/gi;
    let total = 0, match, count = 0;
    while ((match = rangePat.exec(text)) !== null) {
        const start = parseInt(match[1]);
        const end = match[2].match(/\d{4}/) ? parseInt(match[2]) : 2026;
        if (start > 1980 && end >= start) { total += (end - start); count++; }
    }
    if (count > 0 && total > 0 && total < 50) return Math.round(total);

    return null;
}

function getDifficultyMix(experienceYears) {
    if (experienceYears === null || experienceYears === undefined) return { easy: 0.4, medium: 0.35, hard: 0.25 };
    if (experienceYears <= 2)  return { easy: 0.6, medium: 0.3, hard: 0.1 };
    if (experienceYears <= 5)  return { easy: 0.35, medium: 0.4, hard: 0.25 };
    if (experienceYears <= 8)  return { easy: 0.2, medium: 0.4, hard: 0.4 };
    return { easy: 0.1, medium: 0.3, hard: 0.6 };
}

function matchTopicsFromResume(text) {
    const lower = text.toLowerCase();
    const scores = {};

    for (const [topic, keywords] of Object.entries(RESUME_TOPIC_KEYWORDS)) {
        let score = 0;
        for (const kw of keywords) {
            const regex = new RegExp(kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
            const matches = lower.match(regex);
            if (matches) score += matches.length;
        }
        if (score > 0) scores[topic] = score;
    }

    return scores;
}

function selectQuestionsForDuration(topicScores, durationMinutes, experienceYears) {
    const totalQuestions = Math.round(durationMinutes / 2.5);
    if (totalQuestions < 2) return [];

    // Allocate ~20% of questions to behavioral
    const behavioralCount = Math.max(2, Math.round(totalQuestions * 0.2));
    const techCount = totalQuestions - behavioralCount;

    // Pick behavioral questions
    const shuffledBehavioral = shuffleArray([...BUILTIN_BEHAVIORAL_QUESTIONS]);
    const difficultyMix = getDifficultyMix(experienceYears);

    // Pick behavioral matching experience level (more experienced = harder behavioral)
    const behavioralEasy = shuffledBehavioral.filter(q => q.difficulty === 'Easy');
    const behavioralMedium = shuffledBehavioral.filter(q => q.difficulty === 'Medium');
    const behavioralHard = shuffledBehavioral.filter(q => q.difficulty === 'Hard');

    const bEasyCount = Math.round(behavioralCount * difficultyMix.easy);
    const bMedCount = Math.round(behavioralCount * difficultyMix.medium);
    const bHardCount = behavioralCount - bEasyCount - bMedCount;

    const behavioralPicks = [
        ...behavioralEasy.slice(0, bEasyCount),
        ...behavioralMedium.slice(0, bMedCount),
        ...behavioralHard.slice(0, Math.max(bHardCount, 1))
    ].slice(0, behavioralCount);

    // Distribute technical questions proportionally by topic
    const matchedTopics = Object.entries(topicScores)
        .sort((a, b) => b[1] - a[1]);
    const totalScore = matchedTopics.reduce((s, [, score]) => s + score, 0);

    const distribution = {};
    let allocated = 0;

    matchedTopics.forEach(([topic, score], i) => {
        const proportion = score / totalScore;
        let count = Math.round(techCount * proportion);
        if (i === matchedTopics.length - 1) {
            count = techCount - allocated;
        }
        count = Math.max(count, 1);
        distribution[topic] = count;
        allocated += count;
    });

    // Adjust remaining if we over/under allocated
    if (allocated > techCount) {
        // Shrink the largest category
        const entries = Object.entries(distribution).sort((a, b) => b[1] - a[1]);
        distribution[entries[0][0]] -= (allocated - techCount);
    }

    const techPicks = [];
    for (const [topic, count] of Object.entries(distribution)) {
        if (count <= 0) continue;
        const pool = questionsData.filter(q => q.topic === topic);
        if (pool.length === 0) continue;

        const shuffled = shuffleArray([...pool]);
        const easy = shuffled.filter(q => q.difficulty === 'Easy');
        const medium = shuffled.filter(q => q.difficulty === 'Medium');
        const hard = shuffled.filter(q => q.difficulty === 'Hard');

        const easyCount = Math.round(count * difficultyMix.easy);
        const mediumCount = Math.round(count * difficultyMix.medium);
        const hardCount = count - easyCount - mediumCount;

        const picks = [
            ...easy.slice(0, easyCount),
            ...medium.slice(0, mediumCount),
            ...hard.slice(0, Math.max(hardCount, 1))
        ].slice(0, count);

        techPicks.push(...picks);
    }

    let allQuestions = shuffleArray([...behavioralPicks, ...techPicks]);

    // Guarantee exact count — pad if short, trim if over
    if (allQuestions.length < totalQuestions) {
        const extras = shuffleArray(questionsData.filter(q => !allQuestions.find(a => a.id === q.id)));
        allQuestions = [...allQuestions, ...extras.slice(0, totalQuestions - allQuestions.length)];
    } else if (allQuestions.length > totalQuestions) {
        allQuestions = allQuestions.slice(0, totalQuestions);
    }

    return allQuestions.map((q, i) => ({ ...q, id: q.id || `bank_${Date.now()}_${i}` }));
}

async function testAIModel() {
    const testBtn = document.getElementById('testModelBtn');
    const status = document.getElementById('modelStatus');
    if (!status || !testBtn) return;

    const model = resumeState.selectedModel;
    const apiKey = (document.getElementById('apiKeyInput')?.value || '').trim();

    testBtn.classList.add('testing');
    testBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';
    status.className = 'model-status testing';
    status.textContent = `Testing ${model}...`;
    delete status.dataset.tested;
    delete status.dataset.valid;

    try {
        // Try server proxy first
        const resp = await fetch('/api/ai/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: 'Reply with exactly one word: OK',
                model,
                apiKey
            })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.error || `Server ${resp.status}`);
        const content = (data.text || '').trim().toUpperCase();
        if (!content.includes('OK')) throw new Error('Unexpected: ' + (data.text || '').slice(0, 50));
    } catch (err) {
        // If server unreachable AND we have an API key, try OpenRouter directly
        if (apiKey) {
            try {
                const orResp = await fetch('https://openrouter.ai/api/v1/chat/completions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${apiKey}`
                    },
                    body: JSON.stringify({
                        model: model,
                        messages: [{ role: 'user', content: 'Reply with exactly one word: OK' }],
                        max_tokens: 50
                    })
                });
                const orData = await orResp.json();
                if (!orResp.ok) throw new Error(orData.error?.message || `OpenRouter ${orResp.status}`);
                const content = (orData.choices?.[0]?.message?.content || '').trim().toUpperCase();
                if (!content.includes('OK')) throw new Error('Unexpected: ' + content.slice(0, 50));
            } catch (orErr) {
                throw new Error(err.message.includes('Failed to fetch')
                    ? 'Server unavailable. Run python3 server.py locally, or check your API key.'
                    : `Server: ${err.message} | Direct: ${orErr.message}`);
            }
        } else {
            throw new Error(err.message.includes('Failed to fetch')
                ? 'Paste your OpenRouter API key above, then try again.'
                : err.message);
        }
    }

    status.className = 'model-status valid';
    status.textContent = `✓ ${model} is working`;
    status.dataset.tested = 'true';
    status.dataset.valid = 'true';

    testBtn.classList.remove('testing');
    testBtn.innerHTML = '<i class="fas fa-plug"></i> Test';
}

async function generateResumeQuestions() {
    const generateBtn = document.getElementById('generateBtn');
    const nameInput = document.getElementById('candidateNameResume');

    resumeState.candidateName = nameInput.value.trim() || resumeState.candidateName || 'Candidate';

    if (!resumeState.text) {
        alert('No resume text extracted. Please upload again.');
        return;
    }

    generateBtn.disabled = true;
    generateBtn.classList.add('loading');
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';

    showResumeStep(3);
    const status = document.getElementById('generationStatus');
    status.style.display = 'flex';
    status.className = 'generation-status';
    status.innerHTML = '<div class="spinner"></div><p>Analyzing resume and preparing questions...</p>';

    document.getElementById('genSummary').style.display = 'none';
    document.getElementById('genQuestions').innerHTML = '';

    try {
        let questions = [];

        if (resumeState.mode === 'bank') {
            status.innerHTML = '<div class="spinner"></div><p>Matching resume skills to question bank...</p>';
            await new Promise(r => setTimeout(r, 400));

            const topicScores = matchTopicsFromResume(resumeState.text);
            questions = selectQuestionsForDuration(topicScores, resumeState.duration, resumeState.experienceYears);

            if (questions.length === 0) {
                const allShuffled = shuffleArray([...questionsData]);
                const count = Math.round(resumeState.duration / 2.5);
                const behavioral = shuffleArray(BUILTIN_BEHAVIORAL_QUESTIONS).slice(0, Math.max(2, Math.round(count * 0.2)));
                questions = shuffleArray([...allShuffled.slice(0, count - behavioral.length), ...behavioral]);
            }
        } else {
            status.innerHTML = '<div class="spinner"></div><p>Generating questions with AI...</p>';
            questions = await generateWithAI(resumeState.text, resumeState.duration, resumeState.experienceYears);
        }

        resumeState.questions = questions;
        resumeState.selected = new Set();

        status.style.display = 'none';
        displayGeneratedQuestions(questions);
        showGeneratedSummary(questions);
    } catch (err) {
        console.error('Generation error:', err);
        status.className = 'generation-status error';
        status.innerHTML = `<i class="fas fa-exclamation-triangle"></i><p>${err.message || 'Failed to generate questions. Please try again.'}</p>`;
    }

    generateBtn.disabled = false;
    generateBtn.classList.remove('loading');
    generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Questions';
}

async function generateWithAI(resumeText, durationMinutes, experienceYears) {
    const questionsCount = Math.round(durationMinutes / 2.5);
    const behevCount = Math.max(2, Math.round(questionsCount * 0.2));
    const techCount = questionsCount - behevCount;
    const expGuide = experienceYears
        ? `The candidate has ~${experienceYears} years of experience. Adjust difficulty accordingly:`
        : 'Adjust difficulty based on the resume content.';

    const prompt = `You are an expert technical interviewer. Based on the following resume, generate ${questionsCount} interview questions.

${expGuide}
- Generate ${techCount} technical questions relevant to the candidate's skills.
- Include ${behevCount} behavioral/situational questions (e.g., teamwork, conflict, leadership, failure, deadlines).

Resume:
${resumeText.slice(0, 4000)}

Each question must have: topic, difficulty (Easy/Medium/Hard), question (real-world scenario), and answer (expected solution).

Return ONLY a valid JSON array. No markdown, no backticks. Example:
[{"topic":"MongoDB","difficulty":"Medium","question":"...","answer":"..."}]`;

    const apiKey = (document.getElementById('apiKeyInput')?.value || '').trim();
    let text = '';

    // Try server proxy first
    try {
        const resp = await fetch('/api/ai/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt, model: resumeState.selectedModel, apiKey })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.error || `Server ${resp.status}`);
        text = data.text || '';
    } catch (serverErr) {
        // Fallback: direct OpenRouter call (works on GitHub Pages with API key)
        if (!apiKey) throw new Error('No OpenRouter API key configured. Add your key in the AI settings.');
        const orResp = await fetch('https://openrouter.ai/api/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: resumeState.selectedModel,
                messages: [{ role: 'user', content: prompt }],
                max_tokens: 4096
            })
        });
        const orData = await orResp.json();
        if (!orResp.ok) throw new Error(orData.error?.message || `OpenRouter ${orResp.status}`);
        text = orData.choices?.[0]?.message?.content || '';
    }

    // Clean response — remove markdown code fences if present
    text = text.replace(/```(?:json)?\s*/gi, '').replace(/```\s*$/g, '').trim();

    let questions;
    try {
        questions = JSON.parse(text);
    } catch {
        // Try extracting JSON array from the text
        const match = text.match(/\[[\s\S]*\]/);
        if (match) {
            try {
                questions = JSON.parse(match[0]);
            } catch {
                throw new Error('AI returned invalid format. Please try again or use Question Bank mode.');
            }
        } else {
            throw new Error('AI returned invalid format. Please try again or use Question Bank mode.');
        }
    }

    if (!Array.isArray(questions) || questions.length === 0) {
        throw new Error('AI returned no questions. Please try again.');
    }

    // Assign IDs and validate structure
    return questions.map((q, i) => ({
        id: `ai_${Date.now()}_${i}`,
        topic: q.topic || 'General',
        difficulty: ['Easy', 'Medium', 'Hard'].includes(q.difficulty) ? q.difficulty : 'Medium',
        question: q.question || '',
        answer: q.answer || ''
    })).filter(q => q.question);
}

function displayGeneratedQuestions(questions) {
    const container = document.getElementById('genQuestions');
    container.innerHTML = '';

    questions.forEach((q, index) => {
        const card = document.createElement('div');
        card.className = 'gen-question-card';
        card.dataset.index = index;

        const difficultyClass = q.difficulty.toLowerCase();
        const topicColor = getTopicColor(q.topic);

        card.innerHTML = `
            <div class="gen-q-header">
                <input type="checkbox" class="gen-q-check" data-index="${index}">
                <span class="gen-q-topic" style="background:${topicColor}22; color:${topicColor}">${escapeHtml(q.topic)}</span>
                <span class="gen-q-difficulty difficulty-badge ${difficultyClass}">${escapeHtml(q.difficulty)}</span>
            </div>
            <div class="gen-q-text">${escapeHtml(latexToPlainText(q.question))}</div>
            <button class="gen-q-toggle">
                <span>Show Solution</span>
                <i class="fas fa-chevron-down"></i>
            </button>
            <div class="gen-q-answer">${escapeHtml(latexToPlainText(q.answer))}</div>
        `;

        // Checkbox toggle
        const checkbox = card.querySelector('.gen-q-check');
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                resumeState.selected.add(index);
                card.classList.add('selected');
            } else {
                resumeState.selected.delete(index);
                card.classList.remove('selected');
            }
        });

        // Solution toggle
        const toggleBtn = card.querySelector('.gen-q-toggle');
        const answerDiv = card.querySelector('.gen-q-answer');
        toggleBtn.addEventListener('click', () => {
            answerDiv.classList.toggle('show');
            toggleBtn.classList.toggle('active');
            toggleBtn.querySelector('span').textContent =
                answerDiv.classList.contains('show') ? 'Hide Solution' : 'Show Solution';
        });

        container.appendChild(card);
        renderMath(card);
    });
}

function showGeneratedSummary(questions) {
    const summary = document.getElementById('genSummary');
    summary.style.display = 'flex';

    document.getElementById('genCandidateName').textContent = resumeState.candidateName;
    document.getElementById('genExperience').textContent = resumeState.experienceYears
        ? `~${resumeState.experienceYears} yrs`
        : 'Exp: N/A';
    document.getElementById('genDuration').textContent = `${resumeState.duration} min`;
    document.getElementById('genQuestionCount').textContent = `${questions.length} questions`;
    document.getElementById('genSource').textContent = resumeState.mode === 'bank' ? 'Question Bank' : 'AI Generated';
}

async function downloadGeneratedQuestions() {
    if (resumeState.questions.length === 0) return;

    const selectedIndices = resumeState.selected.size > 0
        ? [...resumeState.selected]
        : resumeState.questions.map((_, i) => i);

    const selectedData = selectedIndices.map(i => resumeState.questions[i]);

    const { Document, Packer, Paragraph, HeadingLevel, AlignmentType } = docx;

    const children = [];

    // ── SECTION 1: CANDIDATE VIEW (questions only) ──
    children.push(
        new Paragraph({
            text: "INTERVIEW QUESTIONS — CANDIDATE COPY",
            heading: HeadingLevel.HEADING_1,
            alignment: AlignmentType.CENTER
        }),
        new Paragraph({ text: "" }),
        new Paragraph({ text: `Candidate: ${resumeState.candidateName}` }),
        new Paragraph({ text: `Duration: ${resumeState.duration} minutes` }),
        new Paragraph({ text: `Source: ${resumeState.mode === 'bank' ? 'Question Bank' : 'AI Generated'}` }),
        new Paragraph({ text: `Experience: ${resumeState.experienceYears ? `~${resumeState.experienceYears} years` : 'Not specified'}` }),
        new Paragraph({ text: `Total Questions: ${selectedData.length}` }),
        new Paragraph({ text: `Date: ${new Date().toLocaleDateString()}` }),
        new Paragraph({ text: "" }),
        new Paragraph({ text: "Answer the following questions:", heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ text: "" })
    );

    selectedData.forEach((q, i) => {
        children.push(
            new Paragraph({ text: `Question ${i + 1}:`, heading: HeadingLevel.HEADING_3 }),
            new Paragraph({ text: q.question }),
            new Paragraph({ text: "" })
        );
    });

    // ── SECTION 2: INTERVIEWER VIEW (with answers) ──
    children.push(
        new Paragraph({ text: "" }),
        new Paragraph({
            text: "INTERVIEW QUESTIONS — INTERVIEWER COPY",
            heading: HeadingLevel.HEADING_1,
            alignment: AlignmentType.CENTER
        }),
        new Paragraph({ text: "" }),
        new Paragraph({ text: "Full format with topics, difficulty, expected answers.", heading: HeadingLevel.HEADING_2 }),
        new Paragraph({ text: "" })
    );

    selectedData.forEach((q, i) => {
        children.push(
            new Paragraph({ text: `Question ${i + 1}`, heading: HeadingLevel.HEADING_2 }),
            new Paragraph({ text: `Topic: ${q.topic}` }),
            new Paragraph({ text: `Difficulty: ${q.difficulty}` }),
            new Paragraph({ text: "" }),
            new Paragraph({ text: "Question:" }),
            new Paragraph({ text: q.question }),
            new Paragraph({ text: "" }),
            new Paragraph({ text: "Answer:" }),
            new Paragraph({ text: q.answer }),
            new Paragraph({ text: "" })
        );
    });

    const doc = new Document({ sections: [{ properties: {}, children }] });

    const blob = await Packer.toBlob(doc);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Interview_Questions_${resumeState.candidateName.replace(/\s+/g, '_')}.docx`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Register resume feature setup
const origSetup = setupEventListeners;
setupEventListeners = function() {
    origSetup();
    setupResumeFeature();
};