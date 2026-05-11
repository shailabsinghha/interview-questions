let questionsData = [];
let filteredQuestions = [];
let currentPage = 1;
const questionsPerPage = 15;
let currentTopic = 'all';
let currentDifficulty = 'all';
let searchQuery = '';
let selectedQuestions = new Set();

document.addEventListener('DOMContentLoaded', () => {
    loadQuestions();
    setupEventListeners();
});

async function loadQuestions() {
    try {
        const response = await fetch('questions.json');
        questionsData = await response.json();
        filteredQuestions = [...questionsData];
        updateCounts();
        renderQuestions();
    } catch (error) {
        console.error('Error loading questions:', error);
    }
}

function updateCounts() {
    const counts = {
        all: questionsData.length,
        MongoDB: 0,
        'Spring Boot': 0,
        AWS: 0,
        DSA: 0,
        Troubleshooting: 0,
        Kubernetes: 0,
        Docker: 0,
        'System Design': 0,
        Security: 0,
        Performance: 0
    };

    questionsData.forEach(q => {
        if (counts[q.topic] !== undefined) {
            counts[q.topic]++;
        }
    });

    document.getElementById('totalQuestions').textContent = questionsData.length;
    document.getElementById('countAll').textContent = counts.all;
    document.getElementById('countMongoDB').textContent = counts['MongoDB'];
    document.getElementById('countSpringBoot').textContent = counts['Spring Boot'];
    document.getElementById('countAWS').textContent = counts.AWS;
    document.getElementById('countDSA').textContent = counts.DSA;
    document.getElementById('countTroubleshooting').textContent = counts.Troubleshooting;
    document.getElementById('countKubernetes').textContent = counts.Kubernetes;
    document.getElementById('countDocker').textContent = counts.Docker;
    document.getElementById('countSystemDesign').textContent = counts['System Design'];
    document.getElementById('countSecurity').textContent = counts.Security;
    document.getElementById('countPerformance').textContent = counts.Performance;
    document.getElementById('totalTopics').textContent = '10';
}

function setupEventListeners() {
    const topicFilters = document.querySelectorAll('input[name="topic"]');
    const difficultyFilters = document.querySelectorAll('input[name="difficulty"]');
    const searchInput = document.getElementById('searchInput');
    const clearSearch = document.getElementById('clearSearch');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const resetBtn = document.getElementById('resetFilters');
    const closeModal = document.getElementById('closeModal');
    const clearSelection = document.getElementById('clearSelection');
    const downloadSelected = document.getElementById('downloadSelected');

    topicFilters.forEach(filter => {
        filter.addEventListener('change', (e) => {
            document.querySelectorAll('.filter-option[data-topic]').forEach(opt => {
                opt.classList.toggle('active', opt.dataset.topic === e.target.value);
            });
            currentTopic = e.target.value;
            currentPage = 1;
            applyFilters();
        });
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
                new Paragraph({ text: q.question }),
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
                new Paragraph({ text: `Question: ${q.question}` }),
                new Paragraph({ text: `Answer: ${q.answer}` }),
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
                new Paragraph({ text: q.question }),
                new Paragraph({ text: "" }),
                new Paragraph({ text: "Answer:" }),
                new Paragraph({ text: q.answer }),
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
    filteredQuestions = questionsData.filter(q => {
        const matchesTopic = currentTopic === 'all' || q.topic === currentTopic;
        const matchesDifficulty = currentDifficulty === 'all' || q.difficulty === currentDifficulty;
        const matchesSearch = searchQuery === '' || 
            q.question.toLowerCase().includes(searchQuery) ||
            q.answer.toLowerCase().includes(searchQuery) ||
            q.topic.toLowerCase().includes(searchQuery);
        
        return matchesTopic && matchesDifficulty && matchesSearch;
    });

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
            <span class="topic-badge" data-topic="${q.topic}">${q.topic}</span>
            <span class="difficulty-badge ${difficultyClass}">${q.difficulty}</span>
        </div>
        <div class="card-body">
            <p class="question-text">${q.question}</p>
            <div class="answer-section">
                <button class="toggle-answer">
                    <span>Show Solution</span>
                    <i class="fas fa-chevron-down"></i>
                </button>
                <div class="answer-content">
                    <p>${q.answer}</p>
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
    document.getElementById('modalQuestion').textContent = q.question;
    document.getElementById('modalAnswer').textContent = q.answer;

    modal.classList.add('show');
}