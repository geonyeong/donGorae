-- 기존 DB에 일감 테이블 추가 (schema.sql은 최초 기동 시에만 적용됨)
USE dongorae;

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
