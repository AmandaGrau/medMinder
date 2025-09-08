
# 💊 medMinder

> **Prescription Management with Security-First Design**

medMinder is a comprehensive prescription tracking application engineered using secure development practices and modern web application architecture. Originally developed as a capstone project at **HackBright Academy**, this project has evolved to incorporate cybersecurity best practices and serves as a demonstration of full-stack development with security-conscious design.

<div align=center>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)

</div>

---

## ⚠️ Important Notice

**Disclaimer**: This application should not be used for actual prescription management. Always consult a healthcare professional for medical advice.

- 🚫 **Not for Production Use** - This application is in active development as a portfolio and learning project
- 🔒 **Security Learning Platform** - Used to explore and implement cybersecurity concepts
- 👨‍💻 **Portfolio Project** - Showcases full-stack development and security knowledge

---

## 📱 Screenshots

<table width="100%" align="center">
<tr>

<td width="50%" align="center">

> **medMinder Home**

<img src="static/img/medMinder-home.png" 
	alt="Mobile view" 
	width="100%"
	style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-height: 663px; max-width: 605px;
	oject-fit: cover;"/>

<div align=center>

> **Prescription Dashboard Overview**

<img src="static/img/dashboard.png" 
	alt="Full screen view" 
	width="100%"
	style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-height: 663px; max-width: 605px;
	oject-fit: cover;"/>

<div align=center>

> **Medication Search**

<img src="static/img/med-search.png" 
	alt="Full screen view" 
	width="100%"
	style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-height: 663px; max-width: 605px;
	oject-fit: cover;"/>

</div>

<div align=center>

> **Refill Scheduling Form**

<img src="static/img/refill-form.png" 
	alt="Full screen view" 
	width="100%"
	style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-height: 663px; max-width: 605px;
	oject-fit: cover;"/>

</div>

<div align=center>

> **Prescription Calendar**

<img src="static/img/calendar.png" 
	alt="Full screen view" 
	width="100%"
	style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-height: 663px; max-width: 605px;
	oject-fit: cover;"/>

</div>

> **Mobile Responsive**

<img src="static/img/mobile.png" 
	alt="Full screen view" 
	width="100%"
	style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-height: 663px; max-width: 605px;
	oject-fit: cover;"/>

</div>

</td>
</tr>
</table>

---

## Features

### 🔐 **Security & Authentication**
- **Multi-Factor Authentication (MFA)** - TOTP-based 2FA implementation using PyOTP
- **Secure Password Handling** - Bcrypt hashing with salt for password storage
- **Session Security** - Secure session management with automatic timeout
- **Input Validation & Sanitization** - Protection against common web vulnerabilities
- **CSRF Protection** - Cross-site request forgery prevention
- **SQL Injection Prevention** - Parameterized queries and ORM best practices
- **Secure Headers** - Implementation of security headers for XSS protection

### 💊 **Application Features**
- **Prescription Database Integration** - Search and manage medication information
- **Medication Tracking** - Add, edit, and delete prescriptions with validation
- **Dosage & Schedule Management** - Complex medication timing and frequency tracking
- **Refill Monitoring** - Automated tracking of prescription refill dates

### 📅 **Calendar & Scheduling**
- **FullCalendar Integration** - Visual medication schedule management
- **Interactive Date Management** - Drag-and-drop schedule adjustments
- **Event Color Coding** - Visual differentiation of medication types and urgency

