SELECT  
        to_timestamp(start_time)::date AS pt_date,
        p.patch,
        count(distinct case when radiant_win then m.match_id end) as radiant_wins,
		count(distinct m.match_id) as qt_matches,
        greatest(max(dire_score),max(radiant_score)) as bigger_score,
		least(min(case when dire_score != 0 then dire_score end),min(case when radiant_score != 0 then radiant_score end))lowest_score,
		AVG((radiant_score + dire_score) / 2.0) AS average_score,
		AVG(duration) average_duration,
		MAX(duration) bigger_duration

FROM dota_dw.matches as m
LEFT JOIN dota_dw.match_patch as p
ON m.match_id = p.match_id
group by 1,2

order by 1 desc  