FOR /F "TOKENS=1* DELIMS= " %%A IN ('DATE/T') DO SET CDATE=%%B
FOR /F "TOKENS=1,2 eol=/ DELIMS=/ " %%A IN ('DATE/T') DO SET mm=%%B
FOR /F "TOKENS=1,2 DELIMS=/ eol=/" %%A IN ('echo %CDATE%') DO SET dd=%%B
FOR /F "TOKENS=2,3 DELIMS=/ " %%A IN ('echo %CDATE%') DO SET yyyy=%%B
SET date=%yyyy%%mm%%dd%
mysqldump uummuu_test > C:\UUMMUU_Code\MysqlDumps\uummuu_test_%date%.sql -u logger
mysqldump uummuu_production > C:\UUMMUU_Code\MysqlDumps\uummuu_production_%date%.sql -u logger
mysqldump uummuu_development > C:\UUMMUU_Code\MysqlDumps\uummuu_development_%date%.sql -u logger
exit