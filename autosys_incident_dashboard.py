# Autosys-ServiceNow Incident Analytics Dashboard
# Simplified version for testing

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gradio as gr
from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, func, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from requests.auth import HTTPBasicAuth
import threading
import time
import random
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database Configuration
DATABASE_URL = "sqlite:///autosys_incidents.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class AutosysIncident(Base):
    __tablename__ = "autosys_incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_number = Column(String(50), unique=True, index=True)
    autosys_job_name = Column(String(200), index=True)
    autosys_server = Column(String(100))
    issue_type = Column(String(100), index=True)
    root_cause = Column(String(500), index=True)
    root_cause_category = Column(String(100), index=True)
    severity = Column(String(20))
    priority = Column(String(10))
    state = Column(String(50))
    assigned_to = Column(String(100))
    assignment_group = Column(String(100))
    opened_at = Column(DateTime, index=True)
    closed_at = Column(DateTime)
    resolution_time_hours = Column(Integer)
    short_description = Column(Text)
    description = Column(Text)
    work_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class IncidentPattern(Base):
    __tablename__ = "incident_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    pattern_name = Column(String(200), unique=True)
    root_cause_pattern = Column(String(500))
    incident_count = Column(Integer, default=0)
    first_occurrence = Column(DateTime)
    last_occurrence = Column(DateTime)
    avg_resolution_time = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Create tables
Base.metadata.create_all(bind=engine)

# Sample Data Generator
class SampleDataGenerator:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_sample_data(self, num_incidents: int = 100) -> int:
        """Generate realistic sample Autosys incident data"""
        
        # Sample data
        job_names = [
            'ETL_DAILY_LOAD', 'BATCH_RECONCILIATION', 'DATA_EXPORT_JOB', 'BACKUP_DAILY',
            'REPORT_GENERATION', 'FILE_TRANSFER_JOB', 'DATABASE_CLEANUP', 'INVOICE_PROCESSING'
        ]
        
        servers = [
            'autosys-prod-01', 'autosys-prod-02', 'batch-server-03', 'etl-server-01'
        ]
        
        issue_types = [
            'Job Failure', 'Job Hang/Timeout', 'Scheduling Issue', 'Dependency Issue',
            'Resource Issue', 'Connectivity Issue'
        ]
        
        root_causes = {
            'Infrastructure': ['Server Down', 'Hardware Failure', 'Network Issue', 'Disk Full'],
            'Application': ['Application Error', 'Code Issue', 'Configuration Error'],
            'Database': ['Database Connection Failed', 'SQL Error', 'Table Lock'],
            'External Dependency': ['File Not Found', 'Upstream System Down', 'Third Party Issue']
        }
        
        priorities = ['1 - Critical', '2 - High', '3 - Moderate', '4 - Low']
        states = ['New', 'In Progress', 'On Hold', 'Resolved', 'Closed']
        severities = ['1 - Critical', '2 - High', '3 - Moderate', '4 - Low']
        
        assignment_groups = [
            'Autosys Support', 'Infrastructure Team', 'Database Team', 'Application Support'
        ]
        
        created_count = 0
        
        for i in range(num_incidents):
            # Generate random dates within last 90 days
            opened_date = datetime.now() - timedelta(days=random.randint(0, 90))
            
            # Random chance of being closed
            is_closed = random.choice([True, True, True, False])
            closed_date = None
            resolution_hours = None
            
            if is_closed:
                closed_date = opened_date + timedelta(hours=random.randint(1, 120))
                resolution_hours = int((closed_date - opened_date).total_seconds() / 3600)
            
            # Select random data
            job_name = random.choice(job_names)
            server = random.choice(servers)
            issue_type = random.choice(issue_types)
            
            # Select root cause category and specific cause
            root_cause_category = random.choice(list(root_causes.keys()))
            root_cause = random.choice(root_causes[root_cause_category])
            
            priority = random.choice(priorities)
            state = random.choice(['Resolved', 'Closed']) if is_closed else random.choice(['New', 'In Progress', 'On Hold'])
            severity = random.choice(severities)
            assignment_group = random.choice(assignment_groups)
            assigned_to = f"user{random.randint(1, 100)}@company.com" if random.random() > 0.3 else None
            
            # Generate descriptions
            short_description = f"Autosys job {job_name} failed on {server}"
            description = f"The Autosys job {job_name} running on server {server} encountered {root_cause.lower()}. This resulted in {issue_type.lower()}."
            work_notes = f"Root cause confirmed: {root_cause}. Working on resolution with {assignment_group}."
            
            # Create incident
            incident = AutosysIncident(
                incident_number=f"INC{random.randint(1000000, 9999999)}",
                autosys_job_name=job_name,
                autosys_server=server,
                issue_type=issue_type,
                root_cause=root_cause,
                root_cause_category=root_cause_category,
                severity=severity,
                priority=priority,
                state=state,
                assigned_to=assigned_to,
                assignment_group=assignment_group,
                opened_at=opened_date,
                closed_at=closed_date,
                resolution_time_hours=resolution_hours,
                short_description=short_description,
                description=description,
                work_notes=work_notes
            )
            
            self.db.add(incident)
            created_count += 1
        
        self.db.commit()
        return created_count
    
    def clear_all_data(self):
        """Clear all existing data from tables"""
        self.db.query(IncidentPattern).delete()
        self.db.query(AutosysIncident).delete()
        self.db.commit()
        return "All data cleared successfully"

