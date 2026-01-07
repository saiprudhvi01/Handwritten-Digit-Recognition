# 🚀 Deployment Guide

## 📋 Prerequisites

- Python 3.10 or higher
- All dependencies from `requirements.txt`
- Pre-trained model `cnn.hdf5`

## 🐳 Docker Deployment (Recommended)

### Quick Start
```bash
# Clone the repository
git clone <your-repo-url>
cd Deep-Learning-MNIST---Handwritten-Digit-Recognition-master

# Build and run with Docker Compose
docker-compose up --build
```

### Production Deployment
```bash
# Set production environment
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key

# Run with Docker Compose (production profile)
docker-compose --profile production up -d
```

## 🖥️ Manual Deployment

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
```

### 3. Run with Gunicorn
```bash
gunicorn --workers 4 --bind 0.0.0.0:8000 wsgi:application
```

## 🌐 Cloud Deployment

### Render.com
1. Connect your GitHub repository to Render
2. Set environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
3. Render will automatically detect the Dockerfile
4. Deploy with automatic builds

### Heroku
1. Create `Procfile`:
```
web: gunicorn --workers 4 --bind 0.0.0.0:$PORT wsgi:application
```
2. Deploy to Heroku
3. Set config vars in Heroku dashboard

### AWS EC2
```bash
# Clone and setup
git clone <your-repo>
cd <project-folder>
pip install -r requirements.txt

# Run with supervisor
sudo apt-get install supervisor
sudo systemctl start gunicorn
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: `development` or `production`
- `SECRET_KEY`: Secret key for sessions
- `MODEL_PATH`: Path to the CNN model file

### Model Requirements
- TensorFlow 2.10+ compatible
- Keras 2.10+ included
- OpenCV for image processing
- NumPy for array operations

## 📊 Performance

### Recommended Specs
- **CPU**: 2+ cores
- **RAM**: 4GB+ minimum
- **Storage**: 10GB+ for model and uploads
- **Network**: Stable internet for MNIST downloads

### Scaling
- **Single Instance**: Handles ~100 concurrent users
- **Multiple Workers**: Scale with `--workers N`
- **Load Balancer**: Use Nginx for multiple instances

## 🔒 Security

### Production Checklist
- [ ] Set strong SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Enable CSRF protection
- [ ] Set up file upload limits
- [ ] Configure CORS if needed
- [ ] Use environment variables for secrets

## 🐛 Troubleshooting

### Common Issues
1. **Model not found**: Ensure `cnn.hdf5` is in the correct path
2. **Permission denied**: Check file permissions for uploads folder
3. **Memory errors**: Reduce batch size or increase RAM
4. **Port conflicts**: Change port in docker-compose.yml

### Health Checks
```bash
# Test locally
curl http://localhost:5000/

# Test in Docker
docker-compose exec digit-recognition curl http://localhost:5000/
```

## 📈 Monitoring

### Logs
```bash
# Docker logs
docker-compose logs -f digit-recognition

# Gunicorn logs
gunicorn --access-logfile - --error-logfile - wsgi:application
```

### Metrics to Monitor
- Response time
- Error rate
- Memory usage
- CPU usage
- Request queue length

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Render
      uses: johnbeynon/render-action@v0.0.6
      with:
        service-id: ${{ secrets.RENDER_SERVICE_ID }}
        api-key: ${{ secrets.RENDER_API_KEY }}
```

## 📞 Support

For deployment issues:
1. Check logs: `docker-compose logs`
2. Verify model compatibility
3. Test with different TensorFlow versions
4. Ensure all environment variables are set

## 🎯 Success Criteria

✅ Application loads without errors
✅ Model loads successfully  
✅ All endpoints respond correctly
✅ File uploads work
✅ Predictions return results
✅ Static files serve properly
✅ Health checks pass
