# AGENTS.md

> 이 파일은 Cursor, Claude Code 등 AI 코딩 에이전트가 이 프로젝트에서 작업할 때
> 자동으로 읽는 "프로젝트 설명서"입니다. 프로젝트 루트에 두세요.

---

## 1. 프로젝트 개요

- **프로젝트명**: 돈고래 (DonGorae)
- **목적**: 한국의 창업 경진대회·창업지원 사업 공고와 프리랜서 개발 일감을 수집해 보여주는 웹사이트. 홈은 창업 공고가 메인, 일감은 `/jobs`
- **핵심 사용자**: 예비창업자·초기창업자·대학생 등 창업 정보를 찾는 일반 사용자 (초기 버전은 로그인 없이 열람)
- **현재 단계**: 개발 중 (MVP)
- **톤**: 스타트업 미디어형 (비주얼·히어로 강조). 정부 포털 UI 금지

## 2. 기술 스택

| 구분 | 내용 |
|---|---|
| 언어/런타임 | Node.js 20+, TypeScript / Python 3.11+ |
| 프레임워크 | Next.js (App Router) — 유저 웹 / Python — 주간 수집 크롤러 |
| DB/ORM | MySQL 8 (초기 ORM 없이 `mysql2` 또는 Prisma — 도입 시 이 문서 갱신) |
| 스타일링 | Tailwind CSS + shadcn/ui |
| 테스트 | 없음 (수동 체크리스트로 대체) |
| 배포 | Docker Compose → AWS Lightsail Ubuntu. 도메인 `dongorae.60fn.com` (Cloudflare). 배포는 서버에서 `git pull` 후 `docker compose build web && docker compose up -d web` |
| 패키지 매니저 | npm (web) / pip + requirements.txt (crawler) |

## 3. 폴더 구조

```
.
├── web/                        # Next.js 유저 프론트 (App Router)
│   ├── src/app/                # 페이지·레이아웃·API
│   ├── src/components/         # UI 컴포넌트
│   ├── src/lib/                # DB·유틸
│   └── public/
├── crawler/                    # Python 주간 수집기
│   ├── sources/                # 공고 파서 (kstartup, bizinfo, kised, mss)
│   ├── job_sources/            # 일감 파서 (wishket, freemoa, elancer)
│   ├── normalize.py / upsert.py
│   ├── job_normalize.py / upsert_jobs.py
│   └── main.py
├── db/
│   ├── schema.sql              # 신규 볼륨용 스키마
│   └── migrations/             # 기존 DB 변경 (002_jobs.sql)
├── docker-compose.yml
├── .env.example
└── AGENTS.md
```

### 작업 시 빠른 안내

| 목적 | 주로 보는 경로 |
|---|---|
| URL·페이지 | `web/src/app/` |
| UI 컴포넌트 | `web/src/components/` |
| DB 접속·쿼리 | `web/src/lib/` |
| DB 스키마 | `db/schema.sql` |
| 공고 파서 | `crawler/sources/` |
| 일감 파서 | `crawler/job_sources/` |
| 기존 DB 변경 | `db/migrations/` |
| 환경변수 | `.env`, `.env.example`, `docker-compose.yml` |

## 4. 코딩 컨벤션

### 4.1 공통 규칙

- 모든 API 응답은 `{ success, data, error }` 형태로 통일
- 변수/함수명은 영어, 주석은 한국어로 작성
- 커밋되지 않은 디버깅 코드(`console.log`, `print` 등) 금지 — 확인 후 반드시 제거
- 새 라이브러리 추가 전, 기존 의존성에 유사 기능이 있는지 확인
- 코딩 스타일은 유지보수성을 위해 직관적이고 단순하게 작성

### 4.2 `web/` (Next.js)

- 코딩 스타일: TypeScript strict, ESLint (Next 기본)
- 네이밍: 컴포넌트 `PascalCase`, 함수/변수 `camelCase`, 상수 `UPPER_SNAKE_CASE`
- DB 접근: `web/src/lib/`에서만. Raw SQL 사용 시 반드시 파라미터 바인딩, 문자열 이어붙이기 금지
- 서버 컴포넌트 우선, 상호작용 필요한 부분만 Client Component
- UI: Tailwind + shadcn/ui. 자체 CSS는 히어로·브랜드 강조에만 최소 사용

### 4.3 `crawler/` (Python)

- PEP 8, 타입 힌트 권장
- 소스별 파서는 `crawler/sources/`에 모듈로 분리
- HTTP 요청 시 User-Agent 명시, 요청 간격 준수, robots.txt 존중
- DB upsert는 prepared statement / 파라미터 바인딩만 사용

## 5. 보안 필수 규칙

- **SQL Injection 방지**: 파라미터 바인딩/ORM 필수. 사용자 입력을 쿼리 문자열에 직접 삽입 금지
- **XSS 방지**: React 기본 이스케이프 활용. `dangerouslySetInnerHTML` 사용 시 반드시 sanitize
- **CSRF**: 초기 MVP는 공개 읽기 전용. 상태 변경 API 추가 시 CSRF/Origin 검증 적용
- **민감정보**: DB 비밀번호·API 키 하드코딩 금지 — `.env` 사용, `.env`는 git 제외
- **크롤링 윤리**: 원문 무단 전문 복제 최소화, `source_url`로 원문 링크 제공

