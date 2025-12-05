USE AirQuality_DW;
GO

-- Sửa lỗi chữ "Rất Cao"
UPDATE FactPolicyEvent
SET ImpactLevel = N'Rất Cao'
WHERE ImpactLevel LIKE 'Rá%';

-- Sửa lỗi chữ "Trung bình"
UPDATE FactPolicyEvent
SET ImpactLevel = N'Trung bình'
WHERE ImpactLevel LIKE 'Trung b%';

UPDATE FactPolicyEvent
SET ImpactLevel = N'Thấp'
WHERE ImpactLevel LIKE 'Tháº¥p';
-- Kiểm tra lại xem đẹp chưa
SELECT * FROM FactPolicyEvent;