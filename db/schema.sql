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
  ('mss', '중소벤처기업부', 'https://www.mss.go.kr', 1),
  ('wishket', '위시켓', 'https://www.wishket.com/project/', 1),
  ('freemoa', '프리모아', 'https://www.freemoa.net/m4/s41', 1),
  ('elancer', '이랜서', 'https://www.elancer.co.kr/list-partner', 1)
ON DUPLICATE KEY UPDATE name = VALUES(name), base_url = VALUES(base_url);

-- 공고 데이터는 크롤러가 수집. 시드 더미는 넣지 않음.

-- 프리랜서 개발 일감 (공고와 분리)
CREATE TABLE IF NOT EXISTS jobs (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(500) NOT NULL,
  summary TEXT NULL,
  organization VARCHAR(200) NULL COMMENT '발주·클라이언트',
  skills JSON NULL COMMENT '기술 스택 문자열 배열',
  work_type VARCHAR(20) NOT NULL DEFAULT 'remote' COMMENT 'remote, onsite, hybrid',
  budget_text VARCHAR(100) NULL COMMENT '화면 표시용 예산/단가',
  budget_band VARCHAR(20) NOT NULL DEFAULT 'unknown' COMMENT 'lt_500, mid, high, unknown',
  duration_text VARCHAR(100) NULL,
  region VARCHAR(100) NULL,
  apply_end DATE NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'open' COMMENT 'open, closed',
  source_code VARCHAR(32) NOT NULL,
  source_url VARCHAR(1000) NOT NULL,
  external_id VARCHAR(200) NULL,
  content_hash CHAR(64) NULL,
  collected_at DATETIME NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_jobs_source_url (source_url(500)),
  KEY idx_jobs_status (status),
  KEY idx_jobs_work_type (work_type),
  KEY idx_jobs_budget_band (budget_band),
  KEY idx_jobs_apply_end (apply_end),
  KEY idx_jobs_source (source_code),
  KEY idx_jobs_collected (collected_at)
) ENGINE=InnoDB;
