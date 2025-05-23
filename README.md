# 🛣️ Asphalt Aid - AI Smart Road Issue Reporting System

## 📋 Project Overview

**Asphalt Aid** is a graduation project that revolutionizes how road infrastructure issues are reported and managed. This intelligent system enables citizens to easily report road problems like potholes, cracks, and other road damages while leveraging AI technology to automatically assess the severity of each issue.

The platform helps administrative authorities prioritize road maintenance work based on AI-determined severity levels, ensuring that the most critical issues are addressed first, leading to more efficient resource allocation and improved road safety.

## ✨ Key Features

### 🔐 **User Management**
- **User Registration & Authentication**: Secure signup with required fields (first name, last name, email)
- **Profile Management**: Users can update their personal information
- **Password Security**: Django's built-in password validators ensure strong passwords
- **Token-based Authentication**: Secure API access using authentication tokens

### 📊 **Report Management**
- **Create Reports**: Users can report road issues with descriptions, addresses, and images
- **AI-Powered Severity Assessment**: Automatic severity analysis (Low/Medium/High) using machine learning
- **Report Types**: Support for potholes, cracks, road sinks, and other road issues
- **Update Restrictions**: Users can only modify static fields (description, address, name) to maintain data integrity
- **Ownership Control**: Users can only view and modify their own reports

### 🤖 **AI Integration**
- **Image Analysis**: Advanced machine learning model analyzes uploaded images
- **Severity Classification**: Automatic assignment of severity levels (1-3 scale)
- **Real-time Processing**: Immediate analysis upon image upload
- **Fallback Handling**: Graceful error handling if AI analysis fails

### 🔒 **Security & Performance**
- **API Throttling**: Rate limiting to prevent abuse
- **Pagination**: Efficient data loading with customizable page sizes
- **Error Handling**: Comprehensive error responses with detailed messages
- **Data Protection**: Secure handling of user data and reports

## 🛠️ Technology Stack

### **Backend (Current Repository)**
- **Framework**: Django 5.1.7 with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Token-based authentication
- **AI/ML**: Custom pothole classification model
- **Task Queue**: Celery with Redis
- **Documentation**: Swagger/OpenAPI with drf-yasg
- **Containerization**: Docker & Docker Compose

