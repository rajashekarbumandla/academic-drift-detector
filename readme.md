# Academic Drift Detector and Course Rescue System

## Project Overview

In higher education institutions, academic failure usually occurs as a gradual process rather than an abrupt event. Students often show early signs of disengagement such as low attendance, difficulty in specific subjects, and declining assessment scores. However, many academic systems focus only on storing this data and fail to analyze it in a timely manner.

The Academic Drift Detector and Course Rescue System is a rule-based educational platform designed to identify early indicators of academic disengagement at the course level. The system continuously monitors basic academic parameters and applies predefined logical rules to determine academic risk levels and suggest corrective actions.

The platform supports both students and faculty by enabling early awareness and timely intervention. The entire system is implemented without using Artificial Intelligence or Machine Learning. All decisions are derived from transparent, explainable rules, making the system reliable and easy to justify in academic environments.

## Objectives

- Detect early academic disengagement before failure occurs  
- Provide clear and explainable academic risk assessment  
- Enable students to understand their academic standing  
- Help faculty prioritize mentoring and intervention  
- Shift academic monitoring from reactive to preventive  

## Target Users

- Undergraduate students  
- Postgraduate students  
- Faculty members and academic mentors  
- Academic administrators  

## Key Features

- Centralized storage of academic data such as attendance and subject scores  
- Rule-based detection of academic drift  
- Classification of academic status into Stable, Watch List, and At Risk  
- Course-wise performance analysis  
- Personalized rescue recommendations generated using academic rules  
- Separate dashboards for students and faculty  
- Subject-wise heatmaps and performance charts  
- Faculty risk-priority queue for early intervention  
- Downloadable student academic report in CSV format  
- Secure role-based authentication and authorization  

## Rule-Based Drift Logic

Academic drift is evaluated using predefined academic conditions such as:

- Attendance falling below institutional thresholds  
- One or more subjects scoring below minimum acceptable marks  
- Multiple weak subjects increasing overall academic risk  

Each condition contributes to the final drift classification. The logic is deterministic and fully explainable, ensuring transparency and fairness.

## Technology Stack

Backend  
Python with Flask framework  

Database  
SQLite  

Frontend  
HTML with inline CSS and JavaScript  

Visualization  
Chart.js  

Decision Logic  
Pure rule-based conditions without AI or ML  

## Data Source

- Synthetic academic datasets created using SQLite  
- Publicly available datasets adapted for demonstration purposes  
- No real or sensitive student data is used  

## System Workflow

1. Student academic data is stored in the database  
2. Rule-based logic evaluates engagement indicators  
3. Academic drift level is calculated per student and per course  
4. Personalized rescue recommendations are generated  
5. Results are displayed through interactive dashboards  

## Application Modules

Student Module  
Students can register only if their academic record exists in the database. After login, they can view their personal details, subject-wise performance, academic status, heatmaps, triggered drift rules, and personalized rescue plans.

Faculty Module  
Faculty registration is restricted to approved institutional email addresses. Faculty can view all students, access individual student profiles, analyze heatmaps, and view a risk-priority queue to identify students requiring immediate attention.

## Security and Access Control

- Students cannot register as faculty  
- Faculty accounts are validated using approved email addresses  
- Students must exist in the academic database to register  
- Role-based access control ensures secure navigation  

## Installation and Setup

Clone the repository  
git clone https://github.com/your-username/academic-drift-detector.git  

Navigate to project directory  
cd academic-drift-detector  

Install dependencies  
pip install flask  

Initialize the database  
python init_db.py  

Run the application  
python app.py  

Access the application at  
http://127.0.0.1:5000  


Students  
Use any student email generated in the database and register once using that email.

## Project Constraints

- The system is rule-based and does not use predictive models  
- Academic rules are fixed and predefined  
- The project is designed as a functional prototype  

## Expected Impact

- Early identification of academic disengagement  
- Reduction in course failures and dropouts  
- Improved communication between students and faculty  
- Better academic planning and mentoring  

## Conclusion

The Academic Drift Detector and Course Rescue System demonstrates how simple, rule-driven analytics can significantly improve academic outcomes. By focusing on early detection and preventive intervention, the system provides a practical and scalable solution for higher education institutions.

## Disclaimer

This project is developed for educational and hackathon purposes only. All datasets used are synthetic or publicly available. No real student data is involved.