# FastAPI Application
app = FastAPI(title="Autosys Incident Analytics API", version="1.0.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/sample-data/generate")
async def generate_sample_data(num_incidents: int = 100, db: Session = Depends(get_db)):
    """Generate sample Autosys incident data"""
    try:
        generator = SampleDataGenerator(db)
        count = generator.generate_sample_data(num_incidents)
        return {"message": f"Successfully generated {count} sample incidents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sample data: {str(e)}")

@app.delete("/sample-data/clear")
async def clear_sample_data(db: Session = Depends(get_db)):
    """Clear all sample data"""
    try:
        generator = SampleDataGenerator(db)
        result = generator.clear_all_data()
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing data: {str(e)}")

@app.get("/incidents")
async def get_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get Autosys incidents"""
    incidents = db.query(AutosysIncident).order_by(desc(AutosysIncident.opened_at)).offset(skip).limit(limit).all()
    return incidents

# Dashboard Functions
def create_dashboard():
    def generate_sample_data():
        db = SessionLocal()
        try:
            generator = SampleDataGenerator(db)
            count = generator.generate_sample_data(100)
            return f"✅ Successfully generated {count} sample incidents with realistic data"
        except Exception as e:
            return f"❌ Error generating sample data: {str(e)}"
        finally:
            db.close()
    
    def clear_all_data():
        db = SessionLocal()
        try:
            generator = SampleDataGenerator(db)
            result = generator.clear_all_data()
            return f"✅ {result}"
        except Exception as e:
            return f"❌ Error clearing data: {str(e)}"
        finally:
            db.close()
    
    def get_incidents_data():
        db = SessionLocal()
        try:
            incidents = db.query(AutosysIncident).order_by(desc(AutosysIncident.opened_at)).limit(1000).all()
            
            data = []
            for inc in incidents:
                data.append({
                    'Incident Number': inc.incident_number,
                    'Date': inc.opened_at.strftime('%Y-%m-%d %H:%M') if inc.opened_at else '',
                    'Job Name': inc.autosys_job_name or 'N/A',
                    'Server': inc.autosys_server or 'N/A',
                    'Issue Type': inc.issue_type,
                    'Root Cause': inc.root_cause,
                    'Category': inc.root_cause_category,
                    'Priority': inc.priority,
                    'State': inc.state,
                    'Resolution Hours': inc.resolution_time_hours or 0
                })
            
            return pd.DataFrame(data)
        finally:
            db.close()
    
    def create_root_cause_chart():
        db = SessionLocal()
        try:
            # Get root cause distribution
            causes = db.query(
                AutosysIncident.root_cause,
                func.count(AutosysIncident.id).label('count')
            ).filter(
                AutosysIncident.root_cause != 'Unknown'
            ).group_by(AutosysIncident.root_cause).order_by(desc('count')).limit(15).all()
            
            if not causes:
                return None
            
            df = pd.DataFrame([(c.root_cause, c.count) for c in causes], columns=['Root Cause', 'Count'])
            
            fig = px.bar(df, x='Count', y='Root Cause', orientation='h',
                        title='Top Root Causes of Autosys Incidents',
                        color='Count', color_continuous_scale='viridis')
            fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
            return fig
        finally:
            db.close()
    
    def get_statistics():
        db = SessionLocal()
        try:
            total = db.query(AutosysIncident).count()
            open_count = db.query(AutosysIncident).filter(
                AutosysIncident.state.in_(['New', 'In Progress', 'On Hold'])
            ).count()
            
            avg_resolution = db.query(func.avg(AutosysIncident.resolution_time_hours)).filter(
                AutosysIncident.resolution_time_hours.isnot(None)
            ).scalar() or 0
            
            most_common_cause = db.query(
                AutosysIncident.root_cause,
                func.count(AutosysIncident.id).label('count')
            ).filter(
                AutosysIncident.root_cause != 'Unknown'
            ).group_by(AutosysIncident.root_cause).order_by(desc('count')).first()
            
            return {
                "Total Incidents": total,
                "Open Incidents": open_count,
                "Closed Incidents": total - open_count,
                "Average Resolution Time (hours)": round(avg_resolution, 1),
                "Most Common Root Cause": most_common_cause.root_cause if most_common_cause else "N/A",
                "Most Common Cause Count": most_common_cause.count if most_common_cause else 0
            }
        finally:
            db.close()
    
    # Create Gradio Interface
    with gr.Blocks(title="Autosys Incident Analytics Dashboard", theme=gr.themes.Soft()) as dashboard:
        gr.Markdown("# 🔧 Autosys Incident Analytics Dashboard")
        gr.Markdown("Monitor and analyze Autosys incidents")
        
        with gr.Tab("📊 Overview"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 🔄 Data Management")
                    sample_btn = gr.Button("🎲 Generate Sample Data", variant="secondary")
                    clear_btn = gr.Button("🗑️ Clear All Data", variant="stop")
                    
                    data_output = gr.Textbox(label="Data Operations Status", lines=4)
                
                with gr.Column():
                    gr.Markdown("### 📈 Key Metrics")
                    stats_btn = gr.Button("📈 Get Statistics", variant="secondary")
                    stats_output = gr.JSON(label="System Statistics")
            
            # Button events
            sample_btn.click(generate_sample_data, outputs=data_output)
            clear_btn.click(clear_all_data, outputs=data_output)
            stats_btn.click(get_statistics, outputs=stats_output)
        
        with gr.Tab("📋 Incidents Table"):
            refresh_table_btn = gr.Button("🔄 Refresh Data")
            incidents_table = gr.Dataframe(
                headers=["Incident Number", "Date", "Job Name", "Server", "Issue Type", 
                        "Root Cause", "Category", "Priority", "State", "Resolution Hours"],
                label="Recent Autosys Incidents",
                interactive=False
            )
            refresh_table_btn.click(get_incidents_data, outputs=incidents_table)
        
        with gr.Tab("📊 Root Cause Analysis"):
            root_cause_btn = gr.Button("📊 Generate Root Cause Chart")
            root_cause_plot = gr.Plot(label="Top Root Causes")
            root_cause_btn.click(create_root_cause_chart, outputs=root_cause_plot)
        
        # Load initial data
        dashboard.load(get_statistics, outputs=stats_output)
        dashboard.load(get_incidents_data, outputs=incidents_table)
    
    return dashboard

# Main execution
if __name__ == "__main__":
    import sys
    
    # Check if sample data should be generated
    generate_sample = "--sample" in sys.argv or "-s" in sys.argv
    
    print("Initializing Autosys Incident Analytics System...")
    
    if generate_sample:
        print("Generating sample data...")
        try:
            db = SessionLocal()
            generator = SampleDataGenerator(db)
            generator.clear_all_data()  # Clear any existing data
            sample_count = generator.generate_sample_data(150)  # Generate 150 sample incidents
            print(f"✅ Generated {sample_count} sample incidents")
            db.close()
        except Exception as e:
            print(f"❌ Sample data generation failed: {e}")
    
    # Create and launch dashboard
    dashboard = create_dashboard()
    
    print("\n" + "="*60)
    print("🚀 Autosys Incident Analytics System Started!")
    print("="*60)
    print("🌐 Dashboard: http://localhost:7860")
    print("🔧 API Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("="*60)
    
    # Launch both Gradio and FastAPI
    def launch_gradio():
        dashboard.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    
    # Launch Gradio in a separate thread
    gradio_thread = threading.Thread(target=launch_gradio, daemon=True)
    gradio_thread.start()
    
    # Start FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