### **Frontend**
- **Repository**: [Asphalt Aid Frontend](https://github.com/munasserr/asphalt-aid-frontend)
- **Setup Instructions**: Refer to the Next.js frontend repository's README for detailed setup and running instructions

## 🚀 Getting Started

### Prerequisites

Before running this project, make sure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Usually comes with Docker Desktop
- **Git**: For cloning the repository

### 📥 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/munasserr/asphalt-aid
   cd asphalt-aid
   ```

2. **🚨 CRITICAL: Download AI Model Files**
   
   ⚠️ **THE APPLICATION WILL NOT WORK WITHOUT THIS STEP!** ⚠️
   
   Due to GitHub's file size limitations (100MB per file), the AI model files are hosted separately and must be downloaded manually:
   
   **Download Link**: [Pothole Classification Model Files](https://drive.google.com/file/d/1UkAC-GLx3z7tcibHfAA-e3_wB9VRMZX7/view?usp=sharing)
   
   **Installation Steps:**
   ```bash
   # 1. Download the zip file from the Google Drive link above
   # 2. Extract the "Pothole Classification" folder from the zip
   # 3. Place it in your project root directory
   
   # Your project structure should look like this:
   asphalt-aid/
   ├── Pothole Classification/     # ← This folder with AI model
   │   └── pothole_model.h5       # ← Essential AI model file
   ├── asphalt_aid/
   ├── reports_app/
   └── ...
   ```
   
   **Why is this necessary?**
   - The AI model file (`pothole_model.h5`) is approximately 91MB
   - GitHub has a strict 100MB file size limit
   - Without this model, the AI severity prediction feature will fail
   - Reports can still be created, but without intelligent severity assessment
   
   **Verification:**
   ```bash
   # Verify the model file exists
   ls -la "Pothole Classification/pothole_model.h5"
   # You should see the file listed
   ```

3. **Environment Setup**
   ```bash
   # The project uses Docker, so no local Python environment setup is needed
   # All dependencies are handled in the Docker containers
   ```

4. **Build and Run with Docker**
   ```bash
   # Build and start all services
   docker compose up --build

   # Or run in detached mode
   docker compose up -d --build
   ```

5. **Initialize the Database**
   ```bash
   # Run database migrations
   docker compose exec django-web python manage.py migrate

   # Create a superuser for admin access
   docker compose exec django-web python manage.py createsuperuser
   ```

6. **Verify AI Model is Working**
   ```bash
   # Check Docker logs for AI model loading
   docker compose logs django-web | grep "model"
   
   # You should see:
   # "✓ Pothole classification model loaded successfully"
   ```

7. **Load Sample Data (Optional)**
   ```bash
   # You can create sample reports using the API or admin interface
   ```

### 🔗 **Access Points**

Once the application is running, you can access:

- **API Base URL**: `http://localhost:8000/api`
- **Admin Interface**: `http://localhost:8000/admin`
- **API Documentation (Swagger)**: `http://localhost:8000/swagger/`
- **API Documentation (ReDoc)**: `http://localhost:8000/redoc/`

## 🤖 AI Model Information

The AI model for pothole classification is located in the **"Pothole Classification"** folder. This machine learning model:

- **Purpose**: Analyzes uploaded images to determine road issue severity
- **Input**: Image files (JPEG, PNG)
- **Output**: Severity level (0: No Issue, 1: Low, 2: Medium, 3: High)
- **Technology**: Custom trained model for pothole and road damage detection
- **Integration**: Automatically triggered when users upload images with reports
- **Size**: ~91MB (too large for GitHub, hosted on Google Drive)

**Model Download**: [https://drive.google.com/file/d/1UkAC-GLx3z7tcibHfAA-e3_wB9VRMZX7/view?usp=sharing](https://drive.google.com/file/d/1UkAC-GLx3z7tcibHfAA-e3_wB9VRMZX7/view?usp=sharing)

## 📱 Frontend Application

To use the complete Asphalt Aid system, you'll need to run the frontend application as well:

**Frontend Repository**: [https://github.com/munasserr/asphalt-aid-frontend](https://github.com/munasserr/asphalt-aid-frontend)

Please refer to the frontend repository's README file for detailed instructions on how to set up and run the frontend application.

## 📚 API Documentation

### **Main Available Endpoints**

#### **Authentication**
- `POST /api/users/auth/signup/` - User registration
- `POST /api/users/auth/signin/` - User login

#### **User Profile**
- `GET /api/users/profile/` - Get user profile
- `PUT /api/users/profile/update/` - Update user profile
- `POST /api/users/change-password/` - Change password

#### **Reports**
- `GET /api/reports/reports/` - List user's reports (paginated)
- `POST /api/reports/reports/` - Create new report (with AI analysis)
- `GET /api/reports/reports/{id}/` - Get specific report
- `PATCH /api/reports/reports/{id}/` - Update report (limited fields)
- `DELETE /api/reports/reports/{id}/` - Delete report

## 🔧 Development

### **Project Structure**
```
asphalt-aid/
├── asphalt_aid/          # Main Django project
├── reports_app/          # Reports management app
├── users_app/            # User management app
├── ai_service/           # AI integration service
├── Pothole Classification/ # AI model files (will look like that when you download separately)
├── media/                # User uploaded files
├── docker-compose.yml    # Docker services configuration
├── Dockerfile           # Django app container
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### **Adding New Features**
1. Create new apps using `docker compose exec django-web python manage.py startapp <app_name>`
2. Add new models, views, and serializers as needed
3. Update URL configurations
4. Run migrations: `docker compose exec django-web python manage.py makemigrations && docker compose exec django-web python manage.py migrate`


## 🆘 Troubleshooting

### **Common Issues**

#### **AI Model Not Working**
```bash
# Symptoms: Reports created but severity always shows default value
# Solution: 
1. Verify model file exists: ls -la "Pothole Classification/pothole_model.h5"
2. Check Docker logs: docker compose logs django-web | grep -i "model\|error"
3. Re-download from Google Drive if file is missing/corrupted
```

#### **Application Won't Start**
```bash
# Check if all services are running
docker compose ps

# View logs for errors
docker compose logs django-web
docker compose logs redis
```

#### **Docker Issues**
```bash
# Rebuild containers
docker compose down
docker compose up --build

# Clear Docker cache if needed
docker system prune -a
```

### **Getting Help**

If you encounter any issues:

1. Review the API documentation at `/swagger/`
2. Ensure Docker is running properly
3. Verify all services are up: `docker compose ps`
4. **Most importantly**: Ensure the AI model files are downloaded and placed correctly

## 🎯 Future Enhancements

- **Mobile Application**: Native mobile app for easier reporting
- **Advanced Analytics**: Dashboard for administrators with statistics
- **Real-time Notifications**: Push notifications for report status updates
- **Geographic Integration**: Enhanced mapping and location services
- **Machine Learning Improvements**: Continuous model training and improvement

---
