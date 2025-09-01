const express = require('express');
const os = require('os');
const app = express();
const port = process.env.PORT || 3000;

// Get configuration from environment variables
const config = {
  NODE_ENV: process.env.NODE_ENV || 'development',
  LOG_LEVEL: process.env.LOG_LEVEL || 'info',
  APP_NAME: process.env.APP_NAME || 'Kubernetes Hello World',
  VERSION: process.env.VERSION || '1.0.0'
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: Math.floor(process.uptime()),
    environment: config.NODE_ENV
  });
});

// Main application endpoint
app.get('/', (req, res) => {
  const hostname = os.hostname();
  const platform = os.platform();
  const arch = os.arch();
  const uptime = Math.floor(os.uptime() / 60);
  const freemem = Math.round(os.freemem() / 1024 / 1024);
  const totalmem = Math.round(os.totalmem() / 1024 / 1024);
  const cpus = os.cpus().length;
  
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${config.APP_NAME}</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
                font-size: 2.5rem;
            }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }
            .info-card {
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .info-card h3 {
                margin: 0 0 10px 0;
                font-size: 1.2rem;
            }
            .info-card p {
                margin: 0;
                font-size: 1.5rem;
                font-weight: bold;
            }
            .status {
                text-align: center;
                margin: 20px 0;
                padding: 10px;
                background: rgba(76, 175, 80, 0.3);
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 ${config.APP_NAME}</h1>
            <div class="status">
                ✅ Application is running successfully in Kubernetes!
            </div>
            
            <div class="info-grid">
                <div class="info-card">
                    <h3>Hostname</h3>
                    <p>${hostname}</p>
                </div>
                <div class="info-card">
                    <h3>Platform</h3>
                    <p>${platform}</p>
                </div>
                <div class="info-card">
                    <h3>Architecture</h3>
                    <p>${arch}</p>
                </div>
                <div class="info-card">
                    <h3>Uptime</h3>
                    <p>${uptime} min</p>
                </div>
                <div class="info-card">
                    <h3>Memory Free</h3>
                    <p>${freemem} MB</p>
                </div>
                <div class="info-card">
                    <h3>Memory Total</h3>
                    <p>${totalmem} MB</p>
                </div>
                <div class="info-card">
                    <h3>CPU Cores</h3>
                    <p>${cpus}</p>
                </div>
                <div class="info-card">
                    <h3>Environment</h3>
                    <p>${config.NODE_ENV}</p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; opacity: 0.8;">
                <p>Timestamp: ${new Date().toISOString()}</p>
                <p>Version: ${config.VERSION}</p>
            </div>
        </div>
    </body>
    </html>
  `);
});

// Start the server
app.listen(port, () => {
  console.log(`🚀 ${config.APP_NAME} v${config.VERSION} running on port ${port}`);
  console.log(`📊 Environment: ${config.NODE_ENV}`);
  console.log(`🔍 Log Level: ${config.LOG_LEVEL}`);
  console.log(`⏰ Started at: ${new Date().toISOString()}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 Received SIGTERM, shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 Received SIGINT, shutting down gracefully...');
  process.exit(0);
});

