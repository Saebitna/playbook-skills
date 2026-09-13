import csv


def export_rows(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerows(rows)


# WIP: parquet 백엔드 추가 중. writer 추상화까지 했고
# 스키마 추론이 남음. pyarrow 의존성 추가 여부 미결정.
def export_parquet(rows, path):
    raise NotImplementedError
