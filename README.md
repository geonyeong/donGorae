# 돈고래 (DonGorae)

한국의 **창업 경진대회·창업지원 사업** 공고와 **프리랜서 개발 일감**을 모아 한눈에 보여주는 웹사이트입니다.  
홈은 창업 공고가 메인이고, 일감은 별도 메뉴입니다. 스타트업 미디어형 UI이며, 로그인 없이 누구나 열람할 수 있습니다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| 웹 | Next.js (App Router) + TypeScript + Tailwind CSS + shadcn/ui |
| DB | MySQL 8 |
| 수집 | Python 3.11+ (httpx, BeautifulSoup) |
| 인프라 | Docker Compose → AWS Lightsail (Ubuntu). 도메인 `dongorae.60fn.com`은 Cloudflare |

## 폴더 구조

```
.
├── web/                 # Next.js 유저 프론트
│   └── src/app/jobs/    # 일감 목록·상세
├── crawler/             # 주간 수집 크롤러
│   ├── sources/         # 창업 공고 파서
│   └── job_sources/     # 일감 파서 (위시켓, 프리모아, 이랜서)
├── db/
│   ├── schema.sql       # MySQL 스키마
│   └── migrations/      # 기존 DB용 변경 (002_jobs.sql)
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

로컬 개발(`npm run dev`)에서 공고 DB 연결이 실패하면 더미 공고로 폴백합니다. 운영 빌드는 더미를 쓰지 않습니다. 일감은 더미가 없고, 수집 전이면 빈 목록입니다.

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

### 일감

화면:

| 경로 | 내용 |
|------|------|
| `/` | 하단 **이번 주 일감** 최대 3개 |
| `/jobs` | 검색, 근무 형태·예산·기술 필터 |
| `/jobs/[id]` | 요약과 원문 링크. 지원 폼 없음 |

데이터는 `programs`와 분리된 `jobs` 테이블입니다. 같은 주간 크롤(`docker compose --profile crawler run --rm crawler`, 일요일 02:00 KST)이 위시켓·프리모아 공개 목록을 함께 넣습니다. 이랜서 목록 API(`api.elancer.co.kr`)는 robots.txt가 수집을 막아, 공개 HTML에 카드가 있을 때만 저장합니다. 로그인 뒤 본문은 수집하지 않습니다.

## 배포 (Lightsail)

GitHub `main` 푸시 후 서버에서 수동 배포합니다. 자동 배포(GitHub Actions)는 아직 없습니다.

```bash
cd ~/donGorae
git pull

set -a
source .env
set +a

# 기존 DB에 jobs 테이블이 없을 때만. 이미 있으면 무시되어도 됩니다.
docker compose exec -T db mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" < db/migrations/002_jobs.sql

docker compose build web
docker compose up -d web
```

확인: `https://dongorae.60fn.com` , `https://dongorae.60fn.com/jobs`

## 브랜딩

- 로고: `web/public/brand/logo.jpg`
- 히어로 비주얼(고래가 돈다발을 뿜는 이미지): `web/public/brand/hero-whale.jpg`
- 톤: 딥 네이비 + 라임 액센트, 미디어형 풀블리드 히어로

## 운영 (AWS Lightsail)

현재 서버: Lightsail Ubuntu, 도메인 `dongorae.60fn.com` (Cloudflare 프록시).  
권장 사양: **2 vCPU / 4GB RAM**. MySQL 3306은 외부에 열지 않습니다.

웹 코드 변경 후에는 `docker compose build web && docker compose up -d web`이 필요합니다. 이미지가 빌드 시점의 페이지를 포함합니다.

크론 예 (서버 타임존이 UTC일 때, 일요일 02:00 KST):

```cron
0 17 * * 6 cd /home/ubuntu/donGorae && /usr/bin/docker compose --profile crawler run --rm crawler >> /home/ubuntu/crawl.log 2>&1
```

## 수동 체크리스트

- [ ] `/` 히어로·로고·브랜드 이미지 표시
- [ ] `/programs` 검색·필터·목록
- [ ] `/programs/[id]` 상세·원문 링크
- [ ] 헤더 **일감**, `/jobs` 검색·필터, `/jobs/[id]` 원문 링크
- [ ] 홈 하단 이번 주 일감 (데이터 없으면 안내 문구)
- [ ] 푸터에 데이터 기준일 표시 (공고·일감 중 최근 수집일)
- [ ] `docker compose up -d db` 후 크롤 → 목록에 실데이터 반영

## 라이선스 / 데이터

공고·일감 원문은 각 출처 사이트에 귀속됩니다. 본 서비스는 메타데이터 요약·원문 링크 제공을 목적으로 합니다.
