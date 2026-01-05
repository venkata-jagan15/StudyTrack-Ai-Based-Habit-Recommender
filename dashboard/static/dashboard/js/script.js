/**
 * Core Logic for AI Study Habit Recommender
 */

// Colors
const colors = {
    primary: '#6366f1',
    secondary: '#ec4899',
    accent: '#8b5cf6',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    text: '#94a3b8'
};

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

function initApp() {
    // Check which page we are on
    const bodyId = document.body.id;

    if (bodyId === 'student-dashboard') {
        initStudentDashboard();
    } else if (bodyId === 'teacher-dashboard') {
        initTeacherDashboard();
    }
}

// Student Dashboard Logic
function initStudentDashboard() {
    console.log("Initializing Student Dashboard...");


    // Form Handling
    // Form Handling
    // document.getElementById('habit-form').addEventListener('submit', (e) => {
    //    // Allow default submission to backend
    // });
}

// Teacher Dashboard Logic
function initTeacherDashboard() {
    console.log("Initializing Teacher Dashboard...");

    // Fetch Real Data from Script Tag
    let students = [];
    try {
        const dataScript = document.getElementById('student-data');
        if (dataScript) {
            students = JSON.parse(dataScript.textContent);
        }
    } catch (e) {
        console.error("Error parsing student data:", e);
    }

    // If no data (e.g. fresh db), fall back to empty or mock? 
    // Let's rely on real data. If empty, charts will be empty.

    // Process Data for Charts
    const highPerformers = [];
    const avgPerformers = [];
    const lowPerformers = [];

    const riskCounts = { 'High': 0, 'Medium': 0, 'Low': 0, 'Safe': 0 }; // 'Safe' maps to Low usually, but let's see model defaults

    // Histogram bins
    const gradeBins = [0, 0, 0, 0, 0, 0, 0]; // 0-40, 41-50, ... 91-100

    students.forEach(s => {
        // Scatter Plot Data
        const point = { x: s.study, y: s.score };

        // Categorize for Cluster Chart based on ML Cluster ID
        // Cluster 0: "Increase study hours" -> Likely Low/Risk (Red)
        // Cluster 1: "Good balance" -> Likely Success (Green)
        // Cluster 2: "Focus on sleep" -> Likely Warning (Yellow)

        if (s.cluster === 1) highPerformers.push(point);
        else if (s.cluster === 2) avgPerformers.push(point);
        else lowPerformers.push(point); // Cluster 0 and any fallback

        // Risk Counts
        // Model uses 'High', 'Medium', 'Low' (safe is default but 'Low' is text)
        // Adjust for any mismatch
        let risk = s.risk;
        if (risk === 'Safe') risk = 'Low';
        if (riskCounts[risk] !== undefined) riskCounts[risk]++;

        // Histogram
        const score = s.score;
        if (score <= 40) gradeBins[0]++;
        else if (score <= 50) gradeBins[1]++;
        else if (score <= 60) gradeBins[2]++;
        else if (score <= 70) gradeBins[3]++;
        else if (score <= 80) gradeBins[4]++;
        else if (score <= 90) gradeBins[5]++;
        else gradeBins[6]++;
    });

    // 1. Cluster Chart (Scatter Plot)
    const ctxCluster = document.getElementById('teacher-cluster-chart').getContext('2d');
    new Chart(ctxCluster, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'High Performers (Balanced)',
                    data: highPerformers,
                    backgroundColor: colors.success,
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Needs Sleep Optimization',
                    data: avgPerformers,
                    backgroundColor: colors.warning,
                    pointRadius: 6,
                    pointHoverRadius: 8
                },
                {
                    label: 'Needs Improvement',
                    data: lowPerformers,
                    backgroundColor: colors.danger,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }
            ]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: { display: true, text: 'Daily Study Hours', color: colors.text },
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: colors.text }
                },
                y: {
                    title: { display: true, text: 'Predicted Test Score (%)', color: colors.text },
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: colors.text }
                }
            },
            plugins: {
                legend: { labels: { color: '#f8fafc' } }
            }
        }
    });

    // 2. Risk Distribution (Doughnut Chart)
    const ctxRisk = document.getElementById('teacher-risk-chart').getContext('2d');
    new Chart(ctxRisk, {
        type: 'doughnut',
        data: {
            labels: ['Low/Safe Risk', 'Moderate Risk', 'High Risk'],
            datasets: [{
                data: [riskCounts['Low'] + riskCounts['Safe'], riskCounts['Medium'], riskCounts['High']],
                backgroundColor: [colors.success, colors.warning, colors.danger],
                borderWidth: 0
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#f8fafc' } }
            }
        }
    });

    // 3. Grade Distribution (Histogram)
    const ctxHist = document.getElementById('teacher-histogram-chart').getContext('2d');
    new Chart(ctxHist, {
        type: 'bar', // A bar chart with categoryPercentage 1.0 looks like a histogram
        data: {
            labels: ['0-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100'],
            datasets: [{
                label: 'Student Count',
                data: gradeBins,
                backgroundColor: colors.primary,
                barPercentage: 1.0,
                categoryPercentage: 1.0,
                borderWidth: 1,
                borderColor: colors.surface
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: colors.text, stepSize: 1 } },
                x: { grid: { display: false }, ticks: { color: colors.text } }
            },
            plugins: { legend: { display: false } }
        }
    });

    // 4. Class Weakness Analysis (Polar Area) - Real Data
    const ctxPolar = document.getElementById('teacher-polar-chart').getContext('2d');
    new Chart(ctxPolar, {
        type: 'polarArea',
        data: {
            labels: ['Sleep Deprivation (< 6h)', 'Low Assignments (< 5)', 'Social Media Overuse (> 3h)', 'High Risk Students', 'Low Study Hours (< 2h)'],
            datasets: [{
                label: 'Flagged Cases',
                data: [
                    students.filter(s => s.sleep < 6).length,
                    students.filter(s => s.assignments < 5).length,
                    students.filter(s => s.social > 3).length,
                    students.filter(s => s.risk === 'High').length,
                    students.filter(s => s.study < 2).length
                ],
                backgroundColor: [
                    'rgba(236, 72, 153, 0.5)',
                    'rgba(245, 158, 11, 0.5)',
                    'rgba(16, 185, 129, 0.5)',
                    'rgba(99, 102, 241, 0.5)',
                    'rgba(148, 163, 184, 0.5)'
                ],
                borderWidth: 1,
                borderColor: colors.surface
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                r: {
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    ticks: { display: false, backdropColor: 'transparent' }
                }
            },
            plugins: {
                legend: { position: 'right', labels: { color: colors.text, font: { size: 11 } } }
            }
        }
    });

}

