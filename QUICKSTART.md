# 🚀 Quick Start Guide - Solar Farm Optimizer

## For the Impatient 😊

### Windows Users

1. **Double-click `setup.bat`** - This will:
   - Check Python installation
   - Create virtual environment
   - Install all dependencies
   - Generate demo images

2. **Run the dashboard**:
   ```bash
   streamlit run app.py
   ```

3. **Open browser**: http://localhost:8501

4. **Upload demo image**: `demo_data/satellite_sample.png`

5. **Click "🚀 Start Analysis"** and watch the magic! ✨

---

### Linux/Mac Users

1. **Run setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Activate environment** (if not already activated):
   ```bash
   source venv/bin/activate
   ```

3. **Run the dashboard**:
   ```bash
   streamlit run app.py
   ```

4. **Open browser**: http://localhost:8501

5. **Upload demo image**: `demo_data/satellite_sample.png`

6. **Click "🚀 Start Analysis"** and watch the magic! ✨

---

## Manual Setup (If Scripts Don't Work)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate demo images
python demo_data/generate_demo_images.py

# 5. Run dashboard
streamlit run app.py
```

---

## What to Expect

### Processing Time
- **Image Loading**: 1-2 seconds
- **Vision AI Analysis**: 5-10 seconds
- **Optimization**: 3-5 seconds
- **Validation**: 1-2 seconds
- **Total**: ~15-20 seconds

### Output
- ✅ 10 ranked optimal sites
- ✅ Interactive sunlight heatmap
- ✅ Site comparison charts
- ✅ Reality gap analysis
- ✅ Downloadable CSV/Excel reports
- ✅ Interactive map with markers

---

## Dashboard Sections

### 1. Upload & Configure (Sidebar)
- Upload your satellite image (or use demo)
- Set latitude/longitude
- Adjust population size (recommended: 1000)
- Select top N sites (recommended: 10)
- Optional: Upload field validation CSV

### 2. Multi-Agent Status
- See each agent's execution status
- Real-time progress tracking
- Execution time for each phase

### 3. Key Metrics
- Number of sites found
- Average optimization score
- Validation confidence
- Error reduction percentage

### 4. Visualizations
- **Site Map**: Overlay on satellite image
- **Rankings**: Bar charts and tables
- **Sunlight**: Heatmaps and analysis
- **Validation**: Prediction vs reality
- **Report**: Export to CSV/Excel

---

## Tips for Best Results

### 1. Image Quality
- **Recommended**: 1024x1024 pixels
- **Formats**: PNG, JPG, JPEG, TIF
- **Content**: Clear satellite/aerial view
- **Avoid**: Highly clouded or low-resolution images

### 2. Parameters
- Start with **Population Size: 1000**
- Use **Top N: 10** for balanced results
- Increase population for more thorough search (slower)
- Decrease for faster results (less optimal)

### 3. Location
- Set accurate latitude/longitude
- This affects sun position calculations
- Important for sunlight hour predictions

### 4. Field Reports (Optional)
- Upload CSV with actual site measurements
- Enables reality gap analysis
- See `data/field_reports.csv` for format
- Improves validation accuracy

---

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Slow processing
- Reduce population size to 500
- Use smaller images (<1024px)
- Close other applications

### Map not showing
```bash
pip install streamlit-folium
```

### Out of memory
- Reduce population size
- Close other applications
- Use 64-bit Python

---

## Sample Workflow

1. **Upload**: `demo_data/satellite_sample.png`
2. **Set Location**: Lat: 40.7128, Lon: -74.0060 (NYC)
3. **Configure**: Population: 1000, Top N: 10
4. **Start Analysis**: Click button, wait ~15 seconds
5. **View Results**: 
   - Check Multi-Agent Status (all green ✓)
   - See Key Metrics (should show ~0.7-0.8 avg score)
   - Explore Site Map tab
   - Download report from Detailed Report tab

---

## Expected Results

With demo images, you should see:
- **10 candidate sites** identified
- **Average score**: 0.65-0.80
- **Confidence**: 70-85%
- **Error reduction**: 20-30% vs baseline
- **Processing time**: 15-25 seconds

---

## Next Steps

1. ✅ Try with your own satellite images
2. ✅ Experiment with different parameters
3. ✅ Upload field validation data
4. ✅ Export and analyze reports
5. ✅ Integrate with your workflow

---

## Need Help?

- 📖 Read full `README.md`
- 🐛 Check Troubleshooting section
- 🔧 Review configuration in `.env`
- 💡 Start with demo data first

---

## What Makes This Special?

- 🤖 **4 Specialized AI Agents** working together
- 👁️ **Advanced Computer Vision** (segmentation, detection, prediction)
- 🧬 **Genetic Algorithm** optimization
- ✅ **Reality Validation** with gap analysis
- 📊 **Interactive Visualizations** (Plotly + Folium)
- 🎨 **Premium UI** (dark mode, glassmorphism)
- ⚡ **Production-Ready** (error handling, logging, exports)

---

**🎉 Enjoy optimizing solar farms with AI!**

For detailed documentation, see [README.md](README.md)
