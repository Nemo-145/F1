import fastf1
import pandas as pd
from config import CACHE_DIR, DATA_RAW_DIR, SessionTypes
from config import YEAR, GRAND_PRIX, START_YEAR, END_YEAR, SEASONS
from logging_config import logger

fastf1.Cache.enable_cache(str(CACHE_DIR))
def get_race_results(year: int, grand_prix: str) -> pd.DataFrame:
    session = fastf1.get_session(year, grand_prix, SessionTypes.RACE.value)
    session.load(laps=False, telemetry=False, weather=False, messages=False)
    results = session.results
    results_df = results[['Position', 'GridPosition', 'FullName', 'TeamName', 'Status', 'Points', 'ClassifiedPosition', 'Laps', 'Time']].copy()
    results_df['Year'] = year
    results_df['Grand Prix'] = grand_prix
    return results_df


def collect_all_data(years):
    all_results = []
    for year in years:
        logger.info(f"Processing season {year}")
        schedule = fastf1.get_event_schedule(year)
        past_races = schedule[(schedule['EventDate'] < pd.Timestamp.now()) & ~schedule['EventName'].str.contains('Test')]
        for row in past_races.itertuples():
            try:
                logger.info(f"Downloading {row.EventName} {year}")
                df = get_race_results(year, row.EventName)
                all_results.append(df)
            except Exception as e:
                logger.error(f"Could not load {row.EventName}: {e}")
                continue
    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        return final_df
    return pd.DataFrame()
        
if __name__ == "__main__":
    logger.info(f"Loading races results for {GRAND_PRIX} {YEAR}")

    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    save_path = DATA_RAW_DIR / f"all_races_{START_YEAR}_{END_YEAR}.csv"
    
    results_df = collect_all_data(SEASONS)

    if not results_df.empty:  
        results_df.to_csv(save_path, index=False)

    logger.info(f"Races results saved to {save_path}")
    logger.info(results_df.head())
    
    