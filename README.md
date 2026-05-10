# Interview Questions Bank

A comprehensive web application for generating, managing, and exporting real-world scenario-based interview questions for candidates. Updated with 10,000 detailed questions across all topics.

![Interview Questions Bank](https://via.placeholder.com/800x400?text=Interview+Questions+Bank)

## 🌟 Features

### 1. Question Management
- **6000+ Real-World Scenarios**: Covering MongoDB, Spring Boot, AWS, DSA, Troubleshooting, Kubernetes, and Docker
- **Scenario-Based Questions**: Not direct technical questions - candidates must analyze situations and propose solutions
- **Difficulty Levels**: Easy, Medium, Hard for each topic
- **Search & Filter**: Filter by topic, difficulty, or search keywords

### 2. Question Selection & Export
- **Select Questions**: Checkbox selection on each question card
- **Candidate Name Input**: Enter candidate name before downloading
- **Two View Types**:
  - **Candidate View**: Questions only (for candidate to solve) + Master copy with answers
  - **Interview View**: Full format with topic, difficulty, question, and answer
- **DOCX Export**: Download selected questions as Word document

### 3. User Interface
- **Modern Dark Theme**: Beautiful dark UI with smooth animations
- **Responsive Design**: Works on desktop and mobile
- **Interactive Cards**: Click to reveal solutions
- **Live Statistics**: Shows total questions and topic counts

### 4. Tech Stack
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: Python HTTP Server with DOCX generation
- **Data**: JSON-based question storage

## 📸 Screenshots

### Main Interface
![Main Interface](https://via.placeholder.com/800x400?text=Main+Interface+with+Sidebar+and+Questions)

### Question Selection
![Question Selection](https://via.placeholder.com/800x400?text=Select+Questions+with+Checkboxes)

### Download Modal
![Download Modal](https://via.placeholder.com/800x400?text=Download+Modal+with+Candidate+Name)

### Filter by Topic
![Topic Filters](https://via.placeholder.com/800x400?text=Filter+by+MongoDB+AWS+DSA+etc)

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/shailabsinghha/interview-questions.git
cd interview-questions

# Start the server
python3 server.py

# Open in browser
http://localhost:8000
```

### Usage Flow
1. Open the application in your browser
2. **Filter** questions by topic (MongoDB, Spring Boot, AWS, etc.) or difficulty (Easy, Medium, Hard)
3. **Search** for specific keywords in scenarios
4. **Select** questions using checkboxes on each card
5. Click **Download DOCX** button in the bottom bar
6. Enter **Candidate Name** in the modal
7. Choose **View Type**:
   - Candidate View: Questions only for candidate
   - Interview View: Full format with answers
8. Click **Generate DOCX** to download

## 📊 Question Categories

| Topic | Count |
|-------|-------|
| MongoDB | 1,000 |
| Spring Boot | 1,000 |
| AWS | 1,000 |
| DSA | 1,000 |
| Troubleshooting | 1,000 |
| Kubernetes | 500 |
| Docker | 500 |
| **Total** | **6,000** |

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for automatic deployment:

- **Trigger**: On push to main branch
- **Build**: Validates all files
- **Deploy**: Automatic deployment to GitHub Pages

### Workflow File
```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./
```

## 📁 Project Structure

```
interview-questions/
├── index.html          # Main HTML file
├── styles.css          # CSS styles
├── app.js              # JavaScript logic
├── questions.json      # 6000 questions database
├── server.py           # Python backend server
├── README.md           # This file
└── .github/
    └── workflows/
        └── deploy.yml  # CI/CD workflow
```

## 🎯 Example Questions

### MongoDB
> "Your product search is timing out with millions of documents. Users complain about slow performance during sales. How would you diagnose and fix this?"

### AWS
> "Your website becomes unreachable and all EC2 instances in one AZ show unhealthy status. What happened and how would you restore service?"

### DSA
> "Your sorting algorithm times out on 1 million records. The data is mostly pre-sorted. What approach would work efficiently?"

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is available for personal and professional use.

## 👤 Author

- **GitHub**: [@shailabsinghha](https://github.com/shailabsinghha)

---

## 🌐 Deployment

### GitHub Pages (Static Hosting)
The app is configured for automatic deployment via GitHub Actions:

1. Go to **Settings** → **Pages**
2. Select **Source**: Deploy from a branch
3. Select **Branch**: `gh-pages` (or wait for automatic deployment)
4. Save

**Note**: On GitHub Pages, the download feature works as `.txt` file. For full `.docx` support, run locally with `python3 server.py`.

### Local Development (Full Features)
```bash
python3 server.py
```
Access at: `http://localhost:8000`

---

**Note**: This application works on both static hosting (GitHub Pages - limited download) and local server (full DOCX export). The local Python server provides the complete experience with Word document export.