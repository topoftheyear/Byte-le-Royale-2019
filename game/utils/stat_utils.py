

def compile_stats(domain, stats, ignore_fields=[]):
    stat_names = list(stats[0][domain][1].keys())


    for r in ignore_fields:
        if r in stat_names:
            stat_names.remove(r)

    print(stat_names)

    compiled = {  }
    for t in stats:
        for station in t[domain]:
            if station["station_name"] not in compiled:
                compiled[station["station_name"]] = {}

            for stat_name in stat_names:
                if stat_name not in compiled[station["station_name"]]:
                    compiled[station["station_name"]][stat_name] = []

                compiled[station["station_name"]][stat_name].append(station[stat_name])

    return compiled
