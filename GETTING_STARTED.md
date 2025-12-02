# 🎯 GETTING STARTED - Solar Farm Optimizer

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.11 or higher installed
- [ ] pip package manager
- [ ] 4GB+ RAM available
- [ ] Internet connection (for package downloads)
- [ ] ~3GB free disk space (for dependencies)

Check Python version:
```bash
python --version
# Should show 3.11.0 or higher
```

---

## 🚀 Installation Methods

### Method 1: Automated Setup (Recommended)

**Windows:**
```bash
# Double-click setup.bat or run:
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

This will automatically:
1. ✅ Check Python version
2. ✅ Create virtual environment
3. ✅ Install all dependencies
4. ✅ Generate demo images
5. ✅ Create .env file

---

### Method 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies (takes 5-10 min)
pip install -r requirements.txt

# 5. Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 6. Generate demo images
python demo_data/generate_demo_images.py
```

---

## ✅ Verify Installation

Run the test script:
```bash
python test_installation.py
```

You should see:
```
✓ Python 3.11+ (OK)
✓ All core packages installed
✓ Project structure verified
✓ All agents imported successfully
✓ All vision modules imported successfully
✓ Utilities imported successfully
✓ Found demo image(s)
✓ Agent status check: 4 agents ready
```

---

## 🎮 Running the Application

### Option 1: Web Dashboard (Interactive)

```bash
streamlit run app.py
```

Then open your browser to: http://localhost:8501

**What you'll see:**
1. Upload interface in sidebar
2. Configuration options
3. "Start Analysis" button
4. Real-time progress tracking
5. Interactive results with multiple tabs

---

### Option 2: Command Line Demo

```bash
python run_demo.py
```

**What you'll see:**
- Console output with progress
- Agent execution times
- Top 5 site recommendations
- Validation metrics
- Exported CSV file

---

## 📝 First Analysis Walkthrough

### Step 1: Launch Dashboard
```bash
streamlit run app.py
```

### Step 2: Upload Image
- Click "Upload Satellite Image" in sidebar
- Select `demo_data/satellite_sample.png`
- Wait for preview to appear

### Step 3: Configure Parameters
- **Latitude**: 40.7128 (New York)
- **Longitude**: -74.0060
- **Population Size**: 1000 (recommended)
- **Top N Sites**: 10

### Step 4: Start Analysis
- Click "🚀 Start Analysis" button
- Watch progress bar (4 phases)
- Wait ~15-20 seconds

### Step 5: Explore Results

**Multi-Agent Status:**
- See all 4 agents completed
- Check execution times

**Key Metrics:**
- Number of sites found
- Average scores
- Confidence levels
- Error reduction

**Site Map Tab:**
- Satellite image with overlays
- Interactive Folium map
- Color-coded rankings

**Rankings Tab:**
- Comparison charts
- Detailed table
- Score breakdowns

**Sunlight Analysis Tab:**
- Annual hours heatmap
- Terrain segmentation
- Obstacle detection

**Validation Tab:**
- Reality gap charts
- Confidence gauge
- Recommendations

**Detailed Report Tab:**
- Full data table
- Download CSV
- Download Excel

---

## 🎯 Understanding the Results

### Site Scores (0-1 scale)
- **0.8-1.0**: Excellent site
- **0.6-0.8**: Good site
- **0.4-0.6**: Fair site
- **0.0-0.4**: Poor site

### Score Components
1. **Sunlight** (40%): Annual sunlight hours
2. **Terrain** (25%): Land suitability
3. **Obstacles** (20%): Clearance from buildings/trees
4. **Accessibility** (10%): Road access, slope
5. **Cost** (5%): Economic efficiency

### Confidence Levels
- **>75%**: High confidence
- **50-75%**: Medium confidence
- **<50%**: Low confidence (needs field validation)

---

## 🔧 Troubleshooting Common Issues

### Issue: "streamlit: command not found"
**Solution:**
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Issue: "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Dashboard won't start
**Solution:**
```bash
# Check if port 8501 is in use
# Try different port:
streamlit run app.py --server.port 8502
```

### Issue: Out of memory
**Solution:**
- Reduce population size to 500
- Close other applications
- Use smaller images

### Issue: Processing too slow
**Solution:**
- Reduce population size
- Reduce image resolution
- Check CPU usage

---

## 📚 Next Steps

### Beginner
1. ✅ Run with demo images
2. ✅ Explore all dashboard tabs
3. ✅ Download and review CSV report
4. ✅ Try different parameters

### Intermediate
1. Upload your own satellite images
2. Customize coordinates for your location
3. Upload field validation data
4. Compare results across different images

### Advanced
1. Modify optimization weights in code
2. Add new terrain classes
3. Integrate real APIs (GEE, OSM)
4. Customize visualization themes

---

## 🎓 Learning Resources

### Understanding the Code
- `agents/` - Multi-agent system logic
- `vision/` - Computer vision pipeline
- `utils/` - Helper functions
- `app.py` - Streamlit dashboard

### Key Concepts
- **Genetic Algorithms**: Optimization technique
- **Computer Vision**: Image analysis
- **Multi-Agent Systems**: Collaborative AI
- **Geospatial Analysis**: Map data processing

### Documentation
- `README.md` - Complete documentation
- `QUICKSTART.md` - Quick instructions
- `PROJECT_SUMMARY.md` - Project overview
- Code comments - Inline explanations

---

## 💡 Tips for Best Results

### Image Quality
- ✅ Use high-resolution images (1024x1024+)
- ✅ Clear visibility (no heavy clouds)
- ✅ Satellite/aerial view (not ground level)
- ✅ Recent imagery (for accuracy)

### Configuration
- ✅ Start with default parameters
- ✅ Increase population for better results
- ✅ Use accurate coordinates
- ✅ Provide field data when available

### Analysis
- ✅ Review all tabs before deciding
- ✅ Check confidence scores
- ✅ Read recommendations
- ✅ Export data for further analysis

---

## 🆘 Getting Help

### Self-Help Resources
1. Read error messages carefully
2. Check `README.md` troubleshooting section
3. Verify installation with `test_installation.py`
4. Review configuration in `.env`

### Common Solutions
- Restart virtual environment
- Reinstall dependencies
- Clear browser cache (for Streamlit)
- Check disk space
- Update Python to 3.11+

---

## ✨ Success Checklist

After following this guide, you should be able to:

- [ ] Install all dependencies successfully
- [ ] Launch the Streamlit dashboard
- [ ] Upload and process demo images
- [ ] View multi-agent execution status
- [ ] Explore all visualization tabs
- [ ] Download CSV/Excel reports
- [ ] Understand site scores and recommendations
- [ ] Run command-line demo
- [ ] Troubleshoot common issues

---

## 🎉 You're Ready!

If all checkboxes above are checked, you're ready to:
1. Process your own satellite imagery
2. Optimize solar farm placement
3. Export professional reports
4. Make data-driven decisions

**Happy optimizing! ☀️**

---

For detailed documentation, see [README.md](README.md)  
For quick reference, see [QUICKSTART.md](QUICKSTART.md)  
For project overview, see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
