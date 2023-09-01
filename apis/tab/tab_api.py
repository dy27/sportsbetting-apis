import requests
import json
from dataclasses import dataclass
from RacingAPI import Runner, RaceResponse

@dataclass
class TabRaceInfo:
    """
    meeting_date: date in YYYY-MM-DD format
    venue_mnemonic: shortened form of the venue name
    race_type: "R" for racing (horses), "G" for greyhounds, "H" for harness
    race_number: the race number of the race
    """
    meeting_date: str
    race_type: str
    venue_mnemonic: str
    venue_name: str
    race_number: int
    start_time: str
    

class TabRaceResponse(RaceResponse):
    def get_race_id():
        pass

class TabAPI:
    def __init__(self, jurisdiction):
        """
        jurisdiction: string value of either NSW, VIC, ACT, QLD, SA, NT or TAS
        """
        self.api_link = "https://api.beta.tab.com.au/v1/tab-info-service"
        self.jurisdiction = jurisdiction

    def get_races(self, date) -> list[TabRaceInfo]:
        url = f"{self.api_link}/racing/dates/{date}/meetings?jurisdiction={self.jurisdiction}"
        response = requests.request("GET", url)
        if response.status_code != requests.codes.ok:
            return []
        response_dict = json.loads(response.text)
        races = []
        for meeting in response_dict["meetings"]:
            for race in meeting["races"]:
                race_info = TabRaceInfo(
                    meeting_date=meeting["meetingDate"],
                    race_type=meeting["raceType"],
                    venue_mnemonic=meeting["venueMnemonic"],
                    venue_name=meeting["meetingName"],
                    race_number=int(race["raceNumber"]),
                    start_time=race["raceStartTime"]
                )
                races.append(race_info)
        return races

    def get_race_odds(self, req: TabRaceInfo) -> list[Runner]:
        url = f"{self.api_link}/racing/dates/{req.meeting_date}/meetings/{req.race_type}/{req.venue_mnemonic}/races/{req.race_number}?jurisdiction={self.jurisdiction}"
        response = requests.request("GET", url)
        if response.status_code != requests.codes.ok:
            return []
        response_dict = json.loads(response.text)
        runners = []
        for runner_dict in response_dict["runners"]:
            runner = Runner(runner_dict["runnerName"], int(runner_dict["runnerNumber"]))
            if "fixedOdds" in runner_dict:
                runner.fixed_odds = {
                    "win": runner_dict["fixedOdds"]["returnWin"] if "returnWin" in runner_dict["fixedOdds"] else None,
                    "place": runner_dict["fixedOdds"]["returnPlace"] if "returnPlace" in runner_dict["fixedOdds"] else None,
                }
            if "parimutuel" in runner_dict:
                runner.tote_odds = {
                    "win": runner_dict["parimutuel"]["returnWin"] if "returnWin" in runner_dict["parimutuel"] else None,
                    "place": runner_dict["parimutuel"]["returnPlace"] if "returnPlace" in runner_dict["parimutuel"] else None
                }
            runners.append(runner)
        return runners


if __name__ == "__main__":
    api = TabAPI(jurisdiction="NSW")

    req = TabRaceInfo(
        meeting_date = "2022-04-16",
        race_type = "R",
        venue_mnemonic = "LIN",
        race_number = "1",
    )

    api.get_race_odds(req)