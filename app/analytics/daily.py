from app.core.db import connect


def build_daily_snapshot(therapy_date: str):
    db=connect()
    rows=[dict(r) for r in db.execute('SELECT * FROM sleep_sessions WHERE therapy_date=? ORDER BY start_time',(therapy_date,)).fetchall()]
    prisma=[dict(r) for r in db.execute('SELECT * FROM daily_metrics WHERE therapy_date=? ORDER BY id DESC',(therapy_date,)).fetchall()]
    db.close()
    total_hours=sum(r['usage_hours'] or 0 for r in rows)
    oa=sum(r['oa'] or 0 for r in rows)
    ca=sum(r['ca'] or 0 for r in rows)
    hi=sum(r['hi'] or 0 for r in rows)
    ua=sum(r['ua'] or 0 for r in rows)
    total_events=oa+ca+hi+ua
    return {
        'therapy_date': therapy_date,
        'session_count': len(rows),
        'usage_hours': round(total_hours,3) if total_hours else None,
        'oscar_event_weighted_ahi': round(total_events/total_hours,3) if total_hours else None,
        'oscar_oa_index': round(oa/total_hours,3) if total_hours else None,
        'oscar_ca_index': round(ca/total_hours,3) if total_hours else None,
        'oscar_hi_index': round(hi/total_hours,3) if total_hours else None,
        'oscar_rera_index': round(sum(r['rera'] or 0 for r in rows)/total_hours,3) if total_hours else None,
        'prismats': prisma[0] if prisma else None,
    }
