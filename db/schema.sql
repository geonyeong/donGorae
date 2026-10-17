-- 돈고래 (DonGorae) MySQL 스키마
-- 문자셋: utf8mb4

SET NAMES utf8mb4;
SET time_zone = '+09:00';

CREATE DATABASE IF NOT EXISTS dongorae
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE dongorae;

-- 수집 대상 소스
CREATE TABLE IF NOT EXISTS sources (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  code VARCHAR(32) NOT NULL COMMENT 'kstartup, bizinfo, kised, mss',
  name VARCHAR(100) NOT NULL,
  base_url VARCHAR(500) NOT NULL,
  enabled TINYINT(1) NOT NULL DEFAULT 1,
  last_success_at DATETIME NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_sources_code (code)
) ENGINE=InnoDB;

-- 공고/지원사업
CREATE TABLE IF NOT EXISTS programs (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(500) NOT NULL,
  summary TEXT NULL,
  organization VARCHAR(200) NULL,
  category VARCHAR(50) NULL COMMENT '경진대회, 지원사업, 교육 등',
  region VARCHAR(100) NULL,
  target_audience VARCHAR(200) NULL COMMENT '예비창업, 초기, 대학생 등',
  apply_start DATE NULL,
  apply_end DATE NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'open' COMMENT 'upcoming, open, closed',
  source_code VARCHAR(32) NOT NULL,
  source_url VARCHAR(1000) NOT NULL,
  external_id VARCHAR(200) NULL COMMENT '원문의 고유 ID',
  content_hash CHAR(64) NULL COMMENT '중복/변경 감지용',
  content_md MEDIUMTEXT NULL,
  collected_at DATETIME NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_programs_source_url (source_url(500)),
  KEY idx_programs_apply_end (apply_end),
  KEY idx_programs_status (status),
  KEY idx_programs_category (category),
  KEY idx_programs_source (source_code),
  KEY idx_programs_collected (collected_at)
) ENGINE=InnoDB;

-- 태그
CREATE TABLE IF NOT EXISTS tags (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_tags_name (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS program_tags (
  program_id BIGINT UNSIGNED NOT NULL,
  tag_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (program_id, tag_id),
  KEY idx_pt_tag (tag_id),
  CONSTRAINT fk_pt_program FOREIGN KEY (program_id) REFERENCES programs (id) ON DELETE CASCADE,
  CONSTRAINT fk_pt_tag FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 동일 공고의 다중 출처 링크
CREATE TABLE IF NOT EXISTS program_sources (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  program_id BIGINT UNSIGNED NOT NULL,
  source_code VARCHAR(32) NOT NULL,
  source_url VARCHAR(1000) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_ps_url (source_url(500)),
  KEY idx_ps_program (program_id),
  CONSTRAINT fk_ps_program FOREIGN KEY (program_id) REFERENCES programs (id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 크롤 실행 이력
CREATE TABLE IF NOT EXISTS crawl_runs (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  started_at DATETIME NOT NULL,
  finished_at DATETIME NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'running' COMMENT 'running, success, failed',
  new_count INT UNSIGNED NOT NULL DEFAULT 0,
  updated_count INT UNSIGNED NOT NULL DEFAULT 0,
  error_message TEXT NULL,
  PRIMARY KEY (id),
  KEY idx_crawl_started (started_at)
) ENGINE=InnoDB;

-- 초기 소스 시드
INSERT INTO sources (code, name, base_url, enabled) VALUES
  ('kstartup', 'K-Startup', 'https://www.k-startup.go.kr', 1),
  ('bizinfo', '기업마당', 'https://www.bizinfo.go.kr', 1),
  ('kised', '창업진흥원', 'https://www.kised.or.kr', 1),
  ('mss', '중소벤처기업부', 'https://www.mss.go.kr', 1)
ON DUPLICATE KEY UPDATE name = VALUES(name), base_url = VALUES(base_url);

-- 개발용 더미 공고 (UI 확인용)
INSERT INTO programs (
  title, summary, organization, category, region, target_audience,
  apply_start, apply_end, status, source_code, source_url, external_id,
  content_hash, content_md, collected_at
) VALUES
(
  '2026 예비창업패키지 모집 공고 (더미)',
  '혁신적인 아이디어를 가진 예비창업자를 위한 사업화 지원 프로그램입니다.',
  '창업진흥원',
  '지원사업',
  '전국',
  '예비창업',
  CURDATE(),
  DATE_ADD(CURDATE(), INTERVAL 21 DAY),
  'open',
  'kstartup',
  'https://www.k-startup.go.kr/dummy/pre-startup-2026',
  'dummy-001',
  SHA2('dummy-001', 256),
  '더미 데이터입니다. 실제 공고가 아닙니다.',
  NOW()
),
(
  'AI 스타트업 경진대회 2026 (더미)',
  'AI·딥테크 분야 창업팀 대상 전국 경진대회. 우승팀 사업화 자금 지원.',
  '중소벤처기업부',
  '경진대회',
  '전국',
  '초기창업',
  CURDATE(),
  DATE_ADD(CURDATE(), INTERVAL 7 DAY),
  'open',
  'mss',
  'https://www.mss.go.kr/dummy/ai-contest-2026',
  'dummy-002',
  SHA2('dummy-002', 256),
  '더미 데이터입니다. 실제 공고가 아닙니다.',
  NOW()
),
(
  '서울 창업허브 입주기업 모집 (더미)',
  '서울 소재 초기 스타트업 대상 입주·멘토링 프로그램.',
  '서울창업허브',
  '지원사업',
  '서울',
  '초기창업',
  DATE_SUB(CURDATE(), INTERVAL 30 DAY),
  DATE_SUB(CURDATE(), INTERVAL 1 DAY),
  'closed',
  'bizinfo',
  'https://www.bizinfo.go.kr/dummy/seoul-hub',
  'dummy-003',
  SHA2('dummy-003', 256),
  '더미 데이터입니다. 실제 공고가 아닙니다.',
  NOW()
)
ON DUPLICATE KEY UPDATE title = VALUES(title);
