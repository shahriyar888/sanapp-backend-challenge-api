# Platform-Specific Setup Guide

Choose your operating system below for tailored setup instructions.

## 🪟 Windows Setup

### Prerequisites
- [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- [Python 3.11+](https://www.python.org/downloads/)
- [Git for Windows](https://git-scm.com/download/win)

### Installation Steps

1. **Install Docker Desktop**
   - Download and install Docker Desktop
   - Start Docker Desktop
   - Verify: `docker --version`

2. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd sannap_project
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Development Environment**
   ```bash
   dev.bat setup
   ```

5. **Start Django**
   ```bash
   python manage.py runserver
   ```

6. **Access Application**
   - Django: http://localhost:8000
   - MinIO: http://localhost:9001

### Common Windows Issues

**Issue: "docker-compose is not recognized"**
```bash
# Solution: Restart Docker Desktop and terminal
```

**Issue: "Port already in use"**
```bash
# Check what's using the port
netstat -ano | findstr :5432

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Issue: "Permission denied"**
```bash
# Run terminal as Administrator
```

---

## 🐧 Linux Setup

### Prerequisites
- Docker Engine
- Docker Compose
- Python 3.11+
- Git

### Installation Steps (Ubuntu/Debian)

1. **Install Docker**
   ```bash
   # Update package index
   sudo apt-get update
   
   # Install Docker
   sudo apt-get install docker.io docker-compose
   
   # Add user to docker group
   sudo usermod -aG docker $USER
   
   # Log out and back in, then verify
   docker --version
   ```

2. **Install Python**
   ```bash
   sudo apt-get install python3.11 python3-pip python3-venv
   ```

3. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd sannap_project
   ```

4. **Make Scripts Executable**
   ```bash
   chmod +x dev.sh prod.sh
   ```

5. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Setup Development Environment**
   ```bash
   ./dev.sh setup
   ```

7. **Start Django**
   ```bash
   python manage.py runserver
   ```

8. **Access Application**
   - Django: http://localhost:8000
   - MinIO: http://localhost:9001

### Common Linux Issues

**Issue: "Permission denied" when running docker**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in
```

**Issue: "Port already in use"**
```bash
# Check what's using the port
sudo lsof -i :5432

# Kill the process
sudo kill -9 <PID>
```

**Issue: "Cannot connect to Docker daemon"**
```bash
# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker
```

---

## 🍎 macOS Setup

### Prerequisites
- [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- Python 3.11+ (via Homebrew)
- Git (pre-installed or via Xcode)

### Installation Steps

1. **Install Homebrew** (if not installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Docker Desktop**
   - Download and install Docker Desktop for Mac
   - Start Docker Desktop
   - Verify: `docker --version`

3. **Install Python**
   ```bash
   brew install python@3.11
   ```

4. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd sannap_project
   ```

5. **Make Scripts Executable**
   ```bash
   chmod +x dev.sh prod.sh
   ```

6. **Install Python Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

7. **Setup Development Environment**
   ```bash
   ./dev.sh setup
   ```

8. **Start Django**
   ```bash
   python3 manage.py runserver
   ```

9. **Access Application**
   - Django: http://localhost:8000
   - MinIO: http://localhost:9001

### Common macOS Issues

**Issue: "Port already in use"**
```bash
# Check what's using the port
lsof -i :5432

# Kill the process
kill -9 <PID>
```

**Issue: "Permission denied" on scripts**
```bash
# Make scripts executable
chmod +x dev.sh prod.sh
```

**Issue: "Python command not found"**
```bash
# Use python3 instead of python
python3 manage.py runserver

# Or create an alias
echo "alias python=python3" >> ~/.zshrc
source ~/.zshrc
```

---

## 🔧 Development Workflow (All Platforms)

### Daily Development

1. **Start Services**
   - Windows: `dev.bat start`
   - Linux/macOS: `./dev.sh start`

2. **Run Django**
   ```bash
   python manage.py runserver
   ```

3. **Make Changes**
   - Edit code
   - Django auto-reloads

4. **Run Tests**
   ```bash
   pytest
   ```

5. **Stop Services** (when done)
   - Windows: `dev.bat stop`
   - Linux/macOS: `./dev.sh stop`

### Production Testing

1. **Build Production**
   - Windows: `prod.bat build`
   - Linux/macOS: `./prod.sh build`

2. **Run Migrations**
   ```bash
   # Windows
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   
   # Linux/macOS
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   ```

3. **Access Application**
   - http://localhost

4. **Stop Production**
   - Windows: `prod.bat stop`
   - Linux/macOS: `./prod.sh stop`

---

## 🎯 Quick Command Reference

### Windows
| Task | Command |
|------|---------|
| Setup | `dev.bat setup` |
| Start Dev | `dev.bat start` |
| Stop Dev | `dev.bat stop` |
| Start Prod | `prod.bat build` |
| View Logs | `dev.bat logs` |
| Clean | `dev.bat clean` |

### Linux/macOS
| Task | Command |
|------|---------|
| Setup | `./dev.sh setup` |
| Start Dev | `./dev.sh start` |
| Stop Dev | `./dev.sh stop` |
| Start Prod | `./prod.sh build` |
| View Logs | `./dev.sh logs` |
| Clean | `./dev.sh clean` |

---

## 📚 Next Steps

After setup:
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) for detailed information
2. Check [TEST_README.md](TEST_README.md) for testing guide
3. Bookmark [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for daily use
4. Create a superuser: `python manage.py createsuperuser`
5. Access admin panel: http://localhost:8000/admin

---

## 🆘 Getting Help

### Check Logs
- Windows: `dev.bat logs`
- Linux/macOS: `./dev.sh logs`

### Verify Services
```bash
docker ps
```

### Clean Start
- Windows: `dev.bat clean` then `dev.bat setup`
- Linux/macOS: `./dev.sh clean` then `./dev.sh setup`

### Documentation
- [README.md](README.md) - Overview
- [DEVELOPMENT.md](DEVELOPMENT.md) - Detailed setup
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference
- [TEST_README.md](TEST_README.md) - Testing guide
