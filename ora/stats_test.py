from stats import single_match_stats

stat_instance = single_match_stats.SingleMatchStats('stats/UITEST_data.zip')

print(stat_instance.all_eliminations)
print(stat_instance.get_teamfight_index(100))