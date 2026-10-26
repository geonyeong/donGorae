-- 기존 DB에 일감 수집 소스를 추가한다. jobs 테이블은 002_jobs.sql.
-- 구조 변경은 없고 sources 행만 넣는다.

INSERT INTO sources (code, name, base_url, enabled) VALUES
  ('wishket', '위시켓', 'https://www.wishket.com/project/', 1),
  ('freemoa', '프리모아', 'https://www.freemoa.net/m4/s41', 1),
  ('elancer', '이랜서', 'https://www.elancer.co.kr/list-partner', 1)
ON DUPLICATE KEY UPDATE name = VALUES(name), base_url = VALUES(base_url);
