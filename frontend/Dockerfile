# 1. Node.js 환경에서 Vite 앱 실행
FROM node:22.9.0

WORKDIR /app

# 필요한 파일 복사
COPY package.json package-lock.json ./
RUN npm install

# Vite 개발 서버 실행
COPY . .
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