### 🎨 **Modern Web Development**
- **Responsive Design** - Mobile-first approach with Bootstrap framework
- **Modern UI/UX** - Glassmorphism design principles and smooth animations
- **Progressive Enhancement** - Graceful degradation for accessibility
- **Clean Architecture** - MVC pattern with separation of concerns

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript ES6+ |
| **Backend** | Python 3.8+, Flask 2.0+, Jinja2 |
| **Database** | PostgreSQL 13+ |
| **Security** | Flask-Login, Werkzeug (password hashing), PyOTP (2FA), Flask-WTF (CSRF protection) |
| **Authentication** | TOTP Multi-Factor Authentication, Secure Session Management |
| **Libraries** | FullCalendar.js, Font Awesome, Custom CSS Framework |
| **Development** | Git, Virtual Environment, Requirements.txt |
| **Security Tools** | Input validation, SQL injection prevention, XSS protection |

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** ([Download Python](https://www.python.org/downloads/))
- **PostgreSQL 13+** ([Download PostgreSQL](https://www.postgresql.org/download/))
- **Git** ([Download Git](https://git-scm.com/downloads))

### Installation

1. **Clone the repsository**
    ```bash
    git clone https://github.com/AmandaGrau/medMinder
    cd medMinder
    ```

2. **Set up virtual environment** (Recommended)
	```bash
	# Create virtual environment
	python3 -m venv venv

	# Activate virtual environment on macOS/Linux:
	source venv/bin/activate

	# Activate virtual environment on Windows:
	venv\Scripts\activate
	```

3. **Install dependencies**
	```bash
	pip install -r requirements.txt 
	```

4. **Database Setup**
	```bash
	# Create PostgreSQL database
	createdb prescriptions
   
	# Or using PostgreSQL CLI:
	psql -U postgres
	CREATE DATABASE prescriptions;
	\q
	```

5. **Environment Configuration**
	```bash
	# Create environment file
	cp .env.example .env

	# Edit .env with your database credentials
	nano .env
	```

	Example `.env` file:
	```env
	DATABASE_URL=postgresql://username:password@localhost/prescriptions
	SECRET_KEY=your-secret-key-here
	FLASK_ENV=development
	```

6. **Initialize Database**
	```bash
	python3 -c "from model import db; db.create_all()"
	```

7. **Start the application**
	```bash
	python3 server.py
	```

8. **Access the application**
	Open your browser and navigate to **http://localhost:5000**

---

## 🔧 Configuration

### Database Configuration

Update your database connection in `model.py`:

```python
# For local development
DATABASE_URL = "postgresql://username:password@localhost/prescriptions"

# For production
DATABASE_URL = os.environ.get('DATABASE_URL')
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://localhost/prescriptions` |
| `SECRET_KEY` | Flask secret key for sessions | Required |
| `FLASK_ENV` | Flask environment | `production` |
| `PORT` | Application port | `5000` |

---

## 🆕 Project Evolution

**Current Status**: *Active development as a portfolio and learning project*

### From Software Engineering to Cybersecurity
medMinder began as a **Hackbright Academy capstone project** and has since evolved into a portfolio demonstration of secure development practices. Following the completion of **CompTIA Security+** certification, this project has been enhanced to showcase cybersecurity knowledge applied to web application development.

### Recent Security Enhancements
-  **Multi-Factor Authentication** - Implemented TOTP-based 2FA following NIST guidelines
-  **Security Headers** - Added comprehensive security headers (CSP, HSTS, etc.)
-  **Input Validation** - Enhanced input sanitization and validation mechanisms
-  **Session Security** - Improved session management with secure configuration
-  **Password Security** - Upgraded password hashing and storage practices
-  **Vulnerability Assessment** - Regular security reviews and improvements

### Development & Learning Focus
-  **Security-First Mindset** - Every feature developed with security considerations
-  **Code Quality** - Clean, maintainable code following security best practices  
-  **Documentation** - Comprehensive documentation for security implementations
-  **Continuous Learning** - Platform for exploring new security technologies

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Database Connection Issues
```bash
# Error: "database 'prescriptions' does not exist"
createdb prescriptions

# Error: "role 'username' does not exist"
createuser -s username

# Error: "password authentication failed"
# Update your .env file with correct credentials
```

#### Python/Flask Issues
```bash
# Error: "ModuleNotFoundError"
pip install -r requirements.txt

# Error: "Port already in use"
# Kill existing process or change port
lsof -ti:5000 | xargs kill -9
# Or change port in server.py
```

#### 2FA Setup Issues
```bash
# Error: "Invalid QR code"
# Ensure PyOTP is installed correctly
pip install pyotp qrcode[pil]

# Clear browser cache and try again
```

#### Development Issues
```bash
# Clear Flask cache
export FLASK_ENV=development
# Or delete __pycache__ folders
find . -name "__pycache__" -exec rm -rf {} +
```

---

## 🙏 Acknowledgments

- **[Hackbright Academy](https://hackbrightacademy.com/)** - For providing the foundational software engineering education that started this journey
- **[CompTIA](https://www.comptia.org/)** - For the Security+ certification program that shaped the security implementations in this project
- **Hackbright Instructors** - Thank you for excellent guidance and patience during the original capstone development
- **Fellow Bootcamp Alumni** - Many thanks to my cohort for the humorous memes, kind support, and collaborative learning experiences
- **Cybersecurity Community** - For resources, best practices, and continuous learning opportunities
- **Open Source Community** - For tools, libraries, and security best practices

---
 
<div align="center">

Created by **Amanda Grau**                              
*Cybersecurity Professional & Software Engineer*



<div align="center">

[![Email](https://img.shields.io/badge/Email-EA580C?style=for-the-badge&logo=gmail&logoColor=white)](mailto:agrau.dev@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-1E3A8A?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/amandargrau)
[![GitHub](https://img.shields.io/badge/GitHub-0F172A?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AmandaGrau)

##
<div align="center">

This project is licensed under the MIT License - see the [LICENSE](docs/LICENSE) file for details.