## 6. 아키텍처 원칙 (관심사 분리)

- 뷰(컴포넌트)에는 DB 쿼리 직접 삽입 금지 — `lib/` 계층에서만 DB 접근
- 크롤러와 웹은 프로세스/컨테이너 분리 (크롤 실패가 웹을 죽이지 않게)
- 수집 주기: **7일(주 1회)**. 실시간 크롤링 금지
- 함수가 대략 50줄 이상이면 분리 전 계획을 먼저 공유
- 중복 코드를 발견해도 바로 대규모 리팩토링하지 말고 10번 절차를 따를 것

## 7. 에러 처리 & 로깅

- 운영 환경에서 스택 트레이스·쿼리문을 사용자에게 노출하지 않기
- Next.js: 서버 로그 / Python crawler: stdout + `crawl_runs` 테이블에 실행 결과 기록
- 새 로깅 체계를 임의로 도입하지 말고, 필요 시 먼저 질문

## 8. 테스트 정책

### 8.2 테스트가 없는 프로젝트 (최소 안전장치)

- 코드 수정 후 관련 페이지/기능을 수동 점검할 체크리스트를 간단히 제시
- DB 스키마 변경은 사전에 알리고 백업 여부 확인 후 진행
- 파일 삭제·대규모 리팩토링 시 영향 파일/기능 목록을 함께 보고

## 9. 코드 스타일 예시 (Good / Bad)

```ts
// ❌ Bad — 쿼리 문자열에 입력값 직접 삽입
const rows = await db.query(`SELECT * FROM programs WHERE id = ${id}`);

// ✅ Good — 파라미터 바인딩
const rows = await db.query("SELECT * FROM programs WHERE id = ?", [id]);
```

```ts
// ❌ Bad — API 응답 형식 제각각
return NextResponse.json({ ok: true, result: items });

// ✅ Good — 통일 응답
return NextResponse.json({ success: true, data: items, error: null });
```

```python
# ❌ Bad — 요청 폭주·차단 유발
for url in urls:
    fetch(url)

# ✅ Good — 간격 + UA
for url in urls:
    time.sleep(3)
    fetch(url, headers={"User-Agent": USER_AGENT})
```

## 10. AI 에이전트가 반드시 지킬 규칙

- 파일을 삭제하거나 대규모로 리팩토링하기 전, 먼저 계획을 요약해서 알려줄 것
- 확신이 없는 사항은 임의로 결정하지 말고 질문할 것
- `git push`는 개발자 요청 또는 승인 없이는 절대 금지
- 1차 공고 소스: K-Startup, 기업마당(bizinfo), 창업진흥원(kised), 중기부(mss) — 신규 소스 추가 전 공유
- 일감은 `jobs` 테이블과 `/jobs`만 사용. `programs`에 컬럼을 섞지 말 것. 등록된 일감 소스는 위시켓·프리모아·이랜서이고, 주기는 공고와 같은 주 1회다. 새 사이트를 넣기 전 이용약관·소스 확정을 물을 것. 로그인 뒤 본문 수집 금지. robots.txt가 막는 API는 호출하지 말 것
- UI는 스타트업 미디어형 유지. 보라 그라데이션·크림+세리프 등 흔한 AI 기본 룩 지양

---

## 11. Git 커밋 규칙 (AI 자동 커밋용)

> 참고: 사용자가 커밋을 명시적으로 요청했을 때만 커밋한다. (평소에는 코드만 수정)

### 11.1 커밋 시점

- 하나의 논리적 단위가 완료될 때마다 커밋
- 목적이 다른 변경사항을 한 커밋에 섞지 않기
- 커밋 메시지 제목 앞에 `(Cursor ai)` 를 추가

### 11.2 커밋 메시지 형식 (Conventional Commits)

```
<type>(<scope>): <제목>

<본문 - 무엇을, 왜 변경했는지>
```

| type | 설명 |
|---|---|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `refactor` | 동작 변화 없는 코드 구조 개선 |
| `style` | 포맷팅 등 스타일 변경 |
| `docs` | 문서 수정 |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드·설정·의존성 |
| `perf` | 성능 개선 |

### 11.5 주의사항

- `git push`, `git reset --hard`, `git rebase` 등은 사용자 승인 후 실행
- `.env`, `node_modules`, `__pycache__`, 빌드 산출물은 `.gitignore`에 포함
- 커밋 메시지 제목은 50자 이내

---

## 12. 프로젝트별 추가 규칙

- 서비스명·브랜드: **돈고래 (DonGorae)** — 히어로에서 브랜드가 최상위 시그널
- 호스팅: **AWS Lightsail** + Cloudflare (`dongorae.60fn.com`). 스키마 변경은 `db/migrations/`를 기존 DB에 적용
- MVP: 로그인/회원/지원 폼 없음 — 추가 전 설계 공유
- 데이터 기준일은 푸터에 표시. 공고·일감 `collected_at` 중 최근 값
- 수집은 주 1회 cron (`docker compose --profile crawler run --rm crawler`)
