# 돈고래 (DonGorae)

한국의 **창업 경진대회·창업지원 사업** 공고를 모아 한눈에 보여주는 웹사이트입니다.  
스타트업 미디어형 UI로, 로그인 없이 누구나 열람할 수 있습니다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| 웹 | Next.js (App Router) + TypeScript + Tailwind CSS + shadcn/ui |
| DB | MySQL 8 |
| 수집 | Python 3.11+ (httpx, BeautifulSoup) |
| 인프라 | Docker Compose → 네이버 클라우드(NCP) Ubuntu VM |

## 폴더 구조

```
.
├── web/                 # Next.js 유저 프론트
├── crawler/             # 주간 수집 크롤러
├── db/schema.sql        # MySQL 스키마·시드
├── docker-compose.yml
├── AGENTS.md            # AI/개발 원칙
└── README.md
```

## 로컬 실행

### 1) DB 기동

```bash
# Docker Desktop 실행 후
cp .env.example .env
docker compose up -d db
```

### 2) 웹

```bash
cd web
cp ../.env.example .env.local   # DATABASE_HOST=127.0.0.1
npm install
npm run dev
```

→ http://localhost:3000

DB에 연결되지 않으면 더미 데이터로 UI가 표시됩니다.

### 3) 크롤러 (주 1회 기준)

```bash
cd crawler
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

DATABASE_HOST=127.0.0.1 \
DATABASE_USER=dongorae \
DATABASE_PASSWORD=dongorae \
DATABASE_NAME=dongorae \
python main.py
```

Docker로 실행:

```bash
docker compose --profile crawler run --rm crawler
```

## 수집 소스 (1차)

| code | 사이트 | 비고 |
|------|--------|------|
| kstartup | K-Startup | 점검 중이면 스킵 |
| bizinfo | 기업마당 | 창업 관련 키워드 필터 |
| kised | 창업진흥원 | 보드 장애 시 스킵 |
| mss | 중소벤처기업부 | 창업·스타트업 관련 필터 |

수집 주기: **7일 (주 1회)**. 실시간 크롤링하지 않습니다.

## 브랜딩

- 로고: `web/public/brand/logo.jpg`
- 히어로 비주얼(고래가 돈다발을 뿜는 이미지): `web/public/brand/hero-whale.jpg`
- 톤: 딥 네이비 + 라임 액센트, 미디어형 풀블리드 히어로

## 운영 (NCP)

권장 VM: **2 vCPU / 4GB RAM / 50GB+ SSD**, Ubuntu 22.04+

```bash
docker compose up -d db web
# cron 예시 (매주 일요일 02:00)
# 0 2 * * 0 cd /path/to/donGorae && docker compose --profile crawler run --rm crawler
```

## 수동 체크리스트

- [ ] `/` 히어로·로고·브랜드 이미지 표시
- [ ] `/programs` 검색·필터·목록
- [ ] `/programs/[id]` 상세·원문 링크
- [ ] 푸터에 데이터 기준일 표시
- [ ] `docker compose up -d db` 후 크롤 → 목록에 실데이터 반영

## 라이선스 / 데이터

공고 원문은 각 기관 사이트에 귀속됩니다. 본 서비스는 메타데이터 요약·원문 링크 제공을 목적으로 합니다.