// Helper: Generate Random Data ensuring it stays within logical bounds
function generateClusterData(count, ranges) {
    // ... not needed much anymore but keeping for reference if needed
    return [];
}

// Teacher Dashboard View Switcher
function switchTeacherView(viewType) {
    const classView = document.getElementById('class-view');
    const indView = document.getElementById('individual-view');
    const btnClass = document.getElementById('btn-class-view');
    const btnInd = document.getElementById('btn-individual-view');

    if (viewType === 'class') {
        classView.classList.remove('hidden');
        indView.classList.add('hidden');

        btnClass.classList.replace('btn-secondary', 'btn-primary');
        btnInd.classList.replace('btn-primary', 'btn-secondary');
    } else {
        classView.classList.add('hidden');
        indView.classList.remove('hidden');

        btnClass.classList.replace('btn-primary', 'btn-secondary');
        btnInd.classList.replace('btn-secondary', 'btn-primary');
    }
}

// Download Report - Real CSV Download
function downloadReport() {
    let students = [];
    try {
        const dataScript = document.getElementById('student-data');
        if (dataScript) students = JSON.parse(dataScript.textContent);
    } catch (e) { console.error("No data for report"); return; }

    if (!students.length) {
        alert("No student data available to download.");
        return;
    }

    // CSV Header
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Student ID,Name,Study Hours,Sleep Hours,Assignments,Social Media,Predicted Score,Risk Level,Cluster Group\r\n";

    // CSV Rows
    students.forEach(s => {
        const row = [
            s.id,
            s.name,
            s.study,
            s.sleep || 0,
            s.assignments || 0,
            s.social || 0,
            s.score,
            s.risk,
            s.cluster === 1 ? "Balanced" : (s.cluster === 2 ? "Sleep Focus" : "Needs Improvement")
        ].join(",");
        csvContent += row + "\r\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    const date = new Date().toISOString().slice(0, 10);
    link.setAttribute("download", `Class_Analytics_Report_${date}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
