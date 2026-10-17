import type { Program } from "./types";

/** DB 연결 전 UI 확인용 더미 데이터 */
export const DUMMY_PROGRAMS: Program[] = [
  {
    id: 1,
    title: "2026 예비창업패키지 모집 공고 (더미)",
    summary:
      "혁신적인 아이디어를 가진 예비창업자를 위한 사업화 지원 프로그램입니다.",
    organization: "창업진흥원",
    category: "지원사업",
    region: "전국",
    targetAudience: "예비창업",
    applyStart: "2026-10-01",
    applyEnd: "2026-11-07",
    status: "open",
    sourceCode: "kstartup",
    sourceUrl: "https://www.k-startup.go.kr",
    collectedAt: "2026-10-17T02:00:00+09:00",
  },
  {
    id: 2,
    title: "AI 스타트업 경진대회 2026 (더미)",
    summary:
      "AI·딥테크 분야 창업팀 대상 전국 경진대회. 우승팀 사업화 자금 지원.",
    organization: "중소벤처기업부",
    category: "경진대회",
    region: "전국",
    targetAudience: "초기창업",
    applyStart: "2026-10-10",
    applyEnd: "2026-10-24",
    status: "open",
    sourceCode: "mss",
    sourceUrl: "https://www.mss.go.kr",
    collectedAt: "2026-10-17T02:00:00+09:00",
  },
  {
    id: 3,
    title: "팁스(TIPS) 연계 창업기업 모집 (더미)",
    summary: "민간 투자와 정부 R&D를 매칭하는 딥테크 창업 지원 트랙.",
    organization: "창업진흥원",
    category: "지원사업",
    region: "전국",
    targetAudience: "초기창업",
    applyStart: "2026-09-01",
    applyEnd: "2026-12-31",
    status: "open",
    sourceCode: "kised",
    sourceUrl: "https://www.kised.or.kr",
    collectedAt: "2026-10-17T02:00:00+09:00",
  },
  {
    id: 4,
    title: "서울 창업허브 입주기업 모집 (더미)",
    summary: "서울 소재 초기 스타트업 대상 입주·멘토링 프로그램.",
    organization: "서울창업허브",
    category: "지원사업",
    region: "서울",
    targetAudience: "초기창업",
    applyStart: "2026-08-01",
    applyEnd: "2026-09-15",
    status: "closed",
    sourceCode: "bizinfo",
    sourceUrl: "https://www.bizinfo.go.kr",
    collectedAt: "2026-10-17T02:00:00+09:00",
  },
];

export const DATA_AS_OF = "2026-10-17";
