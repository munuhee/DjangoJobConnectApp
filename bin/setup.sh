#!/bin/bash

echo "🚀 Setting up Jobspeedyup"

echo "🔨 Building Docker image..."
docker build -t jobspeedyup:1.0 .

if [ $? -ne 0 ]; then
  echo "❌ Error: Docker image build failed!"
  exit 1
fi

echo "🚀 Starting Docker containers in detached mode..."
docker run -d -p 8000:8000 jobspeedyup:1.0

if [ $? -ne 0 ]; then
  echo "❌ Error: Docker container failed to start!"
  exit 1
fi

echo "✅ Setup completed successfully!